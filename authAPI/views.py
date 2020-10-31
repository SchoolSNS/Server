from .models import User
from feedAPI.models import Post, Comment
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from feedAPI.serializers import PostSerializer, CommentSerializer
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

        data = serializer.validated_data

        proxy = {
            "http": "hischool.pythonanywhere.com"
        }

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': settings.SCHOOL_API_KEY, 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': data['school']}

        res = requests.get(url, params=param, proxies=proxy)

        if res.status_code == 200 :
            serializer.save()
            return Response({'success': '회원가입에 성공했습니다.'}, status=201)

        else :
            return Response({'message': ['학교이름을 확인해주세요.']}, status=400)

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
        queryset = Comment.objects.filter(owner=self.kwargs.get('user_id'))
        return queryset

class MyProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list (self, request) :
        queryset = User.objects.filter(email=self.request.user)
        serializer = self.serializer_class(queryset, many=True)

        for i in serializer.data :
            data = i

        return Response(data)

class UserProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list (self, request) :
        queryset = User.objects.filter(id=self.kwargs.get('user_id'))
        serializer = self.serializer_class(queryset, many=True)

        for i in serializer.data :
            data = i
        
        return Response(data)