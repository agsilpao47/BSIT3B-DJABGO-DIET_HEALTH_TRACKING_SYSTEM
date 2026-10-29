import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DietMealLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=120)),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')], max_length=20)),
                ('calories', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6000)])),
                ('logged_on', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_meals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_diet_meal_log',
                'ordering': ['meal_type', 'food_name'],
                'indexes': [models.Index(fields=['user', 'logged_on'], name='diet_meal_user_date_idx')],
            },
        ),
    ]
