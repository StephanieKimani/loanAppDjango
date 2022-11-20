from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import read_only_admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import LoanDetail
from .serializers import LoanDetailSerializer,UserLoanSerializer
from userAccounts.models import NewUser
from bankAccounts.models import BankDetail
from django.db import connection
import pandas
import numpy 
import mysql.connector as sql
from sklearn.preprocessing import StandardScaler
import pickle
from django.conf import settings 
from  itertools import product

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    apiUrls={
    'List of Loans':'/list',
    'Individual Loan':'/individual/<str:pk>',
    'Update Loan':'/update/<str:pk>'
    }
    return Response(apiUrls)

#class LoanDetailApi(viewsets.ModelViewSet):
 #   queryset = LoanDetail.objects.all()
  #  serializer_class = LoanDetailSerializer

#class UserDetailApi(viewsets.ModelViewSet):
 #   queryset = NewUser.objects.all()
  #  serializer_class = UserLoanSerializer

# Displays all Loans
@api_view(['GET'])
def loanList(request):
    clients = LoanDetail.objects.all()
    serializer = LoanDetailSerializer(clients, many =True)
    return Response(serializer.data)

# Creates Loans
@api_view(['POST'])
def loanCreate(request):
    serializer = LoanDetailSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):  
       amount=serializer.validated_data.get('amount')
       monthlyPayment=serializer.validated_data.get('monthlyPayment')
       loanDuration=serializer.validated_data.get('loanDuration')
       loanPurpose=serializer.validated_data.get('loanPurpose')
       images=serializer.validated_data.pop('images')
       accountNo=serializer.validated_data.get('accountNo')
       interest=(35.92)
       lossGivenDefault=(0.75)
       default="pending"
       status="pending"
       repayed="pending"
       
       serializer.save(amount=amount,monthlyPayment=monthlyPayment,
       loanDuration=loanDuration,loanPurpose=loanPurpose,images=images,
       accountNo=accountNo,interest=interest,
       lossGivenDefault=lossGivenDefault,default=default,
       status=status,repayed=repayed,)

       print('Loan Inserted')
       print(serializer.errors) 
    return Response(serializer.data)

# Displays loan details for one user based on the primary key (In this case,to load Images)
@api_view(['GET'])
def loanDetail(request,pk):
    loan = LoanDetail.objects.get(id =pk)
    serializer = LoanDetailSerializer(loan, many =False)
    return Response(serializer.data)

# For one user, get loan details based on pk,get additional client details based on account No 
@api_view(['GET'])
def updateDefault(request,pk,accountNo):

   dfLoan = pandas.DataFrame.from_records(LoanDetail.objects.filter(id =pk).values())
   dfLoan.drop(['id','accountNo','loanPurpose','images','default','status','repayed'],inplace = True,axis=1)
   dfClient = pandas.DataFrame.from_records(BankDetail.objects.filter(accountNo =accountNo).values())
   dfClient.drop(['accountNo'],inplace = True,axis=1)
   df = pandas.concat([dfLoan, dfClient], axis = 1)
   df = df[['newCreditCustomer','age','gender','amount','interest','loanDuration','monthlyPayment','education','maritalStatus','employmentStatus','employmentDurationCurrentEmployer','incomeTotal','debtToIncomeRatio','lossGivenDefault','creditScore','noOfPreviousLoansBeforeLoan','amountOfPreviousLoansBeforeLoan','noOfPreviousEarlyRepaymentsBeforeLoan']]
   
   def condition(x):
    if x ==0:
     return 'Male'
    elif x==1:
     return 'Female'
    else:
     return 'Undefined'
   df['genderNominal'] =df['gender'].apply(condition)
   df.drop('gender',inplace = True,axis=1)

   def condition(x):
    if x ==-1:
        return 'Married'
    elif x==1:
        return 'Married'
    elif x==2:
        return "Cohabitant"
    elif x==3:
        return 'Single'
    elif x==4:
        return 'Divorced'
    else:
        return 'Widow'
   df['maritalStatusNominal'] =df['maritalStatus'].apply(condition)
   df.drop('maritalStatus',inplace = True,axis=1)

   def condition(x):
    if x =='TrialPeriod' or x=='Other':
       return 1
    elif x=='UpTo1Year':
        return 2
    elif x=='UpTo2Years':
        return 3
    elif x=='UpTo3Years':
        return 4
    elif x=='UpTo4Years':
        return 5
    elif x=='UpTo5Years':
        return 6
    else:
        return 7
   df['employmentDurationCurrentEmployerOrdinal'] =df['employmentDurationCurrentEmployer'].apply(condition)
   df.drop('employmentDurationCurrentEmployer',inplace = True,axis=1)

   categoricalNominal_features =[]
   categoricalNominal_features_list =['newCreditCustomer','genderNominal','maritalStatusNominal']
   categoricalNominal_features.extend(categoricalNominal_features_list)

   categoricalOrdinal_features =[]
   categoricalOrdinal_features_list =['education','employmentStatus','employmentDurationCurrentEmployerOrdinal']
   categoricalOrdinal_features.extend(categoricalOrdinal_features_list)
 
   numerical_features =[]
   numerical_features_list =['age','amount','interest','loanDuration','monthlyPayment','incomeTotal','debtToIncomeRatio','lossGivenDefault','creditScore','noOfPreviousLoansBeforeLoan','amountOfPreviousLoansBeforeLoan','noOfPreviousEarlyRepaymentsBeforeLoan']
   numerical_features.extend(numerical_features_list)

   df['newCreditCustomer'] = df['newCreditCustomer'].astype(object) 
   list1 = ['True','False']
   list2=['Female','Male','Undefined']
   list3 =['Cohabitant','Divorced','Married','Single','Widow']
   df_nominal_credit=pandas.get_dummies(df[['newCreditCustomer']].astype(pandas.CategoricalDtype(categories=list1)))
   df_nominal_gender=pandas.get_dummies(df[['genderNominal']].astype(pandas.CategoricalDtype(categories=list2)))
   df_nominal_marriage=pandas.get_dummies(df[['maritalStatusNominal']].astype(pandas.CategoricalDtype(categories=list3)))
   #+['newCreditCustomer_False', 'newCreditCustomer_True','genderNominal_Female','genderNominal_Male','genderNominal_Undefined','maritalStatusNominal_Cohabitant]','maritalStatusNominal_Divorced','maritalStatusNominal_Married','maritalStatusNominal_Single','maritalStatusNominal_Widow'])
   df_nominal = pandas.concat([df_nominal_credit,df_nominal_gender,df_nominal_marriage],axis=1)
   

   for feature in categoricalOrdinal_features:
        df[feature]=df[feature].astype('category').cat.codes

   df_ordinal=df[categoricalOrdinal_features]

   new_dataset=pandas.concat([df_nominal,df_ordinal,df[numerical_features]],axis=1)
   
   X=new_dataset.to_numpy()
   scale_X = StandardScaler()
   X=scale_X.fit_transform(X)

   
   with open('C:\\Users\\reubenmbalanya\Desktop\loanappdjango\\backend\logisticRegressionLoanModel','rb') as f:
    model = pickle.load(f)

   prediction = model.predict(X)
   print("Prediction",prediction[0])

   if prediction==1:
    default= "Likely to Default"
   else:
    default ="Unlikely to Default"

   loan = LoanDetail.objects.filter(id=pk).first()
   serializer = LoanDetailSerializer(loan,data={'default':default},partial = True)

   if serializer.is_valid(raise_exception=True):  
       serializer.save()

       print('Loan Updated')
 

      
   return Response(serializer.data)

@api_view(['GET'])
def updateStatus(request,pk,status):
   loan = LoanDetail.objects.filter(id=pk).first()
   serializer = LoanDetailSerializer(loan,data={'status':status},partial = True)
    
   if serializer.is_valid(raise_exception=True):  
       serializer.save()

       print('Status Updated')
      
   return HttpResponse(serializer.data)

@api_view(['GET'])
def updateRepayed(request,pk):
   loan = LoanDetail.objects.filter(id=pk).order_by('id').latest('id')
   serializer = LoanDetailSerializer(loan,data={'repayed':'no'},partial = True)
    
   if serializer.is_valid(raise_exception=True):  
       serializer.save()
       print('Repayed Updated')
      
   return HttpResponse(serializer.data)

@api_view(['GET'])
def getStatus(request,accountNo):
    loan = LoanDetail.objects.filter(accountNo =accountNo).order_by('id').latest('id')
    serializer = LoanDetailSerializer(loan, many =False)
    return Response(serializer.data)
