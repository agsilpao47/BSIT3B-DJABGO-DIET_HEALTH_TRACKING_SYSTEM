from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import (
    ExerciseItem,
    ExerciseLocation,
    FoodItem,
    FoodBudgetPeriod,
    FoodCategory,
    HealthProfile,
    HealthStatus,
    MealType,
    WeightStatus,
)
from .services import budget_food_plan, foods_for_profile


class DietRecommendationTests(TestCase):
    def setUp(self):
        FoodItem.objects.all().delete()
        ExerciseItem.objects.all().delete()
        self.user = get_user_model().objects.create_user(username='diet-user', password='test-pass')
        self.profile = HealthProfile.objects.create(
            user=self.user,
            age=35,
            height_cm=165,
            weight_kg=80,
            health_status=[HealthStatus.DIABETES],
        )

    def create_food(self, name, weight_status, conditions):
        return FoodItem.objects.create(
            name=name,
            description='General meal idea.',
            meal_type=MealType.LUNCH,
            calories=400,
            weight_status=weight_status,
            conditions=conditions,
        )

    def test_seed_command_loads_expanded_catalog_with_reasonable_prices(self):
        call_command('seed_health', verbosity=0)

        self.assertEqual(FoodItem.objects.count(), 41)
        self.assertEqual(ExerciseItem.objects.count(), 38)
        self.assertEqual(
            FoodItem.objects.get(name='Banana and boiled egg').estimated_cost,
            Decimal('20.00'),
        )
        self.assertEqual(
            FoodItem.objects.get(name='Grilled chicken with brown rice').estimated_cost,
            Decimal('75.00'),
        )
        self.assertTrue(
            ExerciseItem.objects.filter(location=ExerciseLocation.INDOOR).exists()
        )
        self.assertTrue(
            ExerciseItem.objects.filter(location=ExerciseLocation.OUTDOOR).exists()
        )

    def test_adult_recommendations_match_bmi_and_condition(self):
        recommended = self.create_food('Matching meal', WeightStatus.OVERWEIGHT, ['diabetes'])
        self.create_food('Wrong condition', WeightStatus.OVERWEIGHT, ['hypertension'])
        self.create_food('Wrong status', WeightStatus.UNDERWEIGHT, ['diabetes'])

        self.assertEqual(foods_for_profile(self.profile), [recommended])

    def test_under_20_profiles_only_receive_general_weight_status_suggestions(self):
        general = self.create_food('General meal', WeightStatus.ALL, ['all'])
        self.create_food('BMI-specific meal', WeightStatus.OVERWEIGHT, ['all'])
        self.profile.age = 17

        self.assertEqual(foods_for_profile(self.profile), [general])

    def test_budget_plan_uses_cheapest_safe_meals_and_stays_within_budget(self):
        breakfast = self.create_food('Breakfast', WeightStatus.ALL, ['diabetes'])
        breakfast.meal_type = MealType.BREAKFAST
        breakfast.estimated_cost = Decimal('30.00')
        breakfast.save()
        self.create_food('Expensive breakfast', WeightStatus.ALL, ['diabetes'])
        lunch = self.create_food('Lunch', WeightStatus.ALL, ['diabetes'])
        lunch.meal_type = MealType.LUNCH
        lunch.estimated_cost = Decimal('50.00')
        lunch.save()
        dinner = self.create_food('Dinner', WeightStatus.ALL, ['diabetes'])
        dinner.meal_type = MealType.DINNER
        dinner.estimated_cost = Decimal('70.00')
        dinner.save()
        self.profile.daily_food_budget = Decimal('85.00')

        plan = budget_food_plan(self.profile)

        self.assertEqual(plan, [breakfast, lunch])
        self.assertLessEqual(sum((food.estimated_cost for food in plan), Decimal('0')), self.profile.daily_food_budget)

    def test_monthly_food_budget_is_converted_to_daily_allowance(self):
        breakfast = self.create_food('Affordable breakfast', WeightStatus.ALL, ['diabetes'])
        breakfast.meal_type = MealType.BREAKFAST
        breakfast.estimated_cost = Decimal('25.00')
        breakfast.save()
        lunch = self.create_food('Affordable lunch', WeightStatus.ALL, ['diabetes'])
        lunch.meal_type = MealType.LUNCH
        lunch.estimated_cost = Decimal('35.00')
        lunch.save()
        self.create_food('Too costly lunch', WeightStatus.ALL, ['diabetes'])
        self.profile.daily_food_budget = Decimal('1800.00')
        self.profile.food_budget_period = FoodBudgetPeriod.MONTHLY

        plan = budget_food_plan(self.profile)

        self.assertEqual(self.profile.daily_food_budget_limit, Decimal('60.00'))
        self.assertEqual(plan, [breakfast, lunch])
        self.assertLessEqual(sum((food.estimated_cost for food in plan), Decimal('0')), Decimal('60.00'))

    def test_recommendations_require_all_recorded_medical_conditions(self):
        safe_for_both = self.create_food(
            'Suitable for both',
            WeightStatus.OVERWEIGHT,
            ['diabetes', 'hypertension'],
        )
        self.create_food('Only for diabetes', WeightStatus.OVERWEIGHT, ['diabetes'])
        self.profile.health_status = [HealthStatus.DIABETES, HealthStatus.HYPERTENSION]

        self.assertEqual(foods_for_profile(self.profile), [safe_for_both])

