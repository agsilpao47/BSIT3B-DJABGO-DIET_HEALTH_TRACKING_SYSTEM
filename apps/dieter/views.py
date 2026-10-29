import csv
import io
import json
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.info.models import (
    ExerciseItem,
    ExerciseLocation,
    FoodCategory,
    FoodItem,
    HealthProfile,
    MealType,
)

from .forms import ExerciseImportForm, ExerciseItemForm, FoodItemForm
from .services import (
    exercises_for_profile,
    recommended_foods_for_profile,
    total_food_plan_cost,
)


EXERCISE_CSV_FIELDS = (
    'name',
    'description',
    'intensity',
    'duration_minutes',
    'weight_status',
    'min_age',
    'max_age',
    'conditions',
    'avoid_conditions',
)


def _get_profile(user):
    try:
        return user.health_profile
    except HealthProfile.DoesNotExist:
        return None


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return wrapped_view


@login_required(login_url='login')
def profile_view(request):
    messages.info(request, 'Your profile is now on the My Profile page.')
    return redirect('dashboard')


@login_required(login_url='login')
def foods_view(request):
    profile = _get_profile(request.user)
    if profile is None:
        messages.info(request, 'Add your body details to view personalized food tips.')
        return redirect('dashboard')
    food_filters = _food_filter_context(request)
    catalog_mode = request.GET.get('catalog') == 'all'
    food_source = FoodItem.objects.all() if catalog_mode else recommended_foods_for_profile(profile)
    foods = _filter_foods(food_source, food_filters)
    return render(request, 'health/foods.html', {
        'profile': profile,
        'foods': foods,
        'food_plan_total': total_food_plan_cost(foods),
        'catalog_mode': catalog_mode,
        'has_food_allergies': bool(
            profile.food_allergy_details
            or (profile.health_status_answers or {}).get('food_allergy_options')
        ),
        'has_unlisted_food_allergy': (
            'other' in (profile.health_status_answers or {}).get('food_allergy_options', [])
        ),
        'all_foods': FoodItem.objects.all() if request.user.is_staff else [],
        'food_form': FoodItemForm() if request.user.is_staff else None,
        'editing_food': None,
        **food_filters,
    })


@staff_required
@require_POST
def create_food_view(request):
    form = FoodItemForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Food tip added.')
        return redirect('info:foods')

    profile = _get_profile(request.user)
    if profile is None:
        messages.info(request, 'Add your body details to view personalized food tips.')
        return redirect('dashboard')
    foods = recommended_foods_for_profile(profile)
    return render(request, 'health/foods.html', {
        'profile': profile,
        'foods': foods,
        'food_plan_total': total_food_plan_cost(foods),
        'has_food_allergies': bool(
            profile.food_allergy_details
            or (profile.health_status_answers or {}).get('food_allergy_options')
        ),
        'has_unlisted_food_allergy': (
            'other' in (profile.health_status_answers or {}).get('food_allergy_options', [])
        ),
        'all_foods': FoodItem.objects.all(),
        'food_form': form,
        'editing_food': None,
        **_food_filter_context(request),
    })


@staff_required
@require_POST
def delete_food_view(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id)
    food.delete()
    messages.success(request, 'Food tip deleted.')
    return redirect('info:foods')


@staff_required
def edit_food_view(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id)
    form = FoodItemForm(
        request.POST if request.method == 'POST' else None,
        instance=food,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Food tip updated.')
        return redirect('info:foods')

    profile = _get_profile(request.user)
    if profile is None:
        messages.info(request, 'Add your body details to view personalized food tips.')
        return redirect('dashboard')
    foods = recommended_foods_for_profile(profile)
    return render(request, 'health/foods.html', {
        'profile': profile,
        'foods': foods,
        'food_plan_total': total_food_plan_cost(foods),
        'has_food_allergies': bool(
            profile.food_allergy_details
            or (profile.health_status_answers or {}).get('food_allergy_options')
        ),
        'has_unlisted_food_allergy': (
            'other' in (profile.health_status_answers or {}).get('food_allergy_options', [])
        ),
        'all_foods': FoodItem.objects.all(),
        'food_form': form,
        'editing_food': food,
        **_food_filter_context(request),
    })


@login_required(login_url='login')
def exercises_view(request):
    profile = _get_profile(request.user)
    if profile is None:
        messages.info(request, 'Add your body details to view personalized exercise tips.')
        return redirect('dashboard')
    exercise_filters = _exercise_filter_context(request)
    catalog_mode = request.GET.get('catalog') == 'all'
    exercises = ExerciseItem.objects.all() if catalog_mode else exercises_for_profile(profile)
    if exercise_filters['selected_location']:
        exercises = [
            exercise for exercise in exercises
            if exercise.location in (exercise_filters['selected_location'], ExerciseLocation.BOTH)
        ]
    return render(request, 'health/exercises.html', {
        'profile': profile,
        'exercises': exercises,
        'catalog_mode': catalog_mode,
        'all_exercises': ExerciseItem.objects.all() if request.user.is_staff else [],
        'import_form': ExerciseImportForm() if request.user.is_staff else None,
        'exercise_form': ExerciseItemForm() if request.user.is_staff else None,
        'editing_exercise': None,
        **exercise_filters,
    })


@login_required(login_url='login')
def diet_tracker_removed_view(request):
    messages.info(request, 'Diet Tracker has been removed.')
    return redirect('dashboard')


@staff_required
@require_POST
def import_exercises_view(request):
    form = ExerciseImportForm(request.POST, request.FILES)
    if not form.is_valid():
        return _render_exercises_with_form(request, form)

    try:
        exercises = _parse_exercise_csv(form.cleaned_data['file'])
    except (UnicodeDecodeError, csv.Error, ValueError, ValidationError) as error:
        messages.error(request, f'Could not import exercises: {error}')
        return _render_exercises_with_form(request, form)

    with transaction.atomic():
        ExerciseItem.objects.bulk_create(exercises)
    messages.success(request, f'Imported {len(exercises)} exercise tips.')
    return redirect('info:exercises')


@staff_required
@require_POST
def delete_exercise_view(request, exercise_id):
    exercise = get_object_or_404(ExerciseItem, pk=exercise_id)
    exercise.delete()
    messages.success(request, 'Exercise tip deleted.')
    return redirect('info:exercises')


@staff_required
def edit_exercise_view(request, exercise_id):
    exercise = get_object_or_404(ExerciseItem, pk=exercise_id)
    form = ExerciseItemForm(
        request.POST if request.method == 'POST' else None,
        instance=exercise,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exercise tip updated.')
        return redirect('info:exercises')

    return _render_exercises_with_form(
        request,
        ExerciseImportForm(),
        exercise_form=form,
        editing_exercise=exercise,
    )


def _render_exercises_with_form(
    request,
    import_form,
    exercise_form=None,
    editing_exercise=None,
):
    profile = _get_profile(request.user)
    if profile is None:
        messages.info(request, 'Add your body details to view personalized exercise tips.')
        return redirect('dashboard')
    return render(request, 'health/exercises.html', {
        'profile': profile,
        'exercises': exercises_for_profile(profile),
        'all_exercises': ExerciseItem.objects.all(),
        'import_form': import_form,
        'exercise_form': exercise_form or ExerciseItemForm(),
        'editing_exercise': editing_exercise,
    })


def _parse_exercise_csv(uploaded_file):
    reader = csv.DictReader(io.StringIO(uploaded_file.read().decode('utf-8-sig')))
    if reader.fieldnames is None:
        raise ValueError('The CSV file is empty.')

    missing_fields = set(EXERCISE_CSV_FIELDS).difference(reader.fieldnames)
    if missing_fields:
        raise ValueError(f'Missing CSV columns: {", ".join(sorted(missing_fields))}.')

    exercises = []
    for row_number, row in enumerate(reader, start=2):
        extra_columns = row.get(None)
        if extra_columns and any(value.strip() for value in extra_columns if value):
            raise ValueError(f'Row {row_number} has more columns than the CSV header.')
        if not any((row.get(field) or '').strip() for field in EXERCISE_CSV_FIELDS):
            continue
        if row_number > 501:
            raise ValueError('A CSV import can contain at most 500 exercises.')
        try:
            exercise = ExerciseItem(
                name=(row.get('name') or '').strip(),
                description=(row.get('description') or '').strip(),
                intensity=(row.get('intensity') or '').strip(),
                location=(row.get('location') or ExerciseLocation.BOTH).strip() or ExerciseLocation.BOTH,
                duration_minutes=int(row.get('duration_minutes') or ''),
                weight_status=(row.get('weight_status') or '').strip(),
                min_age=int(row.get('min_age') or ''),
                max_age=int(row.get('max_age') or ''),
                conditions=_parse_csv_list(row.get('conditions') or ''),
                avoid_conditions=_parse_csv_list(row.get('avoid_conditions') or ''),
            )
            if exercise.min_age > exercise.max_age:
                raise ValueError('Minimum age cannot exceed maximum age.')
            exercise.full_clean()
        except (KeyError, TypeError, ValueError, ValidationError) as error:
            raise ValidationError(f'Row {row_number}: {error}') from error
        exercises.append(exercise)

    if not exercises:
        raise ValueError('The CSV file contains no exercise rows.')
    return exercises


def _food_filter_context(request):
    meal_type = request.GET.get('meal_type', '')
    food_category = request.GET.get('food_category', '')
    return {
        'meal_type_choices': MealType.choices,
        'food_category_choices': FoodCategory.choices,
        'selected_meal_type': meal_type if meal_type in MealType.values else '',
        'selected_food_category': food_category if food_category in FoodCategory.values else '',
    }


def _filter_foods(foods, food_filters):
    if food_filters['selected_meal_type']:
        foods = [
            food for food in foods
            if food.meal_type == food_filters['selected_meal_type']
        ]
    if food_filters['selected_food_category']:
        foods = [
            food for food in foods
            if food.food_category == food_filters['selected_food_category']
        ]
    return foods


def _exercise_filter_context(request):
    location = request.GET.get('location', '')
    locations = ExerciseLocation.choices
    valid_locations = {value for value, _label in locations if value != ExerciseLocation.BOTH}
    return {
        'exercise_location_choices': [
            (value, label) for value, label in locations if value != ExerciseLocation.BOTH
        ],
        'selected_location': location if location in valid_locations else '',
    }


def _parse_csv_list(value):
    value = value.strip()
    if not value:
        return []
    if value.startswith('['):
        parsed = json.loads(value)
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise ValueError('Condition columns must be lists of text values.')
        return parsed
    return [item.strip() for item in value.split(',') if item.strip()]
