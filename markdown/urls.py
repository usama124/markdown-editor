from django.urls import path

from markdown.views import DocumentAPIView

urlpatterns = [
    path('document/<pk>', DocumentAPIView.as_view()),
]
