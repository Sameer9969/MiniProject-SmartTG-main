from django.contrib import admin
from .models import ContactMessage, Place, Wishlist,UserProfile

admin.site.register(ContactMessage)
admin.site.register(Place)
admin.site.register(Wishlist)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone')
