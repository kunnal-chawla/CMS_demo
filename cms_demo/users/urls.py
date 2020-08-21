from .views import registration_view, ContentView, AdminContentView, ContentList
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Author End-points
    path('author/registeration/', registration_view, name='register'),
    path('author/login/', obtain_auth_token, name='login'),
    path('author/content/create', ContentView.as_view(), name='create'),
    path('author/content/my-content', ContentView.as_view(), name='view'),
    path('author/content/update/<int:pk>/', ContentView.as_view(), name='update'),
    path('author/content/delete/<int:pk>/', ContentView.as_view(), name='delete'),
    path('author/content/filter', ContentList.as_view(), name='filter'),

    # Admin End-points
    path('admin/content/view/all-content', AdminContentView.as_view(), name='view'),
    path('admin/content/update/<int:pk>/', AdminContentView.as_view(), name='update'),
    path('admin/content/delete/<int:pk>/', AdminContentView.as_view(), name='delete'),
]
