from re import search

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import *

# class ArticleListAPIView(ListAPIView):
#     queryset = Article.objects.filter(published=True)
#     serializer_class = ArticleSafeSerializer
class ArticleAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                description='Search by title or context.',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='published',
                description='Filter by published status ',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                name='ordering',
                description='Ordering by title, views, created_at at (asc, desc) ',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['title', 'views', 'created_at', '-title', '-views', '-created_at'],
            ),
        ]
    )
    def get(self, request):
        articals = Article.objects.all()
        search = request.GET.get('search')
        published = request.GET.get('published')
        if published:
            if published.lower() == 'true':
                articals = articals.filter(published=True)
            elif published.lower() == 'false':
                articals = articals.filter(published=False)

        if search:
            articals = articals.filter(Q(title__icontains=search) | Q(context__icontains=search))

        ordering = request.GET.get('ordering')
        if ordering :
            try:
                articals = articals.order_by(ordering)
            except Exception as e:
                return Response(
                    {
                        'success': False,
                        'error': 'Ordering only by title, views, created_at at with (asc, desc)'
                    }
                )

        serializer = ArticleSafeSerializer(articals, many=True)
        return Response(serializer.data)

class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.filter(published=True)
    serializer_class = ArticleSafeSerializer
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if self.request.user != article.author:
            article.views +=1
            article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)


# class ArticleCreateAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

class ArticleCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=ArticleSerializer
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyArticlesAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Article.objects.all()
    serializer_class = ArticleSafeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'context']
    ordering_fields = ['title', 'created_at', 'views']

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['title', 'views', 'created_at', '-title', '-views', '-created_at'],
                description='Ordering by title, views, created_at at (asc, desc) ',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        super().get(*args, **kwargs)
