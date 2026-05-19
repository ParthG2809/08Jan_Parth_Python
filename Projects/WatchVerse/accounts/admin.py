from django.contrib import admin
from .models import User, Profile, Follow, MediaItem, Review, Activity, Genre, UserProgress, Collection, Discussion

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_verified', 'is_staff')
    search_fields = ('email', 'full_name')

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'release_year', 'rating_avg', 'verdict', 'is_featured', 'is_hidden_gem')
    list_filter = ('media_type', 'verdict', 'is_featured', 'is_hidden_gem', 'genres')
    search_fields = ('title',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Review)
admin.site.register(Activity)
admin.site.register(UserProgress)
admin.site.register(Collection)
admin.site.register(Discussion)
