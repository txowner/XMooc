from django.contrib import admin

# Register your models here.

from organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin(admin.ModelAdmin):
    pass


class CourseOrgAdmin(admin.ModelAdmin):
    pass


class TeacherAdmin(admin.ModelAdmin):
    pass


admin.site.register(CityDict, CityDictAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)