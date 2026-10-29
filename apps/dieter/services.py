"""BMI status and simple food/exercise matching."""

from decimal import Decimal

from apps.info.models import ExerciseItem, FoodItem, WeightStatus


def foods_for_profile(profile):
    weight_statuses = [WeightStatus.ALL]
    if profile.age >= 20:
        weight_statuses.append(profile.status)

    preferred_food = (profile.health_status_answers or {}).get('food_preference')
    items = FoodItem.objects.filter(
        weight_status__in=weight_statuses,
    )
    return [
        item for item in items
        if _matches_condition(item.conditions, profile.recommendation_conditions)
        and _matches_food_preference(item, preferred_food)
        and not _matches_food_allergy(item, profile)
    ]


def budget_food_plan(profile):
    """Choose one affordable, profile-safe food for as many meal types as possible."""
    if profile.daily_food_budget is None:
        return []

    affordable_by_meal = {}
    for food in foods_for_profile(profile):
        if food.estimated_cost is None:
            continue
        current = affordable_by_meal.get(food.meal_type)
        if current is None or food.estimated_cost < current.estimated_cost:
            affordable_by_meal[food.meal_type] = food

    plan = sorted(
        affordable_by_meal.values(),
        key=lambda food: (food.estimated_cost, food.meal_type),
    )
    while plan and sum((food.estimated_cost for food in plan), start=0) > profile.daily_food_budget_limit:
        plan.pop()
    return sorted(plan, key=lambda food: (food.meal_type, food.name))


def recommended_foods_for_profile(profile):
    if profile.daily_food_budget is not None:
        return budget_food_plan(profile)
    return foods_for_profile(profile)


def total_food_plan_cost(foods):
    return sum(
        (food.estimated_cost for food in foods if food.estimated_cost is not None),
        start=Decimal('0.00'),
    )


def exercises_for_profile(profile):
    preferred_intensity = (profile.health_status_answers or {}).get('exercise_intensity') or 'moderate'
    items = ExerciseItem.objects.filter(
        weight_status__in=[profile.status, WeightStatus.ALL],
        min_age__lte=profile.age,
        max_age__gte=profile.age,
    )
    results = []
    for item in items:
        if set(profile.recommendation_conditions).intersection(item.avoid_conditions or []):
            continue
        if profile.age >= 60 and item.intensity == 'high':
            continue
        if not _matches_exercise_intensity(item.intensity, preferred_intensity):
            continue
        if _matches_condition(item.conditions, profile.recommendation_conditions):
            results.append(item)
    return results


def _matches_condition(conditions, user_condition):
    if not conditions or 'all' in conditions:
        return True
    if isinstance(user_condition, str):
        user_condition = [user_condition]
    return set(user_condition).issubset(set(conditions))


def _matches_food_preference(item, preferred_food):
    if not preferred_food or preferred_food == 'balanced':
        return True

    text = (item.name + ' ' + item.description + ' ' + (item.ingredients or '')).casefold()
    if preferred_food == 'high_protein':
        protein_keywords = ['chicken', 'egg', 'beans', 'yogurt', 'fish', 'protein', 'tofu', 'lentil', 'bean', 'beef']
        return any(keyword in text for keyword in protein_keywords)
    if preferred_food == 'low_calorie':
        return 'salad' in text or 'vegetable' in text or 'soup' in text or item.calories <= 350
    if preferred_food == 'high_fiber':
        fiber_keywords = ['oat', 'oats', 'beans', 'vegetable', 'fruit', 'whole grain', 'brown rice', 'lentil', 'quinoa']
        return any(keyword in text for keyword in fiber_keywords)
    if preferred_food == 'vegetarian':
        animal_keywords = ['chicken', 'fish', 'beef', 'pork', 'turkey', 'egg', 'milk', 'yogurt', 'shrimp', 'meat']
        return not any(keyword in text for keyword in animal_keywords)
    if preferred_food == 'easy_digest':
        digest_keywords = ['banana', 'oat', 'rice', 'soup', 'grilled', 'steamed', 'smoothie', 'fruit']
        return any(keyword in text for keyword in digest_keywords)
    return True


def _matches_exercise_intensity(item_intensity, preferred_intensity):
    if not preferred_intensity:
        return True
    intensity_groups = {
        'light': {'low'},
        'moderate': {'low', 'moderate'},
        'heavy': {'moderate', 'high'},
    }
    return item_intensity in intensity_groups.get(preferred_intensity, {'low', 'moderate', 'high'})


def _matches_food_allergy(item, profile):
    allergens = [allergen.casefold().strip() for allergen in item.allergens or []]
    allergy_terms = {
        term.casefold().strip()
        for term in profile.food_allergy_details.replace(';', ',').replace('\n', ',').split(',')
        if term.strip()
    }
    allergy_choices = (profile.health_status_answers or {}).get('food_allergy_options', [])
    if 'other' in allergy_choices:
        return True
    allergen_labels = {
        'peanuts': {'peanut', 'peanuts'},
        'tree_nuts': {'tree nut', 'tree nuts', 'almond', 'cashew', 'walnut', 'pecan', 'pistachio', 'hazelnut'},
        'milk': {'milk', 'dairy'},
        'eggs': {'egg', 'eggs'},
        'wheat': {'wheat'},
        'soy': {'soy', 'soya'},
        'fish': {'fish'},
        'shellfish': {'shellfish', 'shrimp', 'crab', 'lobster'},
        'sesame': {'sesame'},
    }
    for choice in allergy_choices:
        allergy_terms.update(allergen_labels.get(choice, set()))
    if allergy_terms and not allergens:
        return True
    return any(
        term in allergen or allergen in term
        for term in allergy_terms
        for allergen in allergens
    )
