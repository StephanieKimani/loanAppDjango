from rest_framework import serializers
from .models import LoanDetail
from userAccounts.models import NewUser

class UserLoanSerializer(serializers.ModelSerializer):
 class Meta:
        model= NewUser
        fields = '__all__'

class LoanDetailSerializer(serializers.ModelSerializer):
#loanId = serializers.IntegerField()
   #accountNo = UserLoanSerializer(many=True,read_only=True)
    images = serializers.ImageField(
        max_length=None, use_url=True, required = False  )

    class Meta:
        model= LoanDetail
        fields = ("id","amount", 'interest', 'loanDuration', 
        'monthlyPayment','loanPurpose','lossGivenDefault',
        'default','status','repayed','accountNo','images', )
       # depth=1
       
