from authAPI.serializers import UserProfileSerializer
from authAPI.models import User
from feedAPI.serializers import PostSerializer 
from feedAPI.models import Post
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
from rest_framework.filters import SearchFilter
import requests

class LargeResultsSetPagination (PageNumberPagination) :
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response (self, data) :
        return Response(data)

class SchoolSearchView (APIView) :
    pagination_class = LargeResultsSetPagination

    def get (self, request) :
        school_name = self.request.GET.get('query')

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': settings.SCHOOL_API_KEY, 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': school_name}

        proxy = {
            "http": "hischool.pythonanywhere.com"
        }

        res = requests.get(url, params=param, proxies=proxy)

        raw_datas = res.json().get('schoolInfo')

        if raw_datas == None :
            return Response([], status=404)

        parsed_data = {}
        parsed_datas = []

        for raw_data in raw_datas[1].get('row') :
            parsed_data['name'] = raw_data['SCHUL_NM']
            parsed_data['region'] = raw_data['LCTN_SC_NM']
            
            if raw_data['COEDU_SC_NM'] == '남여공학' :
                parsed_data['concoction'] = [True]

            elif raw_data['COEDU_SC_NM'] == '남' :
                parsed_data['concoction'] = [False, 'boy']

            elif raw_data['COEDU_SC_NM'] == '여' :
                parsed_data['concoction'] = [False, 'girl']

            parsed_data['address'] = raw_data['ORG_RDNMA']
            parsed_data['website'] = raw_data['HMPG_ADRES']
            parsed_data['school_type'] = raw_data['HS_SC_NM']

            parsed_datas.append(parsed_data)
            
            parsed_data = {}

        return Response(parsed_datas)

class UserSearchView (ModelViewSet) :
    pagination_class = LargeResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['username']
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

class AllUserView (APIView) :
    pagination_class = LargeResultsSetPagination

    def get (self, request) :
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)

        return Response(serializer.data)

class PostSearchView (ModelViewSet) :
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['title']
    serializer_class = PostSerializer
    queryset = Post.objects.all()