from django.db import models 
from django.contrib.auth.models import AbstractUser
from bankAccounts.models import BankDetail

# Create your models here.   

# Overrides the User Model(or table) to include accountNo and role 
class NewUser(AbstractUser):
      #accountNo = models.OneToOneField(BankDetail,on_delete=models.CASCADE,db_column="accountNo",null = True,blank=True)
      accountNo = models.IntegerField(null = True,blank=True)
      role= models.CharField(max_length=100,null=True)
