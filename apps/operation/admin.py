from django.contrib import admin

# Register your models here.

from operation.models import UserAsk, UserCourse, CourseComment, UserFavorite, UserMessage


class UserAskAdmin(admin.ModelAdmin):
    pass


class UserCourseAdmin(admin.ModelAdmin):
    pass


class CourseCommentAdmin(admin.ModelAdmin):
    pass


class UserFavoriteAdmin(admin.ModelAdmin):
    pass


class UserMessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserMessage, UserMessageAdmin)