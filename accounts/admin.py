from typing import List

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display, action

from .forms import ProfileForm, UserForm
from .models import Profile, Team
from .views import RegisterView, UserLoginView, ProfileRedirectView

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)


class ProfileInline(StackedInline):
    model = Profile
    # formset = inlineformset_factory(User, Profile, form=ProfileForm)
    can_delete = False
    fk_name = 'user'
    extra = 1
    fields = ['name', 'gender', 'phone', 'idtype', 'idnumber', 'college', 'department', 'education', 'degree', 'title',
              'subject', 'area', 'bank', 'bankno', 'remark']


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    inlines = [ProfileInline]
    add_form = UserForm
    list_display = ("username", "email", 'get_name', 'get_groups', 'get_team', "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    actions = ['unset_team']

    @display(description="所属组")
    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])

    @display(description='所属评审组')
    def get_team(self, obj):
        return obj.profile.team

    @display(description='姓名')
    def get_name(self, obj):
        return obj.profile.name

    def get_urls(self) -> List[URLPattern]:
        return super().get_urls() + [
            path(
                "login",
                UserLoginView.as_view(model_admin=self),
                name="login"
            ),
            path(
                "register",
                RegisterView.as_view(model_admin=self),
                name="register"
            ),
        ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.pk:
                instance.updator = instance.creator = request.user
            else:
                instance.updator = request.user

            instance.save()

        formset.save_m2m()

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
                q.profile.team = team
                q.profile.save()

        return assign_team

    @action(description='取消分组', permissions=['unset_team'])
    def unset_team(self, request, queryset):
        for q in queryset:
            q.profile.team = None
            q.profile.save()

    def has_unset_team_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True

        return False


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    list_display = ['name', 'get_permissions']

    @display(description='权限')
    def get_permissions(self, obj):
        return ', '.join([permission.name for permission in obj.permissions.all()])


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    form = ProfileForm

    @display(description='所属组')
    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.user.groups.all()])

    def get_urls(self) -> List[URLPattern]:
        return super().get_urls() + [path('list', ProfileRedirectView.as_view(), name='profile_list')]

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
            obj.user = request.user
            obj.creator = obj.updator = request.user

        super().save_model(request, obj, form, change)

    def response_post_save_add(self, request, obj):
        return redirect(reverse_lazy('admin:projects_information_changelist'))

    def response_post_save_change(self, request, obj):
        return redirect(reverse_lazy('admin:projects_information_changelist'))

    def get_list_display(self, request):
        fields = ['name', 'gender', 'phone', 'birthday', 'department', 'education', 'degree', 'title', 'subject',
                  'get_groups', 'team']

        return fields