class ProfileAndTipsViewTests(TestCase):
    def setUp(self):
        FoodItem.objects.all().delete()
        ExerciseItem.objects.all().delete()
        self.user = get_user_model().objects.create_user(username='profile-user', password='test-pass')
        self.client.force_login(self.user)
        self.profile_data = {
            'age': '28',
            'height_cm': '172',
            'weight_kg': '60',
            'drinks_alcohol': '',
            'alcohol_frequency': '',
            'smokes': '',
            'smoking_frequency': '',
            'has_diabetes': '',
            'diabetes_status': '',
            'has_high_blood_pressure': '',
            'blood_pressure_status': '',
            'has_asthma': '',
            'asthma_status': '',
            'has_heart_condition': '',
            'heart_condition_status': '',
            'sleep_deprived': '',
            'sleep_deprivation_frequency': '',
            'has_other_allergies': '',
            'other_allergy_types': [],
            'physical_health': '',
            'injury_options': [],
            'has_food_allergies': '',
            'food_allergy_options': [],
        }

    def test_dashboard_is_my_profile_and_prompts_for_first_body_details(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Welcome! Add your body details to get started.')
        self.assertContains(response, 'Do you smoke?')
        self.assertContains(response, 'data-condition-parent="id_smokes"')
        self.assertContains(response, 'data-condition-parent="id_physical_health"')
        self.assertContains(response, 'data-condition-parent="id_has_food_allergies"')
        self.assertContains(response, 'data-condition-parent="id_heart_condition_status"')
        self.assertContains(response, 'data-condition-parent="id_other_allergy_types"')
        self.assertContains(response, 'Please specify the heart condition')
        self.assertContains(response, 'Please specify the other allergy')
        self.assertContains(response, 'data-condition-value="other_or_unsure" hidden')
        self.assertContains(response, 'data-condition-value="other" hidden')
        self.assertNotContains(response, 'editProfileModal')
        self.assertContains(response, 'Save body details')
        self.assertNotContains(response, 'Diet Tracker')

    def test_existing_profile_edit_form_opens_in_a_modal(self):
        HealthProfile.objects.create(
            user=self.user,
            age=28,
            height_cm=172,
            weight_kg=60,
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-bs-target="#editProfileModal"')
        self.assertContains(response, 'class="modal fade" id="editProfileModal"')
        self.assertContains(response, 'Edit body details')
        self.assertContains(response, 'data-bs-dismiss="modal">Cancel</button>')
        self.assertContains(response, 'No info about your health status.')
        self.assertContains(response, 'No food budget set.')

    def test_profile_displays_selected_food_budget_period(self):
        self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'daily_food_budget': '1800.00',
            'food_budget_period': FoodBudgetPeriod.MONTHLY,
        })

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'Monthly budget')
        self.assertContains(response, '₱1800.00')
        self.assertContains(response, 'about ₱60.00 per day')

    def test_profile_displays_budget_safe_food_and_exercise_recommendations(self):
        self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'daily_food_budget': '80.00',
        })
        FoodItem.objects.create(
            name='Budget breakfast',
            description='A detailed breakfast description.',
            meal_type=MealType.BREAKFAST,
            calories=250,
            estimated_cost=Decimal('45.00'),
            weight_status=WeightStatus.ALL,
            conditions=['all'],
        )
        ExerciseItem.objects.create(
            name='Profile walk',
            description='An easy walk.',
            intensity='low',
            duration_minutes=20,
            weight_status=WeightStatus.ALL,
            min_age=10,
            max_age=100,
            conditions=['all'],
        )

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'Recommended food')
        self.assertContains(response, 'Budget breakfast')
        self.assertContains(response, '₱80.00')
        self.assertContains(response, 'Recommended exercise')
        self.assertContains(response, 'Profile walk')

    def test_dashboard_saves_status_frequency_and_choice_details(self):
        response = self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'drinks_alcohol': 'yes',
            'alcohol_frequency': 'two_to_four_monthly',
            'smokes': 'yes',
            'smoking_frequency': 'six_to_ten_daily',
            'has_diabetes': 'yes',
            'diabetes_status': 'type_2',
            'has_heart_condition': 'yes',
            'heart_condition_status': 'other_or_unsure',
            'heart_condition_details': 'Cardiomyopathy',
            'has_other_allergies': 'yes',
            'other_allergy_types': ['other'],
            'other_allergy_details': 'Dust mites',
            'physical_health': 'yes',
            'injury_options': ['recent_injury', 'joint_condition'],
            'has_food_allergies': 'yes',
            'food_allergy_options': ['peanuts', 'milk'],
        })

        self.assertRedirects(response, reverse('dashboard'))
        profile = HealthProfile.objects.get(user=self.user)
        self.assertEqual(profile.health_status, [
            HealthStatus.ALCOHOL,
            HealthStatus.SMOKING,
            HealthStatus.DIABETES,
            HealthStatus.HEART,
            HealthStatus.ALLERGIES,
            HealthStatus.INJURY,
            HealthStatus.FOOD_ALLERGY,
        ])
        self.assertEqual(profile.health_status_answers['smoking_frequency'], 'six_to_ten_daily')
        self.assertEqual(profile.health_status_answers['food_allergy_options'], ['peanuts', 'milk'])
        self.assertEqual(profile.health_status_answers['heart_condition_details'], 'Cardiomyopathy')
        self.assertEqual(profile.health_status_answers['other_allergy_details'], 'Dust mites')
        status_labels = profile.health_status_labels
        self.assertNotIn('I smoke', status_labels)
        self.assertNotIn('High blood pressure', status_labels)
        self.assertNotIn('Heart condition', status_labels)
        self.assertNotIn('Other allergies', status_labels)
        self.assertNotIn('Food allergy', status_labels)
        self.assertIn('Injury or condition affecting bones or joints', status_labels)
        self.assertIn('Smoking: 6–10 times a day', status_labels)
        self.assertIn('Food allergies: Peanuts, Milk', status_labels)
        self.assertAlmostEqual(profile.bmi, 20.3, places=1)
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'BMI status')
        self.assertContains(response, '6–10 times a day')
        self.assertContains(response, 'Health status')
        self.assertNotContains(response, '<li>I smoke</li>')
        self.assertContains(response, 'Heart condition details: Cardiomyopathy')
        self.assertContains(response, 'Other allergy details: Dust mites')
        self.assertNotContains(response, 'Food preference: ')
        self.assertContains(response, 'Body model')
        self.assertContains(response, 'Illustrative body model for BMI')
        self.assertContains(response, 'Illustrative body shape based on BMI category only')

    def test_health_status_fields_are_choice_only(self):
        response = self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'sleep_deprived': 'yes',
            'sleep_deprivation_frequency': 'three_to_four_weekly',
            'has_other_allergies': 'yes',
            'other_allergy_types': ['seasonal', 'latex'],
        })

        self.assertRedirects(response, reverse('dashboard'))
        profile = HealthProfile.objects.get(user=self.user)
        self.assertEqual(profile.health_status_answers['other_allergy_types'], ['seasonal', 'latex'])
        self.assertEqual(
            profile.health_status_answers['sleep_deprivation_frequency'],
            'three_to_four_weekly',
        )

    def test_follow_up_choices_are_required_only_when_condition_is_yes(self):
        response = self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'smokes': 'yes',
            'smoking_frequency': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(HealthProfile.objects.filter(user=self.user).exists())
        self.assertContains(response, 'Choose at least one applicable option.')

    def test_no_answer_clears_hidden_follow_up_choices(self):
        response = self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'smokes': 'no',
            'smoking_frequency': 'six_to_ten_daily',
        })

        self.assertRedirects(response, reverse('dashboard'))
        profile = HealthProfile.objects.get(user=self.user)
        self.assertNotIn(HealthStatus.SMOKING, profile.health_status)
        self.assertEqual(profile.health_status_answers['smoking_frequency'], '')

    def test_separate_profile_route_redirects_to_my_profile(self):
        response = self.client.get(reverse('info:profile'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_diet_tracker_route_redirects_to_my_profile(self):
        response = self.client.get(reverse('info:diet'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_food_tips_are_created_and_deleted_by_staff_only(self):
        self.client.post(reverse('dashboard'), {
            **self.profile_data,
        })
        self.user.is_staff = True
        self.user.save(update_fields=['is_staff'])
        food_data = {
            'name': 'Peanut snack',
            'description': 'A small snack.',
            'meal_type': MealType.SNACK,
            'food_category': FoodCategory.FRUIT,
            'calories': 150,
            'weight_status': WeightStatus.ALL,
            'conditions': ['all'],
            'allergens': 'peanuts',
        }

        response = self.client.post(reverse('info:food_create'), food_data)
        food = FoodItem.objects.get(name='Peanut snack')
        self.assertRedirects(response, reverse('info:foods'))
        self.assertEqual(food.allergens, ['peanuts'])
        self.assertEqual(food.food_category, FoodCategory.FRUIT)

        edit_page = self.client.get(reverse('info:food_edit', args=[food.pk]))
        self.assertEqual(edit_page.status_code, 200)
        self.assertContains(edit_page, 'Update food tip')

        edit_response = self.client.post(
            reverse('info:food_edit', args=[food.pk]),
            {
                **food_data,
                'name': 'Updated peanut snack',
                'estimated_cost': '25.50',
                'food_category': FoodCategory.PROTEIN,
                'ingredients': 'Oats and peanuts.',
                'preparation_details': 'Mix and serve.',
            },
        )
        food.refresh_from_db()
        self.assertRedirects(edit_response, reverse('info:foods'))
        self.assertEqual(food.name, 'Updated peanut snack')
        self.assertEqual(food.estimated_cost, Decimal('25.50'))
        self.assertEqual(food.ingredients, 'Oats and peanuts.')
        self.assertEqual(food.food_category, FoodCategory.PROTEIN)

        delete_response = self.client.post(reverse('info:food_delete', args=[food.pk]))
        self.assertRedirects(delete_response, reverse('info:foods'))
        self.assertFalse(FoodItem.objects.filter(pk=food.pk).exists())

    def test_regular_user_cannot_create_food_tips(self):
        response = self.client.post(reverse('info:food_create'), {})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(FoodItem.objects.exists())

    def test_food_tips_exclude_matching_recorded_allergens(self):
        profile = HealthProfile.objects.create(
            user=self.user,
            age=30,
            height_cm=170,
            weight_kg=65,
            health_status_answers={'food_allergy_options': ['peanuts']},
        )
        unsafe_food = FoodItem.objects.create(
            name='Peanut snack',
            description='Contains peanuts.',
            meal_type=MealType.SNACK,
            calories=200,
            weight_status=WeightStatus.ALL,
            conditions=['all'],
            allergens=['peanuts'],
        )
        safe_food = FoodItem.objects.create(
            name='Apple',
            description='Fresh apple.',
            meal_type=MealType.SNACK,
            calories=80,
            weight_status=WeightStatus.ALL,
            conditions=['all'],
            allergens=['apples'],
        )

        self.assertNotIn(unsafe_food, foods_for_profile(profile))
        self.assertIn(safe_food, foods_for_profile(profile))

    def test_food_tips_filter_by_meal_time_and_food_type(self):
        self.client.post(reverse('dashboard'), self.profile_data)
        fruit = FoodItem.objects.create(
            name='Papaya cup',
            description='Fresh fruit.',
            meal_type=MealType.BREAKFAST,
            food_category=FoodCategory.FRUIT,
            calories=100,
            weight_status=WeightStatus.ALL,
            conditions=['all'],
        )
        FoodItem.objects.create(
            name='Vegetable lunch',
            description='A vegetable meal.',
            meal_type=MealType.LUNCH,
            food_category=FoodCategory.VEGETABLE,
            calories=250,
            weight_status=WeightStatus.ALL,
            conditions=['all'],
        )

        response = self.client.get(
            reverse('info:foods'),
            {'meal_type': MealType.BREAKFAST, 'food_category': FoodCategory.FRUIT},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, fruit.name)
        self.assertNotContains(response, 'Vegetable lunch')
        self.assertContains(response, 'All food types')

    def test_all_food_catalog_bypasses_budget_and_profile_matching(self):
        self.client.post(reverse('dashboard'), {
            **self.profile_data,
            'daily_food_budget': '10.00',
        })
        catalog_food = FoodItem.objects.create(
            name='All catalog meal',
            description='Not matched to the user budget or status.',
            meal_type=MealType.DINNER,
            calories=500,
            estimated_cost=Decimal('120.00'),
            weight_status=WeightStatus.UNDERWEIGHT,
            conditions=['diabetes'],
        )

        response = self.client.get(reverse('info:foods'), {'catalog': 'all'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, catalog_food.name)
        self.assertContains(response, 'About ₱120.00 per serving')
        self.assertContains(response, 'regardless of your budget or profile')
        self.assertNotContains(response, 'selected estimated total')

    def test_exercise_tips_filter_by_location_and_include_both_locations(self):
        self.client.post(reverse('dashboard'), self.profile_data)
        ExerciseItem.objects.create(
            name='Indoor stretch',
            description='A gentle stretch.',
            intensity='low',
            location=ExerciseLocation.INDOOR,
            duration_minutes=10,
            weight_status=WeightStatus.ALL,
            min_age=10,
            max_age=100,
            conditions=['all'],
        )
        ExerciseItem.objects.create(
            name='Any-place walk',
            description='A gentle walk.',
            intensity='low',
            location=ExerciseLocation.BOTH,
            duration_minutes=10,
            weight_status=WeightStatus.ALL,
            min_age=10,
            max_age=100,
            conditions=['all'],
        )
        ExerciseItem.objects.create(
            name='Outdoor hike',
            description='A trail walk.',
            intensity='low',
            location=ExerciseLocation.OUTDOOR,
            duration_minutes=10,
            weight_status=WeightStatus.ALL,
            min_age=10,
            max_age=100,
            conditions=['all'],
        )

        response = self.client.get(reverse('info:exercises'), {'location': ExerciseLocation.INDOOR})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Indoor stretch')
        self.assertContains(response, 'Any-place walk')
        self.assertNotContains(response, 'Outdoor hike')

    def test_all_exercise_catalog_bypasses_profile_matching(self):
        self.client.post(reverse('dashboard'), self.profile_data)
        catalog_exercise = ExerciseItem.objects.create(
            name='All catalog exercise',
            description='A catalog activity outside the current profile match.',
            intensity='high',
            location=ExerciseLocation.OUTDOOR,
            duration_minutes=25,
            weight_status=WeightStatus.UNDERWEIGHT,
            min_age=60,
            max_age=80,
            conditions=['diabetes'],
        )

        response = self.client.get(reverse('info:exercises'), {'catalog': 'all'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, catalog_exercise.name)
        self.assertContains(response, 'Showing every exercise in the catalog')

    def test_staff_can_import_and_delete_exercise_tips(self):
        self.client.post(reverse('dashboard'), {
            **self.profile_data,
        })
        self.user.is_staff = True
        self.user.save(update_fields=['is_staff'])
        csv_content = (
            'name,description,intensity,duration_minutes,weight_status,min_age,max_age,conditions,avoid_conditions\n'
            'Gentle walk,An easy walk,low,20,all,10,100,all,\n'
        )
        upload = SimpleUploadedFile('exercises.csv', csv_content.encode(), content_type='text/csv')

        response = self.client.post(reverse('info:exercise_import'), {'file': upload})
        exercise = ExerciseItem.objects.get(name='Gentle walk')
        self.assertRedirects(response, reverse('info:exercises'))
        self.assertEqual(exercise.location, ExerciseLocation.BOTH)

        edit_page = self.client.get(reverse('info:exercise_edit', args=[exercise.pk]))
        self.assertEqual(edit_page.status_code, 200)
        self.assertContains(edit_page, 'Update exercise tip')

        edit_response = self.client.post(
            reverse('info:exercise_edit', args=[exercise.pk]),
            {
                'name': 'Updated gentle walk',
                'description': 'A relaxed neighborhood walk.',
                'intensity': 'low',
                'location': ExerciseLocation.INDOOR,
                'duration_minutes': '25',
                'weight_status': 'all',
                'min_age': '10',
                'max_age': '100',
                'conditions': ['all'],
                'avoid_conditions': [],
            },
        )
        exercise.refresh_from_db()
        self.assertRedirects(edit_response, reverse('info:exercises'))
        self.assertEqual(exercise.name, 'Updated gentle walk')
        self.assertEqual(exercise.duration_minutes, 25)
        self.assertEqual(exercise.location, ExerciseLocation.INDOOR)

        delete_response = self.client.post(reverse('info:exercise_delete', args=[exercise.pk]))
        self.assertRedirects(delete_response, reverse('info:exercises'))
        self.assertFalse(ExerciseItem.objects.filter(pk=exercise.pk).exists())

    def test_invalid_exercise_import_does_not_create_partial_records(self):
        self.client.post(reverse('dashboard'), {
            'age': '28',
            'height_cm': '172',
            'weight_kg': '60',
            'health_status': [],
            'health_status_details': '',
            'injury_details': '',
            'food_allergy_details': '',
        })
        self.user.is_staff = True
        self.user.save(update_fields=['is_staff'])
        csv_content = (
            'name,description,intensity,duration_minutes,weight_status,min_age,max_age,conditions,avoid_conditions\n'
            'Good row,Description,low,20,all,10,100,all,\n'
            'Bad row,Description,fast,20,all,10,100,all,\n'
        )
        upload = SimpleUploadedFile('exercises.csv', csv_content.encode(), content_type='text/csv')

        response = self.client.post(reverse('info:exercise_import'), {'file': upload})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Could not import exercises')
        self.assertFalse(ExerciseItem.objects.exists())

    def test_bmi_status_distinguishes_obesity_range(self):
        profile = HealthProfile.objects.create(
            user=self.user,
            age=35,
            height_cm=170,
            weight_kg=90,
        )
        self.assertEqual(profile.status_label, 'Obese')
