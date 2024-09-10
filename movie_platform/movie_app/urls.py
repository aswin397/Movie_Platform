from django.urls import path
from . import views

app_name = 'movie_platform'  # App name for namespacing

urlpatterns = [
    path('', views.home, name='home'),  # Homepage

    # User Authentication and Profile
    path('login/', views.user_login, name='user_login'),  # Login page
    path('register/', views.register, name='register'),  # Registration page
    path('profile/', views.profile_view, name='profile'),  # View profile
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Edit profile
    path('logout/', views.user_logout, name='user_logout'),  # Logout functionality

    # Movie Views
    path('movies/', views.movie_list, name='movie_list'),  # List all movies
    path('movies/add/', views.add_movie, name='add_movie'),  # Add new movie
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),  # Movie details by id (pk)
    path('movies/edit/<int:pk>/', views.update_movie, name='update_movie'),  # Edit movie by id (pk)
    path('movies/delete/<int:pk>/', views.delete_movie, name='delete_movie'),  # Delete movie by id (pk)
    path('movies/<int:pk>/review/', views.add_review, name='add_review'),  # Add a review to a movie by id (pk)

    # Search functionality
    path('search/', views.search_movies, name='search_movies'),  # Search movies by query

    # Admin functionality
    path('admin/add-category/', views.admin_add_category, name='admin_add_category'),  # Add a new category
    path('admin/', views.admin_panel, name='admin_panel'),  # Admin dashboard

    path('admin-profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('delete-user/<int:user_id>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('add-category/', views.AddCategoryView.as_view(), name='add_category'),
    path('add-user/', views.add_user, name='add_user'),
    path('add-genre/', views.add_genre, name='add_genre'),
    
    # Other URLs...
]
