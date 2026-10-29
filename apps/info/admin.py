from django.contrib import admin

from .models import ExerciseItem, FoodItem, HealthProfile


@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height_cm', 'weight_kg', 'daily_food_budget', 'food_budget_period', 'updated_at')
    search_fields = ('user__username',)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'food_category', 'calories', 'estimated_cost', 'weight_status')
    list_filter = ('meal_type', 'food_category', 'weight_status')


@admin.register(ExerciseItem)
class ExerciseItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'intensity', 'location', 'duration_minutes', 'weight_status', 'min_age', 'max_age')
    list_filter = ('intensity', 'location', 'weight_status')
