from .models import User
from .serializers import registerSerializer, loginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import requests

class registerView (GenericAPIView) :
    serializer_class = registerSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)

        data = serializer.validated_data

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': '881eb3db21cb4cd6affd25cf7c97068c', 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': data['school']}

        res = requests.get(url, params=param)

        if res.status_code == 200 :
            serializer.save()
            return Response({'message': '회원가입에 성공했습니다.'}, status=201)

        else :
            return Response({'message': '학교이름을 확인해주세요.'}, status=400)

class loginView (GenericAPIView) :
    serializer_class = loginSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            user = User.objects.get(email=serializer.data['email'])

        except User.DoesNotExist :
            return Response({'message': '이메일을 정확히 입력했는지 확인하여 주세요.'}, status=401)

        if user.check_password(raw_password=serializer.data['password']) == False :
            return Response({'message': '비밀번호를 정확히 입력했는지 확인하여 주세요.'}, status=401)

        try :
            token = Token.objects.create(user=user)

        except :
            token = Token.objects.get(user=user)

        return Response({'token': F'{token.key}'}, status=200)