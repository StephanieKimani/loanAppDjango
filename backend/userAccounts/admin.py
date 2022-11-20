from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

# Register your models here.

# Overrides the Admin page to display selected fields
fields = list(UserAdmin.fieldsets)
fields[1]=('Personal Info',{'fields': ('first_name','last_name','email','role')})
UserAdmin.fieldsets=tuple(fields)

admin.site.register(NewUser,UserAdmin)

