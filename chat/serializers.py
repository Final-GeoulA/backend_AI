from rest_framework import serializers
# Django Rest Framework의 Serializer 객체를 상속 받아 직렬화 가능한 클래스로 정의
class ChatAskSerializer(serializers.Serializer):
    # ChatField 문자열 데이터 직렬화 시키기 위한 함수
    # allow_blank = False: 빈 문자열을 허용하지 않겠다
    # max_length: 문자열의 최대 길이
    # {'question': '오늘 메뉴는 뭐야'}
    question = serializers.CharField(required=True, allow_blank=False, max_length=500)