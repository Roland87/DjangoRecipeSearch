from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import JSONField  # Import JSONField from django.db.models
from django.db.models import Sum  # Import Sum for calculating average rating

class UserProfile(models.Model):
    """User profile model to extend Django's default User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
    

class UserRating(models.Model):
    """Model to store user ratings for recipes."""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    rating = models.IntegerField()

    def save(self, *args, **kwargs):
        """Override save method to update average rating of associated recipe."""
        if not 0 <= self.rating <= 5:
            raise ValidationError('Rating should be between 0 and 5.')
        super().save(*args, **kwargs)
        self.update_recipe_average_rating()

    def delete(self, *args, **kwargs):
        """Override delete method to update average rating of associated recipe."""
        super().delete(*args, **kwargs)
        self.update_recipe_average_rating()

    def update_recipe_average_rating(self):
        """Calculate and update the average rating of the associated recipe."""
        recipe = self.recipe
        ratings = UserRating.objects.filter(recipe=recipe)

        if ratings:
            total_ratings = sum([rating.rating for rating in ratings])
            average_rating = total_ratings / len(ratings)
            recipe.average_rating = round(average_rating, 2)
        else:
            recipe.average_rating = 0.0
        recipe.save()


class MealCategory(models.Model):
    """Model to represent meal categories."""
    name = models.CharField(max_length=50, unique=True)


class Ingredient(models.Model):
    """Model to represent ingredients."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model to represent recipes."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, help_text="Enter a description for the recipe.")
    instructions = JSONField(blank=True, null=True, help_text="Enter cooking instructions for the recipe.")  # Use JSONField for instructions
    preparation_time = models.DurationField(blank=True, null=True, help_text="Enter preparation time.")
    cooking_time = models.DurationField(blank=True, null=True, help_text="Enter cooking time.")
    average_rating = models.FloatField(default=0)
    categories = models.ManyToManyField(MealCategory)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    youtube_url = models.CharField(max_length=255, blank=True, null=True, help_text="Enter the YouTube video URL")

    def average_rating(self):
        total_ratings = UserRating.objects.filter(recipe=self).count()
        if total_ratings > 0:
            sum_ratings = UserRating.objects.filter(recipe=self).aggregate(Sum('rating'))['rating__sum']
            return sum_ratings / total_ratings
        else:
            return None
    
    def total_ratings(self):
        return UserRating.objects.filter(recipe=self).count()


class RecipeIngredient(models.Model):
    """Model to represent the ingredients used in a recipe."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    manual_ingredient_name = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    UNIT_CHOICES = [
        ('ml', 'Milliliter'),
        ('kg', 'Kilogram'),
        ('db', 'Darab'),      # Darab (piece)
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('tk', 'Teáskanál'),  # Teáskanál (teaspoon)
        ('evk', 'Evőkanál'),  # Evőkanál (tablespoon)
        ('csipet', 'Csipet'),
    ]
    unit = models.CharField(max_length=6, choices=UNIT_CHOICES, default='db')

    def __str__(self):
        """Return string representation of RecipeIngredient."""
        if self.manual_ingredient_name:
            return f"{self.quantity} {self.get_unit_display()} {self.manual_ingredient_name}"
        else:
            return f"{self.quantity} {self.get_unit_display()} {self.ingredient.name}"


class RecipeImage(models.Model):
    """Model to represent images associated with recipes."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_images/')

    def __str__(self):
        return f"Image for {self.recipe.title}"
