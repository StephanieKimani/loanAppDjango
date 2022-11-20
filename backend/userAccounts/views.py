from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import NewUser
from .serializers import UserSerializer
# Create your views here.

# Displays all Users
@api_view(['GET'])
def userList(request):
    clients = NewUser.objects.all()
    serializer = UserSerializer(clients, many =True)
    return Response(serializer.data)

# Displays User based on the primary key
@api_view(['GET'])
def userDetail(request,pk):
    clients = NewUser.objects.get(id =pk)
    serializer = UserSerializer(clients, many =False)
    return Response(serializer.data)

# Creates/Registers Users in the User table in localhost
@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():  
       username=serializer.validated_data.get('username')
       account=serializer.validated_data.get('accountNo')
       email=serializer.validated_data.get('email')
       password=make_password(serializer.validated_data.get('password'))
       role="client"

       serializer.save(username=username,accountNo=account,email=email,password=password,role =role)
       print('User Created') 

    return Response(serializer.data)

# Overrides the Authentication-Token table to return token and user role  
class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {
            'token': token.key,
            'role': user.role,
            'username':user.username,
            'id':user.id,
           'accountNo':user.accountNo,
        }
        return Response(custom_response)

# Updates User based on primary key        
@api_view(['POST'])
def userUpdate(request,pk):
    client = NewUser.objects.get(id =pk)
    serializer = UserSerializer(instance = client,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data) 

# Deletes User
@api_view(['DELETE'])
def userDelete(request,pk):
    client = NewUser.objects.get(id =pk)
    client.delete()
    return Response('Item Succesfully Deleted')

# Test view for ongoing application development
def clientProcess(request):
 return HttpResponse("Hello")
    #return redirect('http://domain.com')

