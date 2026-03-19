from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatAskSerializer
from .rag_service import ask_acne_chatbot
# APIView 상속 rest_framwork RESTAPI 클래스 뷰
# RestFulAPI - post, get, put, delete 등을 직접 사용할 수 있다
class ChatAskAPIView(APIView):
    print("hello")
    def post(self, request):
        Serializer = ChatAskSerializer(data=request.data)
        # ChatField에서 만들었던 유효성 체크, 빈문자열 허용 안 하고, 500 등 체크
        # 조건에 안 맞으면 자바에서의 throw와 같은 역할
        Serializer.is_valid(raise_exception=True)

        question = Serializer.validated_data["question"]

        try:
            result = ask_acne_chatbot(question)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
