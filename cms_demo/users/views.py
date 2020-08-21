from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework.views import APIView
from django.http import Http404, HttpResponseNotAllowed
from .serializers import UserSerializer, RegisterSerializer, ContentSerializer
from .models import Content
from .messages import Messages
from .generic_variables import Groups
from rest_framework import generics


# Register API
@api_view(['POST',])
def registration_view(request):
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