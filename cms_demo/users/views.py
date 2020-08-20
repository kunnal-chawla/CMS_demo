from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import authentication_classes
from .serializers import UserSerializer, RegisterSerializer, ContentSerializer
from .models import Content
from .validators import title_validation, doc_validation, body_validation, summary_validation
from .messages import Messages

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
    parser_class = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user
        content = Content.objects.filter(user=user)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request):
        context = {'email': request.user.email}
        serializer = ContentSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return Response({'message': Messages.code.get('200')})

# Content upload api
@api_view(['POST',])
@authentication_classes([authentication.TokenAuthentication])
def content_upload(request):
    serializer = ContentSerializer(data=request.data, )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)