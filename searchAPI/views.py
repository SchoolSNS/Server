from authAPI.models import User
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
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
        school_name = self.kwargs.get('query')

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': '881eb3db21cb4cd6affd25cf7c97068c', 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': school_name}

        proxy = {
            "http": "hischool.pythonanywhere.com"
        }

        res = requests.get(url, params=param, proxies=proxy)

        print(res.json())

        return Response([])

class UserSearchView (APIView) :
    pagination_class = LargeResultsSetPagination

    def get (self, request) :
        username = self.kwargs.get('query')
        
        data = User.objects.filter(username=username)

        return Response(data)