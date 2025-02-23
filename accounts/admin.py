from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Exclude ManyToMany and reverse foreign key fields
    list_display = [
        field.name
        for field in CustomUser._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
