from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json

from .serializers import ChatAskSerializer
from .rag_service import ask_acne_chatbot
from .models import ChatLog

class ChatAskAPIView(APIView):
    def post(self, request):
        Serializer = ChatAskSerializer(data=request.data)
        Serializer.is_valid(raise_exception=True)

        question = Serializer.validated_data["question"]
        user_id  = request.data.get("user_id")

        try:
            result = ask_acne_chatbot(question)

            if user_id:
                now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                context = json.dumps([
                    {"role": "user", "content": question,        "time": now},
                    {"role": "ai",   "content": result["answer"],"time": now},
                ], ensure_ascii=False)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT SEQ_CHAT_LOG.NEXTVAL FROM DUAL")
                    next_id = cursor.fetchone()[0]

                ChatLog.objects.create(
                    chat_log_id=next_id,
                    user_id=user_id,
                    context=context
                )

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
