from django.contrib import admin

from .models import Member, Information


# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    pass
