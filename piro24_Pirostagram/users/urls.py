from django.urls import path
from . import views

app_name = 'users'  # URL 네임스페이스

urlpatterns = [
    # 회원가입: /users/signup/
    path('signup/', views.signup_view, name='signup'),
    
    # 로그인: /users/login/
    path('login/', views.login_view, name='login'),
    
    # 로그아웃: /users/logout/
    path('logout/', views.logout_view, name='logout'),
    
    # 프로필 수정: /users/profile/update/
    path('profile/update/', views.profile_update_view, name='profile_update'),
    
    # 유저 검색: /users/search/?q=검색어
    path('search/', views.user_search_view, name='search'),
    
    # 팔로워 목록: /users/<username>/followers/
    path('<str:username>/followers/', views.followers_list_view, name='followers'),
    
    # 팔로잉 목록: /users/<username>/following/
    path('<str:username>/following/', views.following_list_view, name='following'),
    
    # 팔로우 토글: /users/<username>/follow/
    path('<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),
    
    # 프로필 조회: /users/<username>/ (맨 마지막에 위치)
    path('<str:username>/', views.profile_view, name='profile'),
]