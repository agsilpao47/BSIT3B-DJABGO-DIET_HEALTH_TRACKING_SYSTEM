from django.db import migrations, models


FOOD_GROUPS = {
    'fruit': ('fruit', 'banana', 'mango', 'papaya', 'apple', 'berries', 'berry', 'avocado'),
    'vegetable': ('vegetable', 'spinach', 'cucumber', 'tomato', 'salad', 'leafy', 'carrot', 'cabbage'),
    'grain': ('oat', 'rice', 'bread', 'toast', 'corn', 'whole grain'),
    'protein': ('chicken', 'fish', 'egg', 'tofu', 'lentil', 'bean', 'tuna', 'meat', 'nut'),
    'dairy': ('milk', 'yogurt', 'dairy', 'cheese'),
}


def _food_category(food):
    text = f'{food.name} {food.description} {food.ingredients}'.casefold()
    matches = [
        category
        for category, keywords in FOOD_GROUPS.items()
        if any(keyword in text for keyword in keywords)
    ]
    if len(matches) > 1:
        return 'mixed'
    return matches[0] if matches else 'other'


def _exercise_location(exercise):
    name = exercise.name.casefold()
    if any(keyword in name for keyword in ('indoor', 'seated', 'chair', 'wall', 'stationary')):
        return 'indoor'
    if 'outdoor' in name:
        return 'outdoor'
    return 'both'


def backfill_categories(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')
    ExerciseItem = apps.get_model('info', 'ExerciseItem')

    for food in FoodItem.objects.all().iterator():
        food.food_category = _food_category(food)
        food.save(update_fields=['food_category'])

    for exercise in ExerciseItem.objects.all().iterator():
        exercise.location = _exercise_location(exercise)
        exercise.save(update_fields=['location'])


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_add_more_food_and_exercise_tips'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='food_category',
            field=models.CharField(
                choices=[
                    ('fruit', 'Fruit'),
                    ('vegetable', 'Vegetables'),
                    ('grain', 'Grains'),
                    ('protein', 'Protein'),
                    ('dairy', 'Dairy'),
                    ('mixed', 'Mixed meal'),
                    ('other', 'Other'),
                ],
                default='other',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='exerciseitem',
            name='location',
            field=models.CharField(
                choices=[
                    ('indoor', 'Indoor'),
                    ('outdoor', 'Outdoor'),
                    ('both', 'Indoor or outdoor'),
                ],
                default='both',
                max_length=20,
            ),
        ),
        migrations.RunPython(backfill_categories, migrations.RunPython.noop),
    ]
