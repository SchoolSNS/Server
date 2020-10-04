from .serializers import 
import requests

key = '881eb3db21cb4cd6affd25cf7c97068c'
url = F'https://open.neis.go.kr/hub/schoolInfo?key={key}&Type=json&pIndex=1&pSize=100&SCHUL_NM={serializer.data['school']}'

requests.get(url)