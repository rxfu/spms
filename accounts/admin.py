from django.contrib import admin

from .models import Role, Profile


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
