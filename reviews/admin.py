from typing import List

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse_lazy
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from projects.models import Information
from settings.models import Setting
from spms.settings import G_PANELIST
from .forms import ReviewForm
from .models import Review
from .views import ReviewRedirectView


# Register your models here.
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    form = ReviewForm

    @display(description='评审')
    def review(self, obj):
        return format_html(
            '<a href="{0}" alt="{1}" title="{1}" target="_blank" class="bg-primary-600 border border-transparent flex flex-row font-light group items-center justify-center py-1 rounded-md text-xs text-white w-full">{1}</a>',
            reverse_lazy('admin:review_project', kwargs={"project_id": obj.id}), '评审')

    @display(description='项目名称')
    def get_project(self, obj):
        return obj.name

    def get_urls(self) -> List[URLPattern]:
        return [
            path('<int:project_id>/project', ReviewRedirectView.as_view(), name='review_project'),
            # path('<int:project_id>/add', ReviewProjectView.as_view(model_admin=self), name='review_add'),
            # path('<int:object_id>/change', ReviewProjectView.as_view(model_admin=self),
            #      name='review_change')
        ] + super().get_urls()

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        project = Information.objects.get(id=request.GET['project_id'])
        extra_context["project"] = project

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        review = Review.objects.get(id=object_id)
        project = Information.objects.get(id=review.project_id)
        extra_context["project"] = project

        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updator = request.user
        else:
            if not Setting.objects.filter(is_opened=True).exists():
                raise ValidationError('系统已关闭，请稍后再试！')

            setting = Setting.objects.get(is_opened=True)
            project = Information.objects.get(id=request.GET['project_id'])

            obj.year = setting.year
            obj.phase = setting.phase
            obj.project = project
            obj.panelist = request.user
            obj.creator = obj.updator = request.user

        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        @display(description='评审意见')
        def get_opinion(obj):
            return Review.objects.get(year=obj.year, project=obj, panelist=request.user).opinion

        @display(description='是否同意申报')
        def get_status(obj):
            review = Review.objects.get(year=obj.year, project=obj, panelist=request.user)

            if review.is_agreed is not None:
                if review.is_agreed:
                    status = ['green', '已同意']
                else:
                    status = ['red', '不同意']
            else:
                status = ['gray', '未审核']

            return format_html(
                '<div class="flex items-center"><div class="block mr-3 outline rounded-full ml-1 h-1 w-1 bg-{0}-500 outline-{0}-200 outline-{0}-500/20"></div><span>{1}</span></div>',
                status[0], status[1])

        fields = ['review', 'year', 'get_project', get_opinion, get_status]

        return fields

    def get_list_display_links(self, request, list_display):
        return None

    def response_post_save_add(self, request, obj):
        return redirect(reverse_lazy('admin:reviews_review_changelist'))

    def response_post_save_change(self, request, obj):
        return redirect(reverse_lazy('admin:reviews_review_changelist'))

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if Setting.objects.filter(is_opened=True).exists():
            setting = Setting.objects.get(is_opened=True)

            if request.user.is_authenticated:
                if request.user.is_superuser:
                    qs = Information.objects.all()
                elif request.user.groups.filter(id=G_PANELIST).exists():
                    qs = Information.objects.filter(year=setting.year, team=request.user.profile.team)

                    # if request.resolver_match.func.__name__ == 'change_view':
                    #     qs = Review.objects.get(id=request.object_id)

        return qs

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)

        if Setting.objects.filter(is_opened=True).exists():
            setting = Setting.objects.get(is_opened=True)

            if request.user.is_authenticated:
                if request.user.groups.filter(id=G_PANELIST, year=setting.year).exists():
                    obj = Review.objects.get(id=object_id)

        return obj
