from django.http import Http404, HttpResponseNotAllowed

from rest_framework import authentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .generic_variables import Groups
from .models import Content
from .messages import Messages
from .serializers import UserSerializer, RegisterSerializer, ContentSerializer


# Registerion API
@api_view(['POST',])
def registration_view(request):
    """
    This API is used to Register new user as an Author into cms system
    :param request: mobile_number, full_name, password, pin_code
    :return: Response object

    Example:
    Endpoint: http://localhost:8000/api/author/registeration/

    Request:
    {
    "mobile_number": 9889878987,
    "full_name": "kunnal chawla",
    "email": "kunnal@gmail.com",
    "password": "Test@123",
    "pin_code": 400044
    }

    Response:
    {
        "user": {
            "mobile_number": 9889878987,
            "full_name": "knnal chawla",
            "email": "knnal@gmail.com"
    },
        "token": "8d5c91ea256d2234a0df09cb98f58d10da8d7b5e"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        return Response({
            "user": UserSerializer(user).data,
            "token": token
        })
    return Response(serializer.errors)


class ContentView(APIView):
    """
        This is a class based APIView designed to perform all the CRUD operation
        required by custom user (Author) on its content
        Endpoints:
            http://localhost:8000/api/author/content/create
            http://localhost:8000/api/author/content/my-content
            http://localhost:8000/api/author/content/update/1/
            http://localhost:8000/api/author/content/delete/1/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise Http404

    def get(self, request):
        if not request.user.groups.filter(name=Groups.Author).exists():
            return HttpResponseNotAllowed(('GET',))
        user = request.user
        content = Content.objects.filter(user=user)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.groups.filter(name=Groups.Author).exists():
            return HttpResponseNotAllowed(('POST',))
        context = {'email': request.user.email}
        serializer = ContentSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, pk):
        if not request.user.groups.filter(name=Groups.Author).exists():
            return HttpResponseNotAllowed(('PUT',))
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        if not request.user.groups.filter(name=Groups.Author).exists():
            return HttpResponseNotAllowed(('DELETE',))
        content = self.get_object(pk)
        content.delete()
        return Response({'message': Messages.code.get('200')})


class AdminContentView(APIView):
    """
        This is a class based APIView designed to perform all the Read, Write
        and delete operation required by custom user (CMS Admin) on content
        Endpoints:
            http://localhost:8000/api/admin/content/view/all-content
            http://localhost:8000/api/admin/content/update/1/
            http://localhost:8000/api/admin/content/delete/1/
        """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise Http404

    def get(self, request):
        if not request.user.groups.filter(name=Groups.Admin).exists():
            return HttpResponseNotAllowed(('GET',))
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.groups.filter(name=Groups.Admin).exists():
            return HttpResponseNotAllowed(('PUT',))
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        if not request.user.groups.filter(name=Groups.Admin).exists():
            return HttpResponseNotAllowed(('DELETE',))
        content = self.get_object(pk)
        content.delete()
        return Response({'message': Messages.code.get('200')})


class ContentList(generics.ListAPIView):
    """
        This class is based on ListAPIView which enables a user(Author) to
        filter their content depending upon content title, content summary,
        content body or combination of all/some

        Example:
            http://localhost:8000/api/author/content/filter?title=XXXX&body=XXXX&summary=XXXX
            http://localhost:8000/api/author/content/filter?title=XXXX&summary=XXXX
            http://localhost:8000/api/author/content/filter?summary=XXXX
            http://localhost:8000/api/author/content/filter
    """
    model = Content
    serializer_class = ContentSerializer

    def get_queryset(self):
        queryset = Content.objects.filter(user=self.request.user)
        title = self.request.query_params.get("title")
        summary = self.request.query_params.get("summary")
        body = self.request.query_params.get("body")
        if title:
            queryset = queryset.filter(title__icontains=title)
        if summary:
            queryset = queryset.filter(summary__icontains=summary)
        if body:
            queryset = queryset.filter(body__icontains=body)
        return queryset