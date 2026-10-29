from django.urls import path

from . import views

app_name = 'info'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('foods/', views.foods_view, name='foods'),
    path('foods/add/', views.create_food_view, name='food_create'),
    path('foods/<int:food_id>/edit/', views.edit_food_view, name='food_edit'),
    path('foods/<int:food_id>/delete/', views.delete_food_view, name='food_delete'),
    path('exercises/', views.exercises_view, name='exercises'),
    path('exercises/import/', views.import_exercises_view, name='exercise_import'),
    path(
        'exercises/<int:exercise_id>/delete/',
        views.delete_exercise_view,
        name='exercise_delete',
    ),
    path(
        'exercises/<int:exercise_id>/edit/',
        views.edit_exercise_view,
        name='exercise_edit',
    ),
    path('diet/', views.diet_tracker_removed_view, name='diet'),
]
