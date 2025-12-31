from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
	path('', views.reviews_list, name='reviews_list'),
    path('<int:pk>/', views.reviews_detail, name='reviews_detail'),
    path('create/', views.reviews_create, name='reviews_create'),
    path('<int:pk>/update/', views.reviews_update, name='reviews_update'),
    path('<int:pk>/delete/', views.reviews_delete, name='reviews_delete'),
]