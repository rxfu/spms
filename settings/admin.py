from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .forms import SettingForm
from .models import Gender, Idtype, Education, Degree, Title, Subject, Type, Department, Series, Phase, Setting


# Register your models here.
@admin.register(Gender)
class GenderAdmin(ModelAdmin):
    pass


@admin.register(Idtype)
class IdtypeAdmin(ModelAdmin):
    pass


@admin.register(Education)
class EducationAdmin(ModelAdmin):
    pass


@admin.register(Degree)
class DegreeAdmin(ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    pass


@admin.register(Series)
class SeriesAdmin(ModelAdmin):
    pass


@admin.register(Phase)
class PhaseAdmin(ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(ModelAdmin):
    form = SettingForm

    @display(description='项目系列')
    def get_series(self, obj):
        return obj.series.name

    @display(description='项目阶段')
    def get_phase(self, obj):
        return obj.phase.name

    def save_model(self, request, obj, form, change):
        if change:
            obj.updator = request.user
        else:
            obj.creator = obj.updator = request.user

        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        fields = ['id', 'year', 'get_series', 'get_phase', 'submit_beg_time', 'submit_end_time', 'review_beg_time',
                  'review_end_time', 'is_opened']

        return fields
