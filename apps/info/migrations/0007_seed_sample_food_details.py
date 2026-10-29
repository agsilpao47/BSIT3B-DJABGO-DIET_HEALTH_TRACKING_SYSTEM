from decimal import Decimal

from django.db import migrations


SAMPLE_FOOD_DETAILS = {
    'Oatmeal with fruit': (
        '35.00',
        'Rolled oats, water or milk, and one seasonal fruit.',
        'Simmer the oats until soft, then top with sliced fruit. Use water or an allergy-safe milk alternative when needed.',
        ['milk'],
    ),
    'Peanut butter banana toast': (
        '30.00',
        'Whole-grain bread, peanut butter, and banana.',
        'Toast the bread, spread with peanut butter, and top with banana slices. Substitute only with an allergy-safe spread.',
        ['peanuts', 'wheat'],
    ),
    'Avocado and egg sandwich': (
        '55.00',
        'Whole-grain bread, egg, avocado, and optional leafy greens.',
        'Cook the egg thoroughly, mash the avocado, and assemble with the bread and greens.',
        ['eggs', 'wheat'],
    ),
    'Grilled chicken with brown rice': (
        '95.00',
        'Skinless chicken breast, brown rice, and mixed vegetables.',
        'Grill the chicken until fully cooked, steam the vegetables, and serve with cooked brown rice.',
        [],
    ),
    'Mixed green salad with lean protein': (
        '85.00',
        'Leafy greens, cucumber, tomato, and grilled chicken or beans.',
        'Wash produce thoroughly, add cooked protein, and dress lightly just before serving.',
        [],
    ),
    'Steamed fish with vegetables': (
        '110.00',
        'Fresh fish, leafy vegetables, ginger, and calamansi.',
        'Steam the fish until fully cooked, steam vegetables separately, and season modestly.',
        ['fish'],
    ),
    'Rice, beans, and vegetables': (
        '45.00',
        'Rice, cooked beans, and seasonal vegetables.',
        'Cook rice and beans until tender, then serve with steamed or sautéed vegetables.',
        [],
    ),
    'Greek yogurt with nuts': (
        '65.00',
        'Plain Greek yogurt, a small portion of mixed nuts, and optional fruit.',
        'Serve chilled and add nuts immediately before eating. Use only if both dairy and nut ingredients are safe.',
        ['milk', 'tree nuts'],
    ),
    'Apple slices with almonds': (
        '40.00',
        'One apple and a small portion of almonds.',
        'Wash and slice the apple; serve with almonds on the side to make ingredients easy to identify.',
        ['tree nuts'],
    ),
    'Vegetable soup': (
        '50.00',
        'Seasonal vegetables, onion, garlic, and low-sodium broth.',
        'Simmer chopped vegetables in broth until tender. Blend part of the soup for a thicker texture if desired.',
        [],
    ),
    'Milk banana smoothie': (
        '35.00',
        'Banana, milk, and optional plain oats.',
        'Blend until smooth and serve immediately. Check the milk and any optional additions for allergens.',
        ['milk'],
    ),
    'Baked chicken and sweet potato': (
        '90.00',
        'Skinless chicken, sweet potato, and seasonal vegetables.',
        'Bake the chicken and sweet potato until tender and fully cooked, then serve with steamed vegetables.',
        [],
    ),
}


def populate_sample_food_details(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')
    for name, details in SAMPLE_FOOD_DETAILS.items():
        cost, ingredients, preparation_details, allergens = details
        for food in FoodItem.objects.filter(name=name):
            update_fields = []
            if food.estimated_cost is None:
                food.estimated_cost = Decimal(cost)
                update_fields.append('estimated_cost')
            if not food.ingredients:
                food.ingredients = ingredients
                update_fields.append('ingredients')
            if not food.preparation_details:
                food.preparation_details = preparation_details
                update_fields.append('preparation_details')
            if not food.allergens:
                food.allergens = allergens
                update_fields.append('allergens')
            if update_fields:
                food.save(update_fields=update_fields)


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_fooditem_estimated_cost_fooditem_ingredients_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_sample_food_details, migrations.RunPython.noop),
    ]
