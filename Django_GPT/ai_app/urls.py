from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('summarize/', views.summarize, name='summarize'),
    path('sentiment/', views.sentiment, name='sentiment'),
    path('translate/', views.translate, name='translate'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]