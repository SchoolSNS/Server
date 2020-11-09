from .models import Post, Comment, Image, Like
from authAPI.models import User
from authAPI.serializers import UserProfileSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import requests
from django.conf import settings

class LargeResultsSetPagination (PageNumberPagination) :
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response (self, data) :
        return Response(data)

class CreatePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    is_saved = False

    def perform_create (self, serializer) :
        serializer.save(owner=self.request.user)

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '게시물이 저장 되었습니다.'}, status=201)

class ReadListPostView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-pk')
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

class ReadFilterBySchoolPostView (ModelViewSet) :
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset (self) :
        user = self.request.user
        queryset = Post.objects.filter(school=user.school).order_by('-pk')
        return queryset

class ReadOnePostView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class UpdateDeletePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '게시물이 수정 되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '게시물이 삭제 되었습니다.'}, status=200)

class CreateCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def perform_create (self, serializer) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)
        serializer.save(owner=self.request.user, post=post)

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        return Response({'success': '댓글 작성이 완료되었습니다.'}, status=201)

class ReadCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('pk')

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

class UpdateDeleteCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '댓글 작성이 완료되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '댓글이 삭제 되었습니다.'}, status=200)

class ReadLikerView (ModelViewSet) :
    serializer_class = UserProfileSerializer
    queryset = Like.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def list (self, request, *args, **kwargs) :
        likers = self.queryset.filter(post=self.kwargs.get('post_id')).values()
        data = []

        for liker in likers :
            userId = liker.get('liked_people_id')
            user = User.objects.filter(pk=userId).order_by('pk')
            serializer = self.serializer_class(user, many=True)
            
            if serializer.data != [] :
                data.append(serializer.data[0])

        return Response(data)

class LikeView (APIView) :
    permission_classes = [IsAuthenticated]

    def post (self, request, post_id) :
        post = Post.objects.get(pk=post_id)
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            like = Like.objects.get(post=post, liked_people=self.request.user)

        except Like.DoesNotExist :
            serializer.save(liked_people=self.request.user, post=post)
            return Response({'success': '해당 게시글에 좋아요를 눌렀습니다.'}, status=200)

        return Response({'message': ['이미 좋아요를 누른 게시물 입니다.']}, status=400)

    def get (self, request, post_id) :
        post = Post.objects.get(pk=post_id)

        try :
            like = Like.objects.get(post=post, liked_people=self.request.user)

        except Like.DoesNotExist :
            return Response({'message': ['좋아요 하지 않음.']}, status=400)

        return Response({'success': '좋아요함'}, status=200)

    
    def delete (self, request, post_id) :
        post = Post.objects.get(pk=post_id)

        try :
            like = Like.objects.get(post=post, liked_people=self.request.user)

        except Like.DoesNotExist :
            return Response({'message': ['해당 게시글에 좋아요 되어 있지 않습니다.']}, status=400)

        like.delete()

        return Response({'success': '해당 게시글에 대한 좋아요가 취소 되었습니다.'}, status=200)