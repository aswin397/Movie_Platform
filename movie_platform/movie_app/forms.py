from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Review

from .models import Category
from .models import Genre

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': 'Genre Name',
        }



class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }


# Form for user profile updates
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Custom registration form with added fields and validations
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        """Override save method to handle additional fields."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Form for adding/editing movies
class MovieForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select,
        label="Select Genre"
    )

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'genre', 'imdb_rating', 'overview', 'poster', 'category']
        
        widgets = {
            'release_date': forms.SelectDateWidget,
        }

    def clean_imdb_rating(self):
        """Validate that the IMDB rating is between 0 and 10."""
        rating = self.cleaned_data.get('imdb_rating')
        if rating < 0 or rating > 10:
            raise forms.ValidationError("IMDB rating must be between 0 and 10.")
        return rating

# Form for submitting reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }
