from django.urls import path
from . import views
from .chatbot_views import chatbot_page, chatbot_api

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/<int:pk>/', views.movies_detail, name='movies_detail'),
    path('search/', views.search_movies, name='search_movies'),
    
    path('reviews/create/', views.reviews_create, name='reviews_create'),
    path('reviews/create/<int:movie_id>/', views.reviews_create, name='reviews_create_with_movie'),
    path('reviews/<int:pk>/', views.reviews_detail, name='reviews_detail'),
    path('reviews/<int:pk>/update/', views.reviews_update, name='reviews_update'),
    path('reviews/<int:pk>/delete/', views.reviews_delete, name='reviews_delete'),
    
    path('chatbot/', chatbot_page, name='chatbot'),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
]