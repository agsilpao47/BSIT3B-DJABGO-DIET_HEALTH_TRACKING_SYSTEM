from decimal import Decimal

from django.db import migrations


FOODS = [
    {
        'name': 'Banana cinnamon overnight oats',
        'description': 'A simple plant-based breakfast of oats and banana prepared ahead for a quick meal.',
        'ingredients': 'Rolled oats, banana, water or an allergy-safe plant drink, and cinnamon.',
        'preparation_details': 'Mix oats with water or a suitable plant drink, chill overnight, then top with sliced banana and cinnamon.',
        'meal_type': 'breakfast',
        'food_category': 'mixed',
        'calories': 290,
        'estimated_cost': Decimal('30.00'),
        'allergens': [],
    },
    {
        'name': 'Tofu and spinach breakfast bowl',
        'description': 'A savory plant-based breakfast with tofu, spinach, and rice.',
        'ingredients': 'Tofu, spinach, cooked rice, garlic, and a small amount of cooking oil.',
        'preparation_details': 'Cook tofu thoroughly with garlic, wilt washed spinach, and serve with warm rice.',
        'meal_type': 'breakfast',
        'food_category': 'mixed',
        'calories': 340,
        'estimated_cost': Decimal('40.00'),
        'allergens': ['soy'],
    },
    {
        'name': 'Avocado tomato toast',
        'description': 'A quick plant-based breakfast with avocado and fresh tomato on toast.',
        'ingredients': 'Whole-grain bread, avocado, tomato, and calamansi.',
        'preparation_details': 'Toast the bread, mash the avocado with calamansi, and top with washed tomato slices.',
        'meal_type': 'breakfast',
        'food_category': 'mixed',
        'calories': 310,
        'estimated_cost': Decimal('45.00'),
        'allergens': ['wheat'],
    },
    {
        'name': 'Chickpea and cucumber rice bowl',
        'description': 'A filling plant-based lunch with chickpeas, crisp vegetables, and rice.',
        'ingredients': 'Cooked chickpeas, cucumber, tomato, rice, and calamansi.',
        'preparation_details': 'Rinse cooked chickpeas, wash and chop vegetables, then serve together with rice.',
        'meal_type': 'lunch',
        'food_category': 'mixed',
        'calories': 420,
        'estimated_cost': Decimal('45.00'),
        'allergens': [],
    },
    {
        'name': 'Tofu vegetable rice stir-fry',
        'description': 'A plant-based rice meal with tofu and mixed vegetables.',
        'ingredients': 'Tofu, cooked rice, carrots, cabbage, garlic, and a small amount of cooking oil.',
        'preparation_details': 'Cook tofu thoroughly, stir-fry with washed vegetables, and fold through warm rice.',
        'meal_type': 'lunch',
        'food_category': 'mixed',
        'calories': 430,
        'estimated_cost': Decimal('50.00'),
        'allergens': ['soy'],
    },
    {
        'name': 'Black bean and sweet potato plate',
        'description': 'A hearty plant-based plate pairing black beans with soft sweet potato.',
        'ingredients': 'Cooked black beans, sweet potato, tomato, and garlic.',
        'preparation_details': 'Bake or steam sweet potato until tender and serve with thoroughly cooked beans and tomato.',
        'meal_type': 'lunch',
        'food_category': 'mixed',
        'calories': 390,
        'estimated_cost': Decimal('40.00'),
        'allergens': [],
    },
    {
        'name': 'Lentil vegetable soup',
        'description': 'A warm plant-based soup with lentils and vegetables.',
        'ingredients': 'Lentils, carrots, tomato, onion, garlic, and water.',
        'preparation_details': 'Simmer rinsed lentils with chopped vegetables until everything is tender.',
        'meal_type': 'dinner',
        'food_category': 'mixed',
        'calories': 360,
        'estimated_cost': Decimal('40.00'),
        'allergens': [],
    },
    {
        'name': 'Vegetable and tofu rice noodles',
        'description': 'A plant-based noodle dish with tofu and mixed vegetables.',
        'ingredients': 'Rice noodles, tofu, cabbage, carrots, garlic, and a small amount of cooking oil.',
        'preparation_details': 'Soften rice noodles, cook tofu thoroughly, and toss with washed vegetables until tender.',
        'meal_type': 'dinner',
        'food_category': 'mixed',
        'calories': 410,
        'estimated_cost': Decimal('50.00'),
        'allergens': ['soy'],
    },
    {
        'name': 'Fresh papaya and banana snack',
        'description': 'A refreshing plant-based snack of fresh fruit with no added sugar.',
        'ingredients': 'Ripe papaya and banana.',
        'preparation_details': 'Wash fruit, peel, cut with clean utensils, and serve fresh.',
        'meal_type': 'snack',
        'food_category': 'fruit',
        'calories': 130,
        'estimated_cost': Decimal('25.00'),
        'allergens': [],
    },
    {
        'name': 'Baked potato with tomato salsa',
        'description': 'A simple plant-based snack of baked potato with fresh tomato salsa.',
        'ingredients': 'Potato, tomato, onion, and calamansi.',
        'preparation_details': 'Bake or steam the potato until tender and serve with washed, chopped tomato and onion.',
        'meal_type': 'snack',
        'food_category': 'vegetable',
        'calories': 210,
        'estimated_cost': Decimal('25.00'),
        'allergens': [],
    },
]


def add_vegetarian_foods(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')

    for food in FOODS:
        FoodItem.objects.get_or_create(
            name=food['name'],
            defaults={
                **food,
                'weight_status': 'all',
                'conditions': ['all'],
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0012_expand_food_and_exercise_catalog'),
    ]

    operations = [
        migrations.RunPython(add_vegetarian_foods, migrations.RunPython.noop),
    ]
