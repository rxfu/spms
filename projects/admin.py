from typing import List

from django.contrib import admin
from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, URLPattern, path
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display, action

from accounts.models import Team
from settings.models import Setting
from spms import settings
from .forms import InformationForm, MemberInlineForm
from .models import Member, Information
from .views import InformationRedirectView, ApplicationGenerateView


# Register your models here.
class MemberInline(TabularInline):
    model = Member
    formset = inlineformset_factory(Information, Member, form=MemberInlineForm)
    extra = 0
    hide_title = True
    tab = True
    fields = ['name', 'gender', 'education', 'degree', 'title', 'department', 'phone', 'subject', 'area']


@admin.register(Information)
class InformationAdmin(ModelAdmin):
    inlines = [MemberInline]
    form = InformationForm
    actions = ['delete_selected', 'unset_team']
    list_display = ('id', 'opinion', 'department_is_agreed')
    list_editable = ('opinion', 'department_is_agreed')

    @display(description='主持人')
    def get_applicant(self, obj):
        return obj.applicant.profile.name

    @display(description='项目组成员')
    def get_members(self, obj):
        return ', '.join(member.name for member in obj.member_set.all())

    @display(description='起始年限')
    def get_year(self, obj):
        return obj.beg_year.strftime('%Y年%m月') + ' 至 ' + obj.end_year.strftime('%Y年%m月')

    @display(description='项目申请书')
    def get_application(self, obj):
        return (
            format_html(
                '<a href="{0}" alt="{1}" title="{1}" target="_blank" class="text-primary-600">{1}</a>',
                obj.application_attachment.url,
                "查看",
            )
            if obj.application_attachment
            else format_html(
                '<div class="flex items-center"><div class="block mr-3 outline rounded-full ml-1 h-1 w-1 bg-red-500 outline-red-200 outline-red-500/20"></div><span>{}</span></div>'.format(
                    "未上传")
            )
        )

    @display(description='学院是否同意申报')
    def get_department_status(self, obj):
        if obj.department_is_agreed is not None:
            if obj.department_is_agreed:
                status = ['green', '已同意']
            else:
                status = ['red', '不同意']
        else:
            status = ['gray', '未审核']

        return format_html(
            '<div class="flex items-center"><div class="block mr-3 outline rounded-full ml-1 h-1 w-1 bg-{0}-500 outline-{0}-200 outline-{0}-500/20"></div><span>{1}</span></div>',
            status[0], status[1])

    @display(description='生成')
    def generate_button(self, obj):
        if Setting.objects.filter(year=obj.year, series=obj.series, is_opened=True).exists():
            return format_html(
                '<a href={} title="生成申请书" class="bg-green-500 border border-transparent flex flex-row font-light group items-center justify-center py-1 rounded-md text-xs text-white w-full">生成申请书</a>',
                reverse_lazy('admin:project_pdf', kwargs={'pk': obj.id}))

    @display(description='编辑')
    def edit_button(self, obj):
        if Setting.objects.filter(year=obj.year, series=obj.series, is_opened=True).exists():
            return format_html(
                '<a href={} title="编辑" class="bg-primary-600 border border-transparent flex flex-row font-light group items-center justify-center py-1 rounded-md text-xs text-white w-full">编辑</a>',
                reverse_lazy('admin:projects_information_change', args=(obj.id,)))

    @display(description='删除')
    def delete_button(self, obj):
        if Setting.objects.filter(year=obj.year, series=obj.series, is_opened=True).exists():
            return format_html(
                '<a href={} title="删除" class="bg-red-600 border border-transparent flex flex-row font-light group items-center justify-center py-1 rounded-md text-xs text-white w-full">删除</a>',
                reverse_lazy('admin:projects_information_delete', args=(obj.id,)))

    def get_urls(self) -> List[URLPattern]:
        return super().get_urls() + [
            path('list', InformationRedirectView.as_view(), name='project_list'),
            path('<int:pk>/pdf', ApplicationGenerateView.as_view(), name='project_pdf'),
        ]

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updator = request.user
        else:
            setting = Setting.objects.get(is_opened=True)

            obj.year = setting.year
            obj.series = setting.series
            obj.applicant = request.user
            obj.creator = obj.updator = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.pk:
                instance.updator = instance.creator = request.user
            else:
                instance.updator = request.user

            instance.save()

        formset.save_m2m()

    def get_list_display(self, request):
        fields = ['year', 'name', 'get_year', 'direction', 'get_applicant', 'get_members', 'get_application']

        if request.user.is_authenticated:
            if request.user.is_superuser:
                fields.extend(['team'])
            elif request.user.groups.filter(id=settings.G_APPLICANT).exists():
                fields.extend(['opinion', 'get_department_status', 'generate_button', 'edit_button', 'delete_button'])
            elif request.user.groups.filter(id=settings.G_COLLEGE).exists():
                fields.extend(['opinion', 'department_is_agreed'])

        return fields

    def get_list_display_links(self, request, list_display):
        return None

    def get_changelist_instance(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(id=settings.G_APPLICANT).exists():
                self.list_editable = ()

        return super().get_changelist_instance(request)

    def get_actions(self, request):
        actions = super().get_actions(request)

        if request.user.is_authenticated:
            if request.user.is_superuser:
                teams = Team.objects.all()
                for team in teams:
                    actions['set_team_' + str(team.id)] = (
                        self.set_team(team), 'set_team_' + str(team.id), '设置为' + team.name)

        return actions

    def set_team(self, team):
        def assign_team(self, request, queryset):
            for q in queryset:
                q.team = team
                q.save()

        return assign_team

    @action(description='取消分组', permissions=['unset_team'])
    def unset_team(self, request, queryset):
        for q in queryset:
            q.team = None
            q.save()

    def has_unset_team_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True

        return False

    @action(description='删除所选项目', permissions=['delete_selected'])
    def delete_selected(self, request, obj):
        for o in obj.all():
            if not Setting.objects.filter(year=o.year, series=o.series, is_opened=True).exists():
                messages.error(request, '不在申报时间，不能删除此项目')

                return redirect(reverse_lazy('admin:projects_information_changelist'))

            if o.review_set.exists():
                messages.error(request, '此项目已评审，不能删除')

                return redirect(reverse_lazy('admin:projects_information_changelist'))

            o.delete()

    def has_delete_selected_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.groups.filter(id=settings.G_COLLEGE).exists():
                return False

        return True

    def delete_model(self, request, obj):
        if not Setting.objects.filter(year=obj.year, series=obj.series, is_opened=True).exists():
            messages.error(request, '不在申报时间，不能删除此项目')

            return redirect(reverse_lazy('admin:projects_information_changelist'))

        if obj.review_set.exists():
            messages.error(request, '此项目已评审，不能删除')

            return redirect(reverse_lazy('admin:projects_information_changelist'))

        obj.delete()

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            if request.user.groups.filter(id=settings.G_APPLICANT).exists():
                qs = qs.filter(applicant=request.user)
            elif request.user.groups.filter(id=settings.G_COLLEGE).exists():
                qs = qs.filter(applicant__profile__department=request.user.profile.department)
            else:
                qs = None

        return qs
