from django.contrib import admin
from .models import Movie, Review

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'genre', 'release_date', 'is_tmdb', 'vote_average']
    list_filter = ['is_tmdb', 'genre']
    search_fields = ['title', 'director', 'cast']
    ordering = ['-created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'genre', 'created_at']
    list_filter = ['rating', 'genre']
    search_fields = ['title', 'content']
    ordering = ['-created_at']