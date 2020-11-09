from rest_framework import serializers
from .models import Post, Comment, Image, Like, CommentImage
from authAPI.models import User
from authAPI.serializers import UserProfileSerializer
from datetime import datetime
from django.conf import settings
import requests
import random

class ImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = Image
        fields = ('image', )

class CommentImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = CommentImage
        fields = ('image', )

class CommentSerializer (serializers.ModelSerializer) :
    comment_id = serializers.IntegerField(source='id', read_only=True)
    owner = UserProfileSerializer(read_only=True)
    comment_images = CommentImageSerializer(many=True, read_only=True)

    class Meta :
        model = Comment
        fields = ('comment_id', 'owner', 'content', 'comment_images', 'created_at')

    def create (self, validated_data) :
        comment = Comment.objects.create(**validated_data, created_at=str(datetime.now().astimezone().replace(microsecond=0).isoformat()))
        images_data = self.context['request'].FILES

        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}')

            if image_data is None :
                break

            CommentImage.objects.create(comment=comment, image=image_data)

        return comment

    def update (self, instance, validated_data) :
        images_data = self.context['request'].FILES
        comment_images = CommentImage.objects.filter(comment=instance)
        
        new_images_count = len(images_data)
        original_images_count = len(comment_images)

        new_image_big_end = False
        new_image_small_end = False

        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}', None)

            if original_images_count < new_images_count :
                if original_images_count == 0 :
                    new_image_big_end = True

                if new_image_big_end is False :
                    comment_images[i-1].image = image_data
                    comment_images[i-1].save(update_fields=('image', ))

                    if comment_images[i-1] == comment_images[original_images_count - 1] :
                        new_image_big_end = True

                elif new_image_big_end is True :
                    if image_data is not None :
                        CommentImage.objects.create(comment=instance, image=image_data)
                    else :
                        break

            elif original_images_count > new_images_count :
                if new_image_small_end == False : 

                    if image_data is not None :
                        comment_images[i-1].image = image_data
                        comment_images[i-1].save(update_fields=('image', ))

                    if image_data is None :
                        comment_images[i-1].delete()

                        if comment_images[i-1] == comment_images[original_images_count - 1] :
                            new_image_small_end = True

                elif new_image_small_end == True :
                    break

            else :
                if image_data == None :
                    break

                comment_images[i-1].image = image_data
                comment_images[i-1].save(update_fields=('image', ))

        content = validated_data.get('content', None)

        if content is not None :
            instance.content = content

        instance.save(update_fields=('content', ))

        return instance

    def to_representation (self, instance) :
        data = super().to_representation(instance)
        images = data.pop('comment_images')
        images_array = [image.get('image') for image in images]
        data.update({'image_urls': images_array})

        return data

    def validate (self, attrs) :
        content = attrs.get('content', '')

        error = {}

        if content is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        return attrs

class LikeSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Like
        fields = '__all__'

    def create (self, validated_data) :
        return Like.objects.create(**validated_data)

class PostSerializer (serializers.ModelSerializer) :
    owner = UserProfileSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    images = ImageSerializer(read_only=True, many=True)
    liked_people = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta :
        model = Post
        fields = ('id', 'owner', 'title', 'content', 'school', 'images', 'like_count', 'comment_count', 'liked_people', 'created_at', 'comments', 'is_liked')

    def get_is_liked (self, obj) :
        user = self.context['request'].user
        
        try :
            like = Like.objects.get(liked_people=user, post=obj)

        except Like.DoesNotExist :
            return False

        return True

    def create (self, validated_data) :
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data, created_at=str(datetime.now().astimezone().replace(microsecond=0).isoformat()))
        
        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}')

            if image_data is None :
                break

            Image.objects.create(post=post, image=image_data)

        return post

    def update (self, instance, validated_data) :
        images_data = self.context['request'].FILES
        images = Image.objects.filter(post=instance)
        
        new_images_count = len(images_data)
        original_images_count = len(images)

        new_image_big_end = False
        new_image_small_end = False

        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}', None)

            if original_images_count < new_images_count :
                if original_images_count == 0 :
                    new_image_big_end = True

                if new_image_big_end is False :
                    images[i-1].image = image_data
                    images[i-1].save(update_fields=('image', ))

                    if images[i-1] == images[original_images_count - 1] :
                        new_image_big_end = True

                elif new_image_big_end is True :
                    if image_data is not None :
                        Image.objects.create(post=instance, image=image_data)
                    else :
                        break

            elif original_images_count > new_images_count :
                if new_image_small_end == False : 

                    if image_data is not None :
                        images[i-1].image = image_data
                        images[i-1].save(update_fields=('image', ))

                    if image_data is None :
                        images[i-1].delete()

                        if images[i-1] == images[original_images_count - 1] :
                            new_image_small_end = True

                elif new_image_small_end == True :
                    break

            else :
                if image_data == None :
                    break
                
                images[i-1].image = image_data
                images[i-1].save(update_fields=('image', ))

        title = validated_data.get('title', None)
        content = validated_data.get('content', None)
        
        instance.title = title
        instance.content = content
        
        instance.save(update_fields=('title', 'content', ))

        return instance

    def to_representation (self, instance) :
        data = super().to_representation(instance)

        images = data.pop('images')
        liked_people = data.pop('liked_people')
        comments = data.pop('comments')

        images_array = [image.get('image') for image in images]
        liked_people_array = [liked_person.get('liked_people') for liked_person in liked_people]
        comments_array = [comment for comment in comments]
        
        if comments_array != [] :
            if len(comments_array) == 1 or len(comments_array) == 2:
                data.update({'image_urls': images_array, 'liked_people': liked_people_array, 'comment_preview': comments_array})

            else :
                comments_preview_array = []

                for i in range(2) :
                    random_comment = random.choice(comments_array)
                    comments_array.remove(random_comment)
                    comments_preview_array.append(random_comment)

                data.update({'image_urls': images_array, 'liked_people': liked_people_array, 'comment_preview': comments_preview_array})

        else :
            data.update({'image_urls': images_array, 'liked_people': liked_people_array})
                    
        return data

    def validate (self, attrs) :
        title = attrs.get('title', '')
        content = attrs.get('text', '')
        tag = attrs.get('tag', '')
        school = attrs.get('school', '')

        error = {}

        if title is None and content is None :
            error['message'] = '제목과 본문은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        if title is None :
            error['message'] = '제목은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        if content is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'    
            raise serializers.ValidationError(error)

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': settings.SCHOOL_API_KEY, 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': school}

        res = requests.get(url, params=param)

        if res.json()['RESULT'].get('MESSAGE', None) is not None :
            error['message'] = '학교 이름을 확인해주세요.'
            raise serializers.ValidationError(error)

        return attrs