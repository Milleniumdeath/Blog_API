from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from users.views import *

#JWT Urls
urlpatterns = [
    path('token/', token_obtain_pair , name='token_obtain_pair'),
    path('token/refresh/', token_refresh , name='token_refresh'),

]

#USER Urls
urlpatterns += [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('my-account/', UserRetrieveAPIView.as_view(), name='user-details'),
    path('my-account/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('my-account/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('my-account/change-password/', UserChangePasswordAPIView.as_view(), name='change-password'),
]