from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_skin, name='predict_skin'),
]
