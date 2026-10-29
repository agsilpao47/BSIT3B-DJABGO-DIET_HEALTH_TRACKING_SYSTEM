from decimal import Decimal

from django.db import migrations


FOODS = [
    ('Banana and boiled egg', 'A quick breakfast pairing fresh fruit with a fully cooked egg.', 'One banana and one egg.', 'Boil the egg until fully cooked and serve with a washed banana.', 'breakfast', 'mixed', 190, '20.00', ['eggs']),
    ('Garlic rice with scrambled egg', 'A simple, filling breakfast made with rice and egg.', 'Cooked rice, egg, garlic, and a small amount of cooking oil.', 'Cook garlic briefly, add rice, then serve with thoroughly cooked scrambled egg.', 'breakfast', 'mixed', 360, '25.00', ['eggs']),
    ('Sweet potato and banana bowl', 'A low-cost, naturally sweet breakfast using common produce.', 'Steamed sweet potato and ripe banana.', 'Steam sweet potato until tender, peel, and serve with sliced banana.', 'breakfast', 'mixed', 250, '25.00', []),
    ('Mongo and rice porridge', 'A warm, filling plant-based breakfast with mung beans and rice.', 'Mung beans, rice, onion, garlic, and water.', 'Simmer soaked mung beans until soft, add rice, and cook until porridge-like.', 'breakfast', 'mixed', 300, '25.00', []),
    ('Papaya oatmeal', 'Warm oats topped with ripe papaya for a simple fruit breakfast.', 'Rolled oats, water, and ripe papaya.', 'Cook oats in water until soft and top with washed, peeled papaya.', 'breakfast', 'mixed', 270, '30.00', []),
    ('Tomato and egg rice bowl', 'A straightforward rice meal with tomato and cooked egg.', 'Rice, tomato, egg, onion, and a small amount of oil.', 'Cook tomato and onion until soft, add egg and cook through, then serve over rice.', 'breakfast', 'mixed', 340, '30.00', ['eggs']),
    ('Chicken and cabbage rice bowl', 'A simple lunch bowl with chicken, cabbage, and rice.', 'Cooked chicken, cabbage, rice, garlic, and onion.', 'Cook chicken thoroughly, soften cabbage with garlic, and serve with rice.', 'lunch', 'mixed', 430, '55.00', []),
    ('Sardines with rice and pechay', 'An economical fish-and-vegetable meal. Check canned sardine labels for salt and allergens.', 'Canned sardines, rice, pechay, onion, and calamansi.', 'Heat sardines thoroughly, steam washed pechay, and serve with rice.', 'lunch', 'mixed', 420, '40.00', ['fish']),
    ('Tofu and kangkong rice bowl', 'A plant-based bowl with tofu and leafy kangkong.', 'Tofu, kangkong, rice, garlic, and a small amount of cooking oil.', 'Cook tofu thoroughly, sauté washed kangkong, and serve with rice.', 'lunch', 'mixed', 390, '40.00', ['soy']),
    ('Chicken tinola with rice', 'A home-style chicken and vegetable soup served with rice.', 'Chicken, sayote, malunggay, ginger, and rice.', 'Simmer chicken until fully cooked, add sayote and malunggay, and serve with rice.', 'lunch', 'mixed', 420, '55.00', []),
    ('Squash and monggo stew', 'A filling plant-based stew of mung beans and squash.', 'Mung beans, squash, onion, garlic, and water.', 'Simmer mung beans until soft, add squash, and cook until tender.', 'lunch', 'mixed', 330, '35.00', []),
    ('Vegetable pancit bihon', 'Rice noodles with mixed vegetables for a simple meal.', 'Bihon noodles, cabbage, carrots, green beans, and garlic.', 'Soften noodles and stir-fry with cooked vegetables; check seasoning for allergens.', 'lunch', 'mixed', 380, '35.00', []),
    ('Chicken adobo with vegetables', 'A portion of chicken with vegetables and rice. Use a moderate amount of sauce.', 'Chicken, rice, kangkong, garlic, vinegar, and soy sauce.', 'Cook chicken thoroughly in vinegar and seasoning; serve with rice and vegetables.', 'dinner', 'mixed', 480, '60.00', ['soy', 'wheat']),
    ('Grilled tilapia with rice', 'Grilled tilapia served with rice and a seasonal vegetable side.', 'Tilapia, rice, tomato, and leafy vegetables.', 'Grill tilapia until fully cooked and serve with rice and washed vegetables.', 'dinner', 'mixed', 430, '65.00', ['fish']),
    ('Lentil and tomato rice bowl', 'A plant-based bowl with lentils, tomato, and rice.', 'Lentils, tomato, onion, garlic, and rice.', 'Simmer lentils until tender with tomato and aromatics; serve with cooked rice.', 'dinner', 'mixed', 400, '45.00', []),
    ('Eggplant and egg rice plate', 'A home-style eggplant and egg meal with rice.', 'Eggplant, egg, rice, tomato, and onion.', 'Cook eggplant until tender, add thoroughly cooked egg, and serve with rice.', 'dinner', 'mixed', 390, '40.00', ['eggs']),
    ('Seasonal fruit cup', 'A small snack of fresh seasonal fruit with no added sugar.', 'Seasonal fruit such as banana, papaya, or watermelon.', 'Wash fruit, peel or cut with clean utensils, and serve fresh.', 'snack', 'fruit', 100, '20.00', []),
    ('Boiled saba banana', 'A filling, low-cost snack made with saba banana.', 'One saba banana and water.', 'Boil banana in water until tender and allow it to cool before serving.', 'snack', 'fruit', 120, '15.00', []),
    ('Cucumber and tomato salad', 'A refreshing vegetable side with a light calamansi dressing.', 'Cucumber, tomato, calamansi, and a small pinch of salt.', 'Wash vegetables, slice with clean utensils, and dress just before serving.', 'snack', 'vegetable', 70, '20.00', []),
    ('Boiled corn on the cob', 'A simple snack of boiled corn without added butter.', 'One ear of corn and water.', 'Boil corn until tender and serve warm.', 'snack', 'grain', 150, '20.00', []),
]


EXERCISES = [
    ('Indoor seated marching', 'March slowly while seated in a sturdy chair, keeping movements comfortable.', 'low', 'indoor', 10, 10, 100, []),
    ('Indoor standing calf raises', 'Rise gently onto the balls of your feet while holding a stable counter for support.', 'low', 'indoor', 10, 16, 80, []),
    ('Indoor supported sit-to-stand', 'Practice standing from a sturdy chair and sitting back down slowly, using support as needed.', 'low', 'indoor', 8, 18, 100, []),
    ('Indoor gentle core brace', 'While seated or lying comfortably, gently tighten your abdominal muscles while breathing normally.', 'low', 'indoor', 8, 16, 80, []),
    ('Indoor step-ups on a low step', 'Step slowly onto a low, stable step near a handrail; skip this activity if balance is uncertain.', 'moderate', 'indoor', 10, 18, 65, ['heart']),
    ('Indoor resistance-band rows', 'Pull a light resistance band toward your torso with controlled movement and comfortable range.', 'moderate', 'indoor', 15, 16, 75, ['heart']),
    ('Indoor low-impact aerobics', 'Follow simple side steps and arm movements at a pace that lets you speak comfortably.', 'moderate', 'indoor', 15, 16, 70, ['heart']),
    ('Indoor yoga flow', 'Move through gentle standing and seated stretches, avoiding poses that cause discomfort.', 'moderate', 'indoor', 20, 16, 70, ['heart']),
    ('Indoor dumbbell basics', 'Use light weights for controlled curls and shoulder movements; stop if you feel pain.', 'moderate', 'indoor', 15, 18, 65, ['heart']),
    ('Indoor dance workout', 'Dance to music using simple steps and take breaks to keep a comfortable pace.', 'moderate', 'indoor', 20, 16, 65, ['heart']),
    ('Outdoor easy neighborhood walk', 'Walk on a familiar, level route in daylight and choose a comfortable pace.', 'low', 'outdoor', 15, 10, 100, []),
    ('Outdoor park mobility', 'Do gentle shoulder, ankle, and leg movements in a clear, stable outdoor space.', 'low', 'outdoor', 12, 10, 100, []),
    ('Outdoor easy cycling', 'Cycle on a safe, level route with a helmet and appropriate traffic precautions.', 'moderate', 'outdoor', 20, 16, 65, ['heart']),
    ('Outdoor beginner badminton', 'Play gentle rallies in a clear area, pausing as needed and avoiding sudden movements.', 'moderate', 'outdoor', 20, 16, 60, ['heart']),
    ('Outdoor relaxed swimming', 'Swim only in a supervised, safe area and stay within your comfort level.', 'moderate', 'outdoor', 15, 16, 70, ['heart', 'asthma']),
    ('Outdoor easy hill walk', 'Walk a gentle incline at a relaxed pace on a safe, maintained path.', 'moderate', 'outdoor', 15, 18, 60, ['heart']),
    ('Outdoor brisk walking intervals', 'Alternate one minute of brisk walking with two minutes at an easy pace on level ground.', 'moderate', 'outdoor', 20, 18, 60, ['heart']),
    ('Outdoor bodyweight circuit', 'Combine supported squats, wall push-ups, and marching with rest between movements.', 'high', 'outdoor', 20, 18, 50, ['heart', 'asthma', 'hypertension']),
    ('Outdoor jogging intervals', 'For people already comfortable jogging, alternate short easy jogs with walking recovery.', 'high', 'outdoor', 20, 18, 45, ['heart', 'asthma', 'hypertension']),
    ('Outdoor jump-rope intervals', 'A higher-impact option for people accustomed to exercise; use a clear surface and stop if uncomfortable.', 'high', 'outdoor', 10, 18, 40, ['heart', 'asthma', 'hypertension']),
]


PRICE_UPDATES = {
    'Oatmeal with berries': '35.00',
    'Vegetable omelet': '45.00',
    'Baked salmon with vegetables': '140.00',
    'Grilled chicken salad': '65.00',
    'Lentil and vegetable soup': '40.00',
    'Apple with unsalted nuts': '35.00',
    'Grilled chicken with brown rice': '75.00',
    'Mixed green salad with lean protein': '65.00',
    'Steamed fish with vegetables': '85.00',
    'Greek yogurt with nuts': '60.00',
    'Baked chicken and sweet potato': '75.00',
    'Tuna and cucumber rice bowl': '55.00',
    'Tofu and vegetable stir-fry': '50.00',
    'Chicken arroz caldo': '45.00',
}


def expand_catalog(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')
    ExerciseItem = apps.get_model('info', 'ExerciseItem')

    for name, price in PRICE_UPDATES.items():
        FoodItem.objects.filter(name=name).update(estimated_cost=Decimal(price))

    for row in FOODS:
        name, description, ingredients, preparation, meal, category, calories, price, allergens = row
        FoodItem.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'ingredients': ingredients,
                'preparation_details': preparation,
                'meal_type': meal,
                'food_category': category,
                'calories': calories,
                'estimated_cost': Decimal(price),
                'weight_status': 'all',
                'conditions': ['all'],
                'allergens': allergens,
            },
        )

    for row in EXERCISES:
        name, description, intensity, location, duration, min_age, max_age, avoid_conditions = row
        ExerciseItem.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'intensity': intensity,
                'location': location,
                'duration_minutes': duration,
                'weight_status': 'all',
                'min_age': min_age,
                'max_age': max_age,
                'conditions': ['all'],
                'avoid_conditions': avoid_conditions,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_healthprofile_food_budget_period'),
    ]

    operations = [
        migrations.RunPython(expand_catalog, migrations.RunPython.noop),
    ]
