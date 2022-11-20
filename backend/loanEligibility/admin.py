from django.contrib import admin
from django.contrib.auth.models import Group
from.models import LoanDetail

#Register your models here.
class AdminModifications(admin.ModelAdmin):
    def has_add_permission(self,request,obj=None):
        return False;
    def has_change_permission(self,request,obj=None):
        return False;
    def has_delete_permission(self,request,obj=None):
        return False;

admin.site.register(LoanDetail,AdminModifications)