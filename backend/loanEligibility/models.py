from django.db import models
from userAccounts.models import NewUser

# Create your models here.

class LoanDetail(models.Model):
    #accountNo = models.ForeignKey(NewUser,to_field="accountNo",db_column="accountNo",on_delete=models.CASCADE)
    accountNo = models.IntegerField(blank=True)
    amount=models.FloatField(blank=True)
    interest = models.FloatField(blank =True)
    loanDuration=models.IntegerField(blank=True)
    monthlyPayment=models.FloatField(blank=True)
    loanPurpose =models.CharField(max_length =100,blank=True)
    images = models.ImageField(upload_to ='images',null=True,blank =True)
    lossGivenDefault=models.FloatField(blank =True)
    default=models.CharField(max_length =100,blank =True)
    status=models.CharField(max_length =100,blank =True)
    repayed=models.CharField(max_length =100,blank =True)
    #class Meta:
        #read_only_model = True

   