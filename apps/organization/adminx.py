
import xadmin

from organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'images', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'images', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'images', 'address', 'city', 'add_time']

    # 配置课程外检选择时通过ajax异步搜索完成
    relfield_style = 'fk-ajax'

    # 在xadmin的工具栏配置导入excel
    import_excel = True

    # 这个post回处理该管理器中的所有post数据的操作， 这里主要配置上传excel的函数，这里面可以添加处理excel的逻辑
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        # 返回值 必须这么写， 不然操作会失败且返回500
        return super(CourseOrgAdmin, self).post(request, args, kwargs)


class TeacherAdmin(object):
    list_display = \
        ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = \
        ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
