from django.contrib import admin

# Register your models here.

from users.models import UserProfile, EmailVerifyRecord, Banner


class UserProfileAdmin(admin.ModelAdmin):
    pass


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'send_type', 'send_time']
    search_fields = ['email', 'code', 'send_type']
    list_filter = ['email', 'code', 'send_type', 'send_time']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)
