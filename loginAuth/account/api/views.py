
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from social_django.utils import psa
from requests.exceptions import HTTPError
from django.contrib.auth import authenticate
from account.api.serializers import UserLoginSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLogin(APIView):
    
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    print(request)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'errors': {'token': 'Invalid token'}},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def authentication_test(request):
    print(request.user)
    return Response({'message': "User successfully authenticated"},status=status.HTTP_200_OK)


    
    # def post(self, request):
        
        
        
        
        # username = request.Meta.get("username")
        # password = request.Meta.get("password")
        
        # username = request.META.get('HTTP_X_USERNAME')
        # password = request.META.get('HTTP_X_PASSWORD')
        # serializer = UserLoginSerializer(data=request.data)
        # # print(serializer)
        # if serializer.is_valid():
        #     print("hello")
        #     username = serializer.data.get("username")
        #     password = serializer.data.get("password")
        #     print(username)
        #     user = authenticate(username=username, password=password)
        #     # user = authenticate(username=username)
            
        #     if user is not None:
        #         refresh = RefreshToken.for_user(user)
        #         refresh_token = str(refresh)
        #         access_token = str(refresh.access_token)
                    
        #         response_data = {
        #             "msg":"Login Successfully",
        #             "refresh_token":refresh_token,
        #             "access_token": access_token
        #         }
        #         return Response(response_data, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"msg":"Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"msg":"Invalid User"}, status=status.HTTP_400_BAD_REQUEST)