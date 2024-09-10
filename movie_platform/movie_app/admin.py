from django.contrib import admin
from .forms import MovieForm
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    form = MovieForm

    def save_model(self, request, obj, form, change):
        # Assign the current user to the movie if it's a new object
        if not change:  # Checking if the movie is being created (not updated)
            obj.user = request.user
        else:
            # Ensure only the original owner can update the movie
            if obj.user != request.user:
                raise PermissionError("You are not allowed to edit this movie.")
        
        obj.save()

admin.site.register(Movie, MovieAdmin)
