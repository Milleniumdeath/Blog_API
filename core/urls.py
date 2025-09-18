
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="BLOG API",
      default_version='v1',
      description="For learning about DRF",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="milleniumdeath90@gmail.com"),
      license=openapi.License(name="Codial License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)



urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('auth/', include('users.urls')),
   path('', include('main.urls')),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += i18n_patterns(
   path('admin/', admin.site.urls),
)
