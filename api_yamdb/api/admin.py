from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'is_staff')
    search_fields = ('username',)
    list_editable = ('is_staff',)


admin.site.register(User, UserAdmin)
