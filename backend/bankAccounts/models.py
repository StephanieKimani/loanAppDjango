from django.db import models

# Create your models here.

class BankDetail(models.Model):
    accountNo = models.AutoField(primary_key=True)
    newCreditCustomer=models.CharField(max_length=100)
    age=models.IntegerField()
    gender = models.IntegerField()
    education=models.IntegerField()
    maritalStatus=models.IntegerField()
    employmentStatus=models.IntegerField()
    employmentDurationCurrentEmployer = models.CharField(max_length=100)
    incomeTotal=models.IntegerField()
    debtToIncomeRatio =models.FloatField()
    creditScore = models.FloatField()
    noOfPreviousLoansBeforeLoan = models.IntegerField()
    amountOfPreviousLoansBeforeLoan = models.IntegerField()
    noOfPreviousEarlyRepaymentsBeforeLoan = models.IntegerField()
    #class Meta:
        #read_only_model = True