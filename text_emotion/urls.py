from django.urls import path
from . import views
urlpatterns = [
    path("Board_emotion",views.Board_emotion),
]