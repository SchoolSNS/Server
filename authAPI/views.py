from .models import User
from feedAPI.models import Post, Comment
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from feedAPI.serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.conf import settings
import requests

class RegisterView (GenericAPIView) :
    serializer_class = RegisterSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({'success': '회원가입에 성공했습니다.'}, status=201)

class LoginView (GenericAPIView) :
    serializer_class = LoginSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)

        try :
            user = User.objects.get(email=serializer.data['email'])

        except User.DoesNotExist :
            return Response({'message': ['이메일을 정확히 입력했는지 확인하여 주세요.']}, status=401)

        if user.check_password(raw_password=serializer.data['password']) == False :
            return Response({'message': ['비밀번호를 정확히 입력했는지 확인하여 주세요.']}, status=401)

        token = Token.objects.get_or_create(user=user)

        return Response({'token': F'{token[0]}'}, status=200)

class UsersPostView (ModelViewSet) :
    serializer_class = PostSerializer

    def get_queryset (self) :
        queryset = Post.objects.filter(owner=self.kwargs.get('user_id'))
        return queryset

class UsersCommentView (ModelViewSet) :
    serializer_class = CommentSerializer

    def get_queryset (self) :
        queryset = Post.objects.filter(owner=self.kwargs.get('user_id'))
        return queryset

class MyProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list (self, request) :
        try :
            queryset = User.objects.filter(email=self.request.user)

        except :
            return Response({'message': ['해당 유저를 찾을 수 없습니다.']}, status=400)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})

        return Response(serializer.data[0])

class UserProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list (self, request, *args, **kwargs) :
        queryset = User.objects.filter(id=kwargs.get('user_id'))
        serializer = self.serializer_class(queryset, many=True, context={'request': request})

        try :
            return Response(serializer.data[0])

        except IndexError :
            return Response({'message': ['해당 유저를 찾을 수 없습니다.']}, status=400)

class UserEmailProfileView (ModelViewSet) :
    serializer_class = UserProfileSerializer

    def list (self, request) :
        queryset = User.objects.filter(email=request.GET.get('email'))
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        
        try :
            return Response(serializer.data[0])

        except IndexError :
            return Response({'message': ['해당 유저를 찾을 수 없습니다.']}, status=400)