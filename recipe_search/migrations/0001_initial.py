# Generated by Django 5.0.4 on 2024-04-26 05:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Enter a description for the recipe.', null=True)),
                ('instructions', models.JSONField(blank=True, help_text='Enter cooking instructions for the recipe.', null=True)),
                ('preparation_time', models.DurationField(blank=True, help_text='Enter preparation time.', null=True)),
                ('cooking_time', models.DurationField(blank=True, help_text='Enter cooking time.', null=True)),
                ('youtube_url', models.CharField(blank=True, help_text='Enter the YouTube video URL', max_length=255, null=True)),
                ('categories', models.ManyToManyField(to='recipe_search.mealcategory')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='recipe_images/')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_search.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('manual_ingredient_name', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('unit', models.CharField(choices=[('ml', 'Milliliter'), ('kg', 'Kilogram'), ('db', 'Darab'), ('g', 'Gram'), ('l', 'Liter'), ('tk', 'Teáskanál'), ('evk', 'Evőkanál'), ('csipet', 'Csipet')], default='db', max_length=6)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_search.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_search.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipe_search.RecipeIngredient', to='recipe_search.ingredient'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_search.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_search.userprofile')),
            ],
        ),
    ]