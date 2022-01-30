from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _
admin.autodiscover()
admin.site.enable_nav_sidebar = False

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name','role', 'date_of_birth', 'phone_number', 'gender',
         'identity_card_number', 'parent_name', 'place_of_birth', 'address', 'country', 'nationality', 'settlement', 'image')}),
        (
            _('Permissions'),
            {
            'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields':('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Progress)
admin.site.register(models.Transcript)
admin.site.register(models.Course)
admin.site.register(models.CourseGrade)