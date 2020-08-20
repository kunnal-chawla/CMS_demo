from .views import registration_view, ContentView, content_upload
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('author/registeration/', registration_view, name='register'),
    path('author/login/', obtain_auth_token, name='login'),
    path('author/content/create', ContentView.as_view(), name='create'),
    path('author/content/my-content', ContentView.as_view(), name='view'),
    path('author/content/update/<int:pk>/', ContentView.as_view(), name='update'),
    path('author/content/delete/<int:pk>/', ContentView.as_view(), name='delete'),
]
