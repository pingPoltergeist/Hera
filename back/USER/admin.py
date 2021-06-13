from django.contrib import admin
from USER.models import UserProfile, Watchlist


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    meta = UserProfile
    list_display = ['dj_user', 'search_history', 'age', 'chosen_genres', ]


class WatchlistAdmin(admin.ModelAdmin):
    meta = Watchlist
    list_display = ['user', 'video', 'tv', 'status', 'video_timestamp', 'last_watched', ]


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
