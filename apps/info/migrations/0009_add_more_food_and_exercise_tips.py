from decimal import Decimal

from django.db import migrations


FOODS = [
    {
        'name': 'Vegetable mung bean stew',
        'description': 'A budget-friendly plant-based meal with mung beans and vegetables. Check seasonings and packaged ingredients for allergens and added salt.',
        'ingredients': 'Mung beans, leafy greens, squash, tomato, onion, garlic, and water or broth.',
        'preparation_details': 'Simmer mung beans until tender, add chopped vegetables, and cook until soft. Season lightly and serve with rice if desired.',
        'meal_type': 'lunch',
        'calories': 310,
        'estimated_cost': Decimal('45.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': [],
    },
    {
        'name': 'Chicken arroz caldo',
        'description': 'A warm rice porridge with chicken and ginger. Keep toppings separate and check broth or seasoning labels for allergens.',
        'ingredients': 'Rice, chicken, ginger, garlic, onion, and water or low-sodium broth.',
        'preparation_details': 'Simmer rice with broth until soft, add chicken, and cook thoroughly. Serve with optional toppings on the side.',
        'meal_type': 'breakfast',
        'calories': 330,
        'estimated_cost': Decimal('55.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': [],
    },
    {
        'name': 'Tofu and vegetable stir-fry',
        'description': 'A plant-protein meal with mixed vegetables. Tofu contains soy; use a soy-free alternative for people with soy allergy.',
        'ingredients': 'Firm tofu, cabbage, carrots, and garlic. Optional sauce may contain soy or wheat.',
        'preparation_details': 'Cook tofu thoroughly and stir-fry with vegetables. Check sauce ingredients and use a small amount of oil.',
        'meal_type': 'dinner',
        'calories': 350,
        'estimated_cost': Decimal('65.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': ['soy'],
    },
    {
        'name': 'Boiled egg and sweet potato',
        'description': 'A simple snack or light breakfast with egg protein and sweet potato. Contains egg.',
        'ingredients': 'One egg and one medium sweet potato.',
        'preparation_details': 'Boil the egg until fully cooked and steam or boil the sweet potato until tender.',
        'meal_type': 'snack',
        'calories': 230,
        'estimated_cost': Decimal('35.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': ['eggs'],
    },
    {
        'name': 'Tuna and cucumber rice bowl',
        'description': 'A quick rice bowl with tuna and fresh vegetables. Contains fish; check canned tuna labels and choose a lower-sodium option when available.',
        'ingredients': 'Cooked rice, canned tuna, cucumber, and tomato.',
        'preparation_details': 'Drain tuna, combine with washed vegetables, and serve over freshly cooked rice.',
        'meal_type': 'lunch',
        'calories': 390,
        'estimated_cost': Decimal('70.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': ['fish'],
    },
    {
        'name': 'Papaya and banana fruit cup',
        'description': 'A refreshing fruit snack with no added sweetener needed. Wash and cut fruit with clean utensils.',
        'ingredients': 'Ripe papaya and banana.',
        'preparation_details': 'Wash, peel, and cut the fruit into bite-size pieces. Serve fresh.',
        'meal_type': 'snack',
        'calories': 140,
        'estimated_cost': Decimal('30.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': [],
    },
    {
        'name': 'Corn and vegetable soup',
        'description': 'A light soup with corn and seasonal vegetables. Use water or a broth whose label has been checked for allergens.',
        'ingredients': 'Corn, carrots, cabbage, onion, garlic, and water or low-sodium broth.',
        'preparation_details': 'Simmer vegetables until tender. Add corn near the end and heat through.',
        'meal_type': 'dinner',
        'calories': 210,
        'estimated_cost': Decimal('45.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': [],
    },
    {
        'name': 'Overnight oats with mango',
        'description': 'A make-ahead oat breakfast with fresh mango. Use a safe liquid base and check labels on packaged oats.',
        'ingredients': 'Rolled oats, water or allergy-safe milk, and ripe mango.',
        'preparation_details': 'Combine oats and liquid, refrigerate overnight, and top with freshly cut mango before serving.',
        'meal_type': 'breakfast',
        'calories': 290,
        'estimated_cost': Decimal('40.00'),
        'weight_status': 'all',
        'conditions': ['all'],
        'allergens': [],
    },
]

EXERCISES = [
    {
        'name': 'Indoor marching',
        'description': 'March gently in place near a stable support, keeping a comfortable pace and taking breaks as needed.',
        'intensity': 'low',
        'duration_minutes': 10,
        'weight_status': 'all',
        'min_age': 10,
        'max_age': 100,
        'conditions': ['all'],
        'avoid_conditions': [],
    },
    {
        'name': 'Seated mobility routine',
        'description': 'Perform comfortable shoulder rolls, ankle circles, and gentle seated leg movements. Avoid movements that cause pain.',
        'intensity': 'low',
        'duration_minutes': 12,
        'weight_status': 'all',
        'min_age': 10,
        'max_age': 100,
        'conditions': ['all'],
        'avoid_conditions': [],
    },
    {
        'name': 'Wall push-ups',
        'description': 'A beginner strength movement using a wall for support. Keep the movement controlled and stop if you feel discomfort.',
        'intensity': 'low',
        'duration_minutes': 10,
        'weight_status': 'all',
        'min_age': 16,
        'max_age': 75,
        'conditions': ['all'],
        'avoid_conditions': ['heart'],
    },
    {
        'name': 'Easy stationary cycling',
        'description': 'Cycle at a relaxed pace on a stationary bike with an easy resistance setting. Adjust the seat and stop if you feel unwell.',
        'intensity': 'low',
        'duration_minutes': 15,
        'weight_status': 'all',
        'min_age': 14,
        'max_age': 80,
        'conditions': ['all'],
        'avoid_conditions': ['heart'],
    },
    {
        'name': 'Beginner balance practice',
        'description': 'Practice standing near a sturdy chair or counter. Use support as needed and do not attempt unsupported balancing if unsafe.',
        'intensity': 'low',
        'duration_minutes': 8,
        'weight_status': 'all',
        'min_age': 18,
        'max_age': 100,
        'conditions': ['all'],
        'avoid_conditions': [],
    },
    {
        'name': 'Gentle dance steps',
        'description': 'Follow simple, low-impact dance steps at a pace where you can still speak comfortably. Keep the floor clear.',
        'intensity': 'low',
        'duration_minutes': 15,
        'weight_status': 'all',
        'min_age': 12,
        'max_age': 75,
        'conditions': ['all'],
        'avoid_conditions': ['heart'],
    },
    {
        'name': 'Low-impact step-touch',
        'description': 'Step side to side without jumping, using a small range of motion and a comfortable pace.',
        'intensity': 'low',
        'duration_minutes': 12,
        'weight_status': 'all',
        'min_age': 12,
        'max_age': 75,
        'conditions': ['all'],
        'avoid_conditions': ['heart'],
    },
    {
        'name': 'Gentle pool walking',
        'description': 'Walk slowly in shallow water only where it is safe and supervised. Use pool access rails and follow facility rules.',
        'intensity': 'low',
        'duration_minutes': 15,
        'weight_status': 'all',
        'min_age': 18,
        'max_age': 80,
        'conditions': ['all'],
        'avoid_conditions': ['heart', 'asthma'],
    },
]


def add_catalog_items(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')
    ExerciseItem = apps.get_model('info', 'ExerciseItem')

    for food in FOODS:
        if not FoodItem.objects.filter(name=food['name']).exists():
            FoodItem.objects.create(**food)
    for exercise in EXERCISES:
        if not ExerciseItem.objects.filter(name=exercise['name']).exists():
            ExerciseItem.objects.create(**exercise)


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_estimate_current_food_prices'),
    ]

    operations = [
        migrations.RunPython(add_catalog_items, migrations.RunPython.noop),
    ]
