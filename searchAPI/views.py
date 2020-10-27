from authAPI.serializers import UserProfileSerializer
from authAPI.models import User
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
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
            parsed_data['학교이름'] = raw_data['SCHUL_NM']
            parsed_data['지역'] = raw_data['LCTN_SC_NM']
            
            if raw_data['COEDU_SC_NM'] == '남여공학' :
                parsed_data['남여공학'] = [True]

            elif raw_data['COEDU_SC_NM'] == '남' :
                parsed_data['남여공학'] = [False, '남']

            elif raw_data['COEDU_SC_NM'] == '여' :
                parsed_data['남여공학'] = [False, '여']

            parsed_data['주소'] = raw_data['ORG_RDNMA']
            parsed_data['홈페이지'] = raw_data['HMPG_ADRES']
            parsed_data['학교 유형'] = raw_data['HS_SC_NM']

            parsed_datas.append(parsed_data)
            
            parsed_data = {}

        return Response(parsed_datas)

class UserSearchView (APIView) :
    pagination_class = LargeResultsSetPagination

    def get (self, request) :
        username = self.request.GET.get('query')
        
        users = User.objects.filter(username=username)
        serializer = UserProfileSerializer(data=users, many=True)
        serializer.is_valid(raise_exception=False)

        return Response(serializer.data)

class AllUserView (APIView) :
    pagination_class = LargeResultsSetPagination

    def get (self, request) :
        username = self.request.GET.get('query')
        
        users = User.objects.all()
        serializer = UserProfileSerializer(data=users, many=True)
        serializer.is_valid(raise_exception=False)

        return Response(serializer.data)