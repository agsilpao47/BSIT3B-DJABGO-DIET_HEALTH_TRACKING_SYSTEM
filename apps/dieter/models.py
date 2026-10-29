"""Health and diet data models."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from decimal import Decimal


class WeightStatus(models.TextChoices):
    UNDERWEIGHT = 'underweight', 'Underweight'
    NORMAL = 'normal', 'Normal'
    OVERWEIGHT = 'overweight', 'Overweight'
    ALL = 'all', 'All statuses'


class HealthCondition(models.TextChoices):
    NONE = 'none', 'None'
    DIABETES = 'diabetes', 'Diabetes'
    HYPERTENSION = 'hypertension', 'Hypertension'
    ASTHMA = 'asthma', 'Asthma'
    HEART = 'heart', 'Heart condition'


class HealthStatus(models.TextChoices):
    NONE = 'none', 'None apply'
    PHYSICALLY_HEALTHY = 'physically_healthy', 'Physically healthy (no injury or bone/joint concern)'
    ALCOHOL = 'alcohol', 'I drink alcohol'
    SMOKING = 'smoking', 'I smoke'
    DIABETES = 'diabetes', 'Diabetes'
    HYPERTENSION = 'hypertension', 'High blood pressure'
    ASTHMA = 'asthma', 'Asthma'
    HEART = 'heart', 'Heart condition'
    ALLERGIES = 'allergies', 'Other allergies'
    SLEEP_DEPRIVATION = 'sleep_deprivation', 'Sleep deprivation'
    INJURY = 'injury', 'Injury or condition affecting bones or joints'
    FOOD_ALLERGY = 'food_allergy', 'Food allergy'


class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH = 'lunch', 'Lunch'
    DINNER = 'dinner', 'Dinner'
    SNACK = 'snack', 'Snack'


class FoodCategory(models.TextChoices):
    FRUIT = 'fruit', 'Fruit'
    VEGETABLE = 'vegetable', 'Vegetables'
    GRAIN = 'grain', 'Grains'
    PROTEIN = 'protein', 'Protein'
    DAIRY = 'dairy', 'Dairy'
    MIXED = 'mixed', 'Mixed meal'
    OTHER = 'other', 'Other'


class Intensity(models.TextChoices):
    LOW = 'low', 'Low'
    MODERATE = 'moderate', 'Moderate'
    HIGH = 'high', 'High'


class ExerciseLocation(models.TextChoices):
    INDOOR = 'indoor', 'Indoor'
    OUTDOOR = 'outdoor', 'Outdoor'
    BOTH = 'both', 'Indoor or outdoor'


class FoodBudgetPeriod(models.TextChoices):
    DAILY = 'daily', 'Daily'
    MONTHLY = 'monthly', 'Monthly'


class HealthProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='health_profile',
        on_delete=models.CASCADE,
    )
    age = models.PositiveIntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(80), MaxValueValidator(250)],
    )
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(20), MaxValueValidator(300)],
    )
    daily_food_budget = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100000)],
    )
    food_budget_period = models.CharField(
        max_length=10,
        choices=FoodBudgetPeriod.choices,
        default=FoodBudgetPeriod.DAILY,
    )
    health_status = models.JSONField(default=list, blank=True)
    health_status_answers = models.JSONField(default=dict, blank=True)
    health_status_details = models.TextField(blank=True)
    injury_details = models.TextField(blank=True)
    food_allergy_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'info'
        db_table = 'tbl_health_profile'

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def height_m(self):
        return float(self.height_cm) / 100

    @property
    def bmi(self):
        height_m = self.height_m
        if height_m <= 0:
            return 0
        return round(float(self.weight_kg) / (height_m * height_m), 1)

    @property
    def status(self):
        value = self.bmi
        if value < 18.5:
            return WeightStatus.UNDERWEIGHT
        if value < 25:
            return WeightStatus.NORMAL
        return WeightStatus.OVERWEIGHT

    @property
    def status_label(self):
        if self.bmi >= 30:
            return 'Obese'
        return WeightStatus(self.status).label

    @property
    def bmi_indicator_percent(self):
        return max(0, min(100, (self.bmi - 10) / 30 * 100))

    @property
    def food_preference(self):
        return (self.health_status_answers or {}).get('food_preference') or 'balanced'

    @property
    def exercise_intensity(self):
        return (self.health_status_answers or {}).get('exercise_intensity') or 'moderate'

    @property
    def daily_food_budget_limit(self):
        if self.daily_food_budget is None:
            return None
        if self.food_budget_period == FoodBudgetPeriod.MONTHLY:
            return self.daily_food_budget / Decimal('30')
        return self.daily_food_budget

    @property
    def health_status_labels(self):
        labels = dict(HealthStatus.choices)
        answers = self.health_status_answers or {}
        detailed_status_fields = {
            HealthStatus.SMOKING: 'smoking_frequency',
            HealthStatus.HYPERTENSION: 'blood_pressure_status',
            HealthStatus.HEART: 'heart_condition_status',
            HealthStatus.ALLERGIES: 'other_allergy_types',
            HealthStatus.FOOD_ALLERGY: 'food_allergy_options',
        }
        status_labels = [
            labels[value]
            for value in self.health_status
            if value in labels
            and not answers.get(detailed_status_fields.get(value, ''))
        ]
        answer_labels = {
            'alcohol_frequency': 'Alcohol: ',
            'smoking_frequency': 'Smoking: ',
            'diabetes_status': 'Diabetes: ',
            'blood_pressure_status': 'Blood pressure: ',
            'asthma_status': 'Asthma: ',
            'heart_condition_status': 'Heart condition: ',
            'sleep_deprivation_frequency': 'Sleep deprivation: ',
        }
        option_labels = {
            'alcohol_frequency': {
                'never': 'Never',
                'monthly_or_less': 'Once a month or less',
                'two_to_four_monthly': '2–4 times a month',
                'one_to_three_weekly': '1–3 times a week',
                'four_plus_weekly': '4 or more times a week',
            },
            'smoking_frequency': {
                'never': 'Never',
                'former': 'Former smoker',
                'less_than_daily': 'Less than daily',
                'one_to_five_daily': '1–5 times a day',
                'six_to_ten_daily': '6–10 times a day',
                'eleven_plus_daily': '11 or more times a day',
                'unspecified': 'Previously recorded; frequency not specified',
            },
            'diabetes_status': {
                'type_1': 'Type 1',
                'type_2': 'Type 2',
                'prediabetes': 'Prediabetes',
                'gestational': 'Gestational',
                'unspecified': 'Previously recorded; type not specified',
            },
            'blood_pressure_status': {
                'managed': 'Managed',
                'unmanaged_or_unsure': 'Not managed or unsure',
            },
            'asthma_status': {
                'intermittent': 'Intermittent',
                'mild_persistent': 'Mild persistent',
                'moderate_persistent': 'Moderate persistent',
                'severe_or_unsure': 'Severe or unsure',
            },
            'heart_condition_status': {
                'arrhythmia': 'Arrhythmia',
                'coronary': 'Coronary artery condition',
                'heart_failure': 'Heart failure',
                'congenital': 'Congenital heart condition',
                'other_or_unsure': 'Other or unsure',
            },
            'sleep_deprivation_frequency': {
                'never': 'Never or rarely',
                'one_to_two_weekly': '1–2 nights a week',
                'three_to_four_weekly': '3–4 nights a week',
                'five_plus_weekly': '5 or more nights a week',
            },
        }
        for field, prefix in answer_labels.items():
            value = answers.get(field)
            if value:
                label = option_labels.get(field, {}).get(value, value)
                status_labels.append(f'{prefix}{label}')
        heart_details = (answers.get('heart_condition_details') or '').strip()
        if answers.get('heart_condition_status') == 'other_or_unsure' and heart_details:
            status_labels.append(f'Heart condition details: {heart_details}')
        allergy_details = (answers.get('other_allergy_details') or '').strip()
        if 'other' in answers.get('other_allergy_types', []) and allergy_details:
            status_labels.append(f'Other allergy details: {allergy_details}')
        for field, prefix in (
            ('other_allergy_types', 'Allergies: '),
            ('physical_health_options', 'Physical health: '),
            ('injury_options', 'Injuries/bones/joints: '),
            ('food_allergy_options', 'Food allergies: '),
        ):
            values = answers.get(field, [])
            if values:
                value_labels = {
                    'seasonal': 'Seasonal or pollen',
                    'medication': 'Medication',
                    'insect': 'Insect sting or bite',
                    'latex': 'Latex',
                    'skin_contact': 'Skin or contact',
                    'recent_injury': 'Recent or ongoing injury',
                    'bone_condition': 'Bone condition or previous fracture',
                    'joint_condition': 'Joint pain or condition',
                    'mobility_limitation': 'Mobility limitation',
                    'peanuts': 'Peanuts',
                    'tree_nuts': 'Tree nuts',
                    'milk': 'Milk',
                    'eggs': 'Eggs',
                    'wheat': 'Wheat',
                    'soy': 'Soy',
                    'fish': 'Fish',
                    'shellfish': 'Shellfish',
                    'sesame': 'Sesame',
                    'other': 'Other or not listed',
                }
                status_labels.append(
                    f'{prefix}{", ".join(value_labels.get(value, value.replace("_", " ")) for value in values)}'
                )
        return status_labels

    @property
    def recommendation_conditions(self):
        conditions = set(self.health_status or [])
        recommendations = {
            HealthCondition.DIABETES,
            HealthCondition.HYPERTENSION,
            HealthCondition.ASTHMA,
            HealthCondition.HEART,
        }
        matching = conditions.intersection(recommendations)
        return list(matching) or [HealthCondition.NONE]


class FoodItem(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.TextField(blank=True)
    preparation_details = models.TextField(blank=True)
    meal_type = models.CharField(max_length=20, choices=MealType.choices)
    food_category = models.CharField(
        max_length=20,
        choices=FoodCategory.choices,
        default=FoodCategory.OTHER,
    )
    calories = models.PositiveIntegerField()
    estimated_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        help_text='Estimated price per serving in Philippine pesos.',
    )
    weight_status = models.CharField(max_length=20, choices=WeightStatus.choices)
    conditions = models.JSONField(
        default=list,
        blank=True,
        help_text='Suitable conditions, including "none" or "all".',
    )
    allergens = models.JSONField(default=list, blank=True)

    class Meta:
        app_label = 'info'
        db_table = 'tbl_food_item'
        ordering = ['meal_type', 'name']

    def __str__(self):
        return self.name


class ExerciseItem(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    intensity = models.CharField(max_length=20, choices=Intensity.choices)
    location = models.CharField(
        max_length=20,
        choices=ExerciseLocation.choices,
        default=ExerciseLocation.BOTH,
    )
    duration_minutes = models.PositiveIntegerField()
    weight_status = models.CharField(max_length=20, choices=WeightStatus.choices)
    min_age = models.PositiveIntegerField(default=10)
    max_age = models.PositiveIntegerField(default=100)
    conditions = models.JSONField(default=list, blank=True)
    avoid_conditions = models.JSONField(default=list, blank=True)

    class Meta:
        app_label = 'info'
        db_table = 'tbl_exercise_item'
        ordering = ['intensity', 'name']

    def __str__(self):
        return self.name


class DietMealLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='diet_meals',
        on_delete=models.CASCADE,
    )
    food_name = models.CharField(max_length=120)
    meal_type = models.CharField(max_length=20, choices=MealType.choices)
    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6000)],
    )
    logged_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'info'
        db_table = 'tbl_diet_meal_log'
        ordering = ['meal_type', 'food_name']
        indexes = [
            models.Index(fields=['user', 'logged_on'], name='diet_meal_user_date_idx'),
        ]

    def __str__(self):
        return f'{self.food_name} ({self.logged_on})'
