from django.contrib import admin
from .models import UserProfile, UserRating, MealCategory, Ingredient, Recipe, RecipeIngredient, RecipeImage

admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(MealCategory)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeImage)