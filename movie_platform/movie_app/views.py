from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from .forms import CategoryForm, MovieForm, RegistrationForm, ReviewForm, UserProfileForm
from .models import Movie, Review, Category
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


User = get_user_model()


from .models import Genre
from .forms import GenreForm

def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_platform:admin_profile')  # Redirect to add_movie after adding genre
    else:
        form = GenreForm()

    return render(request, 'add_genre.html', {'form': form})


def add_user(request):
    if request.method == 'POST':
        # Use .get() to safely retrieve values
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure all fields are provided
        if not username or not first_name or not last_name or not email or not password:
            return render(request, 'add_user.html', {'error': 'All fields are required'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'add_user.html', {'error': 'Username already exists'})

        # Create and save the user
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),  # Hash the password before saving
        )
        user.save()

        # Redirect to the admin profile page after user creation
        return redirect('movie_platform:admin_profile')

    return render(request, 'add_user.html')

# Admin profile view
class AdminProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        users = User.objects.all()
        categories = Category.objects.all()  # Fetch all categories
        return render(request, 'admin_profile.html', {'users': users, 'categories': categories})

# View to confirm user deletion
class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'confirm_delete.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('movie_platform:admin_profile') 

# View to add a new category
class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_platform:admin_profile')  # Redirect to admin profile page after adding
        return render(request, 'add_category.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensure only admin can access this view
def admin_profile_view(request):
    users = User.objects.all()
    return render(request, 'admin_profile.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_profile')
    return render(request, 'confirm_delete.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

# Helper function to check if user is superuser
def is_superuser(user):
    return user.is_superuser

def home(request):
    return render(request, 'home.html')

# User Authentication Views
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Correct function call
            return redirect('movie_platform:profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Correct function call
            messages.success(request, f'Welcome {user.first_name}! You have been registered successfully.')
            return redirect('movie_platform:home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('movie_platform:user_login')

# User Profile Views
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('movie_platform:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})

# Movie Views
def movie_list(request):
    movies = Movie.objects.all()  # Fetch all movies from the database
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie)  # Fetch reviews for the movie
    
    # Assuming `ReviewForm` is the form class for adding reviews
    form = ReviewForm()
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    }
    
    return render(request, 'movie_detail.html', context)


@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    existing_review = Review.objects.filter(movie=movie, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user

            if existing_review:
                # Update existing review
                existing_review.rating = review.rating
                existing_review.comment = review.comment
                existing_review.save()
                messages.success(request, 'Your review has been updated.')
            else:
                # Create new review
                review.save()
                messages.success(request, 'Your review has been added.')

            return redirect('movie_platform:movie_detail', pk=movie.pk)
    else:
        form = ReviewForm(instance=existing_review)

    return render(request, 'movie_app/add_review.html', {'form': form, 'movie': movie})


def update_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_platform:movie_list')  # Redirect to the movie list after saving
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user  # Set the user field
            movie.save()
            return redirect('movie_platform:movie_list')  # Redirect to your movie list or another page
    else:
        form = MovieForm()
    
    return render(request, 'add_movie.html', {'form': form})

def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_platform:movie_list')  # Redirect to movie list after saving
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user == movie.user:
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this movie.')
    return redirect('movie_platform:movie_list')

# Movie Search
@login_required
def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'movie_list.html', {'movies': movies})

# Admin Views
@login_required
@user_passes_test(is_superuser)
def admin_add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" added successfully.')
        return redirect('movie_platform:admin_panel')
    return render(request, 'admin_add_category.html')

@login_required
@user_passes_test(is_superuser)
def admin_panel(request):
    users = User.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin_panel.html', {'users': users, 'categories': categories})
