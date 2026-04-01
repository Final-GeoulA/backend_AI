from django.urls import path
from . import views

urlpatterns = [
    path('compare_face',views.compare_face)
]