from django.urls import path
from .views import *
from .models import *
urlpatterns = [
    # path('articles/', ArticleListAPIView.as_view()),
    path('articles/', ArticleAPIView.as_view()),
    path('articles/<int:pk>', ArticleRetrieveAPIView.as_view()),
    path('articles/create/', ArticleCreateAPIView.as_view()),
    path('articles/mine/', MyArticlesAPIView.as_view(),),
]
