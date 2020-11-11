import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DeviceToken, Description
from authAPI.models import User
from feedAPI.models import Post
from .serializers import DeviceTokenSerializer, DescriptionSerializer

class DeviceTokenView (APIView) :
    permission_classes = [IsAuthenticated]

    def post (self, request) :
        serializer = DeviceTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response({'success': '토큰을 저장하였습니다.'})
    
    def put (self, request) :
        try :
            device_token = DeviceToken.objects.get(user=self.request.user)
        
        except DeviceToken.DoesNotExist :
            return Response({'message': ['디바이스 토큰을 찾을 수 없습니다.']}, status=400)

        serializer = DeviceTokenSerializer(device_token, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': '토큰을 저장하였습니다.'})

class CommentPushAlarmView (APIView) :
    permission_classes = [IsAuthenticated]

    def get (self, request) :

        if not firebase_admin._apps :
            cred = credentials.Certificate('push_alarm\hischool-33fa8-firebase-adminsdk-v5fxu-79c7bfc2c4.json')
            default_app = firebase_admin.initialize_app(cred)

        postId = request.GET.get('post_id')
        post = Post.objects.get(pk=postId)

        post_owner = User.objects.get(username=post.owner.username)
        registration_token = DeviceToken.objects.get(user=post_owner)

        comment_writer = User.objects.get(email=self.request.user)

        title = F'{comment_writer.username}님이 당신의 게시글에 댓글을 달았습니다.'

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body="예약승인되었습니다.",
            ),
            token=registration_token,
        )

        response = messaging.send(message)

        data = QueryDict(F'title={title}')

        serializer = DescriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)

        return Response({'success': '성공적으로 알람이 전송되었습니다.'})

class GetAllNotificationView (APIView) :
    permission_classes = [IsAuthenticated]

    def get (self, request) :
        user = User.objects.get(email=self.request.user)
        posts = Post.objects.filter(owner=user)
        data = []
        
        if posts != [] :
            for post in posts :
                description = Description.objects.filter(post=post)
                serializer = DescriptionSerializer(post, many=True)

                data.append(serializer.data)

        return Response(data)