from django.urls import path
from .views import ChatAskAPIView
# ChatAskAPIView.as_view() => ask/ 요청이 오면 ChatAskAPIView 응답해야 하는데
# APIView 상속받아서 마치 Dao.getDao() 싱글톤 처럼 뷰로 생성해주는 역할을 함
urlpatterns = [
    path("ask/", ChatAskAPIView.as_view(), name="chat-ask"),
]