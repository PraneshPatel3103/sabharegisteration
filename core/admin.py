from django.contrib import admin
from .models import UserProfile, EventDetail
from .models import Pradesh, Sant, SabhaOption, DashboardContent

admin.site.register(Pradesh)
admin.site.register(Sant)
admin.site.register(SabhaOption)
admin.site.register(DashboardContent)


class EventDetailInline(admin.StackedInline):  # You can also use TabularInline
    model = EventDetail
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'city', 'pradesh', 'reference_sant', 'is_approved')
    inlines = [EventDetailInline]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EventDetail)
