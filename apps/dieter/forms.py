from django import forms
from django.core.exceptions import ValidationError

from apps.dieter.models import FoodBudgetPeriod
from apps.info.models import (
    ExerciseItem,
    FoodItem,
    HealthCondition,
    HealthProfile,
    HealthStatus,
)


class HealthProfileForm(forms.ModelForm):
    YES_NO_CHOICES = [('', 'Choose an option'), ('yes', 'Yes'), ('no', 'No')]

    drinks_alcohol = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you drink alcohol?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    alcohol_frequency = forms.ChoiceField(
        choices=[
            ('', 'Choose frequency'),
            ('monthly_or_less', 'Once a month or less'),
            ('two_to_four_monthly', '2–4 times a month'),
            ('one_to_three_weekly', '1–3 times a week'),
            ('four_plus_weekly', '4 or more times a week'),
        ],
        required=False,
        label='How often do you drink?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    smokes = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you smoke?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    smoking_frequency = forms.ChoiceField(
        choices=[
            ('', 'Choose frequency'),
            ('former', 'Former smoker'),
            ('less_than_daily', 'Less than daily'),
            ('one_to_five_daily', '1–5 times a day'),
            ('six_to_ten_daily', '6–10 times a day'),
            ('eleven_plus_daily', '11 or more times a day'),
        ],
        required=False,
        label='How often do you smoke?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    has_diabetes = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have diabetes or prediabetes?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    diabetes_status = forms.ChoiceField(
        choices=[
            ('', 'Choose an option'),
            ('type_1', 'Type 1 diabetes'),
            ('type_2', 'Type 2 diabetes'),
            ('prediabetes', 'Prediabetes'),
            ('gestational', 'Gestational diabetes'),
            ('unspecified', 'Diabetes type not specified'),
        ],
        required=False,
        label='Diabetes',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    has_high_blood_pressure = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have high blood pressure?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    blood_pressure_status = forms.ChoiceField(
        choices=[
            ('', 'Choose an option'),
            ('managed', 'High blood pressure, managed'),
            ('unmanaged_or_unsure', 'High blood pressure, not managed or unsure'),
        ],
        required=False,
        label='High blood pressure',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    has_asthma = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have asthma?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    asthma_status = forms.ChoiceField(
        choices=[
            ('', 'Choose an option'),
            ('intermittent', 'Intermittent'),
            ('mild_persistent', 'Mild persistent'),
            ('moderate_persistent', 'Moderate persistent'),
            ('severe_or_unsure', 'Severe or unsure'),
        ],
        required=False,
        label='Asthma',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    has_heart_condition = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have a heart condition?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    heart_condition_status = forms.ChoiceField(
        choices=[
            ('', 'Choose an option'),
            ('arrhythmia', 'Arrhythmia'),
            ('coronary', 'Coronary artery condition'),
            ('heart_failure', 'Heart failure'),
            ('congenital', 'Congenital heart condition'),
            ('other_or_unsure', 'Other or unsure'),
        ],
        required=False,
        label='Heart condition',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    heart_condition_details = forms.CharField(
        required=False,
        max_length=500,
        label='Please specify the heart condition',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'maxlength': 500,
            'placeholder': 'Optional details about the other heart condition',
        }),
    )
    sleep_deprived = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you often have trouble getting enough sleep?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    sleep_deprivation_frequency = forms.ChoiceField(
        choices=[
            ('', 'Choose frequency'),
            ('one_to_two_weekly', '1–2 nights a week'),
            ('three_to_four_weekly', '3–4 nights a week'),
            ('five_plus_weekly', '5 or more nights a week'),
        ],
        required=False,
        label='How often do you have trouble getting enough sleep?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    has_other_allergies = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have any other allergies?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    other_allergy_types = forms.MultipleChoiceField(
        choices=[
            ('seasonal', 'Seasonal or pollen'),
            ('medication', 'Medication'),
            ('insect', 'Insect sting or bite'),
            ('latex', 'Latex'),
            ('skin_contact', 'Skin or contact'),
            ('other', 'Other or not listed'),
        ],
        required=False,
        label='Other allergies (select all that apply)',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
    )
    other_allergy_details = forms.CharField(
        required=False,
        max_length=500,
        label='Please specify the other allergy',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'maxlength': 500,
            'placeholder': 'Optional details about the other allergy',
        }),
    )
    physical_health = forms.ChoiceField(
        choices=[
            ('', 'Choose an option'),
            ('yes', 'Yes, I have a physical concern'),
            ('no', 'No, I am physically healthy'),
        ],
        required=False,
        label='Do you have an injury or physical condition affecting your bones, joints, or mobility?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    injury_options = forms.MultipleChoiceField(
        choices=[
            ('recent_injury', 'Recent or ongoing injury'),
            ('bone_condition', 'Bone condition or previous fracture'),
            ('joint_condition', 'Joint pain or condition'),
            ('mobility_limitation', 'Mobility limitation'),
            ('other', 'Other physical concern'),
        ],
        required=False,
        label='Injury or bone/joint concerns (select all that apply)',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
    )
    has_food_allergies = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        label='Do you have any food allergies?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    food_allergy_options = forms.MultipleChoiceField(
        choices=[
            ('peanuts', 'Peanuts'),
            ('tree_nuts', 'Tree nuts'),
            ('milk', 'Milk'),
            ('eggs', 'Eggs'),
            ('wheat', 'Wheat'),
            ('soy', 'Soy'),
            ('fish', 'Fish'),
            ('shellfish', 'Shellfish'),
            ('sesame', 'Sesame'),
            ('other', 'Other or not listed'),
        ],
        required=False,
        label='Food allergies (select all that apply)',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
    )
    food_preference = forms.ChoiceField(
        choices=[
            ('', 'Choose a food goal'),
            ('balanced', 'Balanced meal plan'),
            ('high_protein', 'High protein'),
            ('low_calorie', 'Low calorie / lighter meals'),
            ('high_fiber', 'High fiber'),
            ('vegetarian', 'Vegetarian / plant-based'),
            ('easy_digest', 'Easy to digest'),
        ],
        required=False,
        label='What type of food do you prefer most?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    exercise_intensity = forms.ChoiceField(
        choices=[
            ('', 'Choose an exercise intensity'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
        ],
        required=False,
        label='What exercise intensity do you prefer?',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    food_budget_period = forms.ChoiceField(
        choices=FoodBudgetPeriod.choices,
        required=False,
        label='Budget period',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    STATUS_FIELD_NAMES = (
        'drinks_alcohol',
        'alcohol_frequency',
        'smokes',
        'smoking_frequency',
        'has_diabetes',
        'diabetes_status',
        'has_high_blood_pressure',
        'blood_pressure_status',
        'has_asthma',
        'asthma_status',
        'has_heart_condition',
        'heart_condition_status',
        'heart_condition_details',
        'sleep_deprived',
        'sleep_deprivation_frequency',
        'has_other_allergies',
        'other_allergy_types',
        'other_allergy_details',
        'physical_health',
        'injury_options',
        'has_food_allergies',
        'food_allergy_options',
        'food_preference',
        'exercise_intensity',
    )
    HEALTH_STATUS_SECTIONS = (
        ('drinks_alcohol', 'alcohol_frequency'),
        ('smokes', 'smoking_frequency'),
        ('has_diabetes', 'diabetes_status'),
        ('has_high_blood_pressure', 'blood_pressure_status'),
        ('has_asthma', 'asthma_status'),
        ('has_heart_condition', 'heart_condition_status'),
        ('sleep_deprived', 'sleep_deprivation_frequency'),
        ('has_other_allergies', 'other_allergy_types'),
        ('physical_health', 'injury_options'),
        ('has_food_allergies', 'food_allergy_options'),
    )

    class Meta:
        model = HealthProfile
        fields = [
            'age',
            'height_cm',
            'weight_kg',
            'daily_food_budget',
            'food_budget_period',
            'drinks_alcohol',
            'alcohol_frequency',
            'smokes',
            'smoking_frequency',
            'has_diabetes',
            'diabetes_status',
            'has_high_blood_pressure',
            'blood_pressure_status',
            'has_asthma',
            'asthma_status',
            'has_heart_condition',
            'heart_condition_status',
            'sleep_deprived',
            'sleep_deprivation_frequency',
            'has_other_allergies',
            'other_allergy_types',
            'physical_health',
            'injury_options',
            'has_food_allergies',
            'food_allergy_options',
            'food_preference',
            'exercise_intensity',
        ]
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 100}),
            'height_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 80,
                'max': 250,
                'step': '0.1',
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 20,
                'max': 300,
                'step': '0.1',
            }),
            'daily_food_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100000,
                'step': '0.01',
                'placeholder': 'Optional',
            }),
        }
        labels = {
            'age': 'Age (years)',
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',
            'daily_food_budget': 'Food budget (₱)',
        }

    @property
    def health_status_fields(self):
        return [self[name] for name in self.STATUS_FIELD_NAMES]

    @property
    def health_status_sections(self):
        return [
            {
                'parent': self[parent],
                'child': self[child],
                'parent_value': 'yes',
            }
            for parent, child in self.HEALTH_STATUS_SECTIONS
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            answers = self.instance.health_status_answers or {}
            parent_fields = {parent for parent, _ in self.HEALTH_STATUS_SECTIONS}
            for name in self.STATUS_FIELD_NAMES:
                if name not in answers:
                    continue
                value = answers[name]
                if name == 'physical_health':
                    if value == 'healthy':
                        value = 'no'
                    elif value in ('injury', 'bone', 'joint', 'mobility'):
                        value = 'yes'
                if name in parent_fields and value not in ('yes', 'no', ''):
                    continue
                if isinstance(self.fields[name], forms.MultipleChoiceField):
                    available_values = {choice[0] for choice in self.fields[name].choices}
                    value = [item for item in value if item in available_values]
                elif isinstance(self.fields[name], forms.ChoiceField):
                    available_values = {choice[0] for choice in self.fields[name].choices}
                    if value not in available_values:
                        legacy_none_values = {
                            'alcohol_frequency': 'never',
                            'smoking_frequency': 'never',
                            'diabetes_status': 'none',
                            'blood_pressure_status': 'none',
                            'asthma_status': 'none',
                            'heart_condition_status': 'none',
                            'sleep_deprivation_frequency': 'never',
                        }
                        if legacy_none_values.get(name) == value:
                            parent = dict((child, parent) for parent, child in self.HEALTH_STATUS_SECTIONS).get(name)
                            if parent:
                                self.initial[parent] = 'no'
                            continue
                        continue
                self.initial[name] = value
            self._set_legacy_initial_values()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('food_budget_period'):
            cleaned_data['food_budget_period'] = FoodBudgetPeriod.DAILY
        for parent, child in self.HEALTH_STATUS_SECTIONS:
            if cleaned_data.get(parent) != 'yes':
                cleaned_data[child] = [] if isinstance(self.fields[child], forms.MultipleChoiceField) else ''
                continue
            if not cleaned_data.get(child):
                self.add_error(child, 'Choose at least one applicable option.')
        if cleaned_data.get('heart_condition_status') != 'other_or_unsure':
            cleaned_data['heart_condition_details'] = ''
        if 'other' not in cleaned_data.get('other_allergy_types', []):
            cleaned_data['other_allergy_details'] = ''
        return cleaned_data

    def _set_legacy_initial_values(self):
        legacy_statuses = set(self.instance.health_status or [])
        answers = self.instance.health_status_answers or {}
        legacy_choices = {
            'alcohol_frequency': (HealthStatus.ALCOHOL, 'unspecified'),
            'smoking_frequency': (HealthStatus.SMOKING, 'unspecified'),
            'diabetes_status': (HealthStatus.DIABETES, 'unspecified'),
            'blood_pressure_status': (HealthStatus.HYPERTENSION, 'unmanaged_or_unsure'),
            'asthma_status': (HealthStatus.ASTHMA, 'severe_or_unsure'),
            'heart_condition_status': (HealthStatus.HEART, 'other_or_unsure'),
        }
        for field, (status, legacy_value) in legacy_choices.items():
            if status in legacy_statuses and not answers.get(field):
                choices = dict(self.fields[field].choices)
                choices[legacy_value] = 'Previously recorded (details not specified)'
                self.fields[field].choices = list(choices.items())
                self.initial[field] = legacy_value
        parent_for_status = {
            HealthStatus.ALCOHOL: 'drinks_alcohol',
            HealthStatus.SMOKING: 'smokes',
            HealthStatus.DIABETES: 'has_diabetes',
            HealthStatus.HYPERTENSION: 'has_high_blood_pressure',
            HealthStatus.ASTHMA: 'has_asthma',
            HealthStatus.HEART: 'has_heart_condition',
            HealthStatus.ALLERGIES: 'has_other_allergies',
            HealthStatus.SLEEP_DEPRIVATION: 'sleep_deprived',
            HealthStatus.FOOD_ALLERGY: 'has_food_allergies',
        }
        for status, parent in parent_for_status.items():
            if status in legacy_statuses and parent not in answers:
                self.initial[parent] = 'yes'
        if (
            HealthStatus.INJURY in legacy_statuses
            and answers.get('physical_health') not in ('yes', 'no')
        ):
            self.initial['physical_health'] = 'yes'
            if not answers.get('injury_options'):
                self.initial['injury_options'] = ['other']
        elif (
            HealthStatus.PHYSICALLY_HEALTHY in legacy_statuses
            and answers.get('physical_health') not in ('yes', 'no')
        ):
            self.initial['physical_health'] = 'no'
        if not answers.get('other_allergy_types') and HealthStatus.ALLERGIES in legacy_statuses:
            self.initial['other_allergy_types'] = ['other']
        if not answers.get('food_allergy_options') and HealthStatus.FOOD_ALLERGY in legacy_statuses:
            self.initial['food_allergy_options'] = ['other']

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data
        answers = {
            name: cleaned_data[name]
            for name in self.STATUS_FIELD_NAMES
        }
        statuses = []
        if answers['drinks_alcohol'] == 'yes':
            statuses.append(HealthStatus.ALCOHOL)
        if answers['smokes'] == 'yes':
            statuses.append(HealthStatus.SMOKING)
        if answers['has_diabetes'] == 'yes':
            statuses.append(HealthStatus.DIABETES)
        if answers['has_high_blood_pressure'] == 'yes':
            statuses.append(HealthStatus.HYPERTENSION)
        if answers['has_asthma'] == 'yes':
            statuses.append(HealthStatus.ASTHMA)
        if answers['has_heart_condition'] == 'yes':
            statuses.append(HealthStatus.HEART)
        if answers['has_other_allergies'] == 'yes':
            statuses.append(HealthStatus.ALLERGIES)
        if answers['sleep_deprived'] == 'yes':
            statuses.append(HealthStatus.SLEEP_DEPRIVATION)
        if answers['physical_health'] == 'no':
            statuses.append(HealthStatus.PHYSICALLY_HEALTHY)
        elif answers['physical_health'] == 'yes':
            statuses.append(HealthStatus.INJURY)
        if answers['has_food_allergies'] == 'yes':
            statuses.append(HealthStatus.FOOD_ALLERGY)

        instance.health_status = statuses
        instance.health_status_answers = answers
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class FoodItemForm(forms.ModelForm):
    conditions = forms.MultipleChoiceField(
        choices=[('all', 'All statuses and conditions'), *HealthCondition.choices],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    allergens = forms.CharField(
        required=False,
        label='Known allergens (comma separated)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: peanuts, dairy',
        }),
    )

    class Meta:
        model = FoodItem
        fields = [
            'name',
            'description',
            'ingredients',
            'preparation_details',
            'meal_type',
            'food_category',
            'calories',
            'estimated_cost',
            'weight_status',
            'conditions',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 120}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'preparation_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'food_category': forms.Select(attrs={'class': 'form-select'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estimated_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Estimated ₱ per serving',
            }),
            'weight_status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'description': 'Detailed description',
            'estimated_cost': 'Estimated cost per serving (₱)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.is_bound:
            self.initial['allergens'] = ', '.join(self.instance.allergens or [])

    def clean_allergens(self):
        return [
            allergen.strip()
            for allergen in self.cleaned_data['allergens'].split(',')
            if allergen.strip()
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.allergens = self.cleaned_data['allergens']
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ExerciseItemForm(forms.ModelForm):
    conditions = forms.MultipleChoiceField(
        choices=[('all', 'All statuses and conditions'), *HealthCondition.choices],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    avoid_conditions = forms.MultipleChoiceField(
        choices=HealthCondition.choices[1:],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Conditions that should avoid this exercise',
    )

    class Meta:
        model = ExerciseItem
        fields = [
            'name',
            'description',
            'intensity',
            'location',
            'duration_minutes',
            'weight_status',
            'min_age',
            'max_age',
            'conditions',
            'avoid_conditions',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 120}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'intensity': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'weight_status': forms.Select(attrs={'class': 'form-select'}),
            'min_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 10}),
            'max_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('min_age') and cleaned_data.get('max_age'):
            if cleaned_data['min_age'] > cleaned_data['max_age']:
                self.add_error('max_age', 'Maximum age cannot be less than minimum age.')
        return cleaned_data


class ExerciseImportForm(forms.Form):
    file = forms.FileField(
        label='Exercise CSV file',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv,text/csv'}),
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if uploaded_file.size > 2 * 1024 * 1024:
            raise ValidationError('The CSV file must be 2 MB or smaller.')
        return uploaded_file
