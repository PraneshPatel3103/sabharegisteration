from django.contrib import admin
from .models import UserProfile, EventDetail, Pradesh, Sant, SabhaOption, DashboardContent

# Register dropdown models for admin management
admin.site.register(Pradesh)
admin.site.register(Sant)

admin.site.register(DashboardContent)

# Show EventDetail inline within UserProfile admin
class EventDetailInline(admin.TabularInline):
    model = EventDetail
    extra = 0  # Number of empty forms shown

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'city', 'pradesh', 'reference_sant', 'is_approved')
    inlines = [EventDetailInline]

admin.site.register(UserProfile, UserProfileAdmin)
