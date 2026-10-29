from decimal import Decimal

from django.db import migrations


SAMPLE_FOOD_PRICES = {
    'Oatmeal with berries': '40.00',
    'Vegetable omelet': '50.00',
    'Baked salmon with vegetables': '180.00',
    'Grilled chicken salad': '90.00',
    'Lentil and vegetable soup': '55.00',
    'Apple with unsalted nuts': '45.00',
}


def estimate_current_food_prices(apps, schema_editor):
    FoodItem = apps.get_model('info', 'FoodItem')
    for name, price in SAMPLE_FOOD_PRICES.items():
        FoodItem.objects.filter(
            name=name,
            estimated_cost__isnull=True,
        ).update(estimated_cost=Decimal(price))


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0007_seed_sample_food_details'),
    ]

    operations = [
        migrations.RunPython(estimate_current_food_prices, migrations.RunPython.noop),
    ]
