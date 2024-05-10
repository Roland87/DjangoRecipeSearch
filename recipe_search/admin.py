from django.contrib import admin
from .models import UserProfile, UserRating, MealCategory, Ingrediente, Reipe, RecipeIngredient, RecipeImage

admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(MealCategory)
admin.site.register(Ingrediente)
admin.site.register(Reipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeImage)