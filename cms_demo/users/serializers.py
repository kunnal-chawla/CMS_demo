from rest_framework import serializers
from .models import CustomUser, Content
from django.contrib.auth.models import Group
from .validators import mobile_number_validator, \
    email_validator, full_name_validator, doc_validation,\
    password_validator, pin_code_validator, \
    title_validation, body_validation, summary_validation


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'full_name', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.IntegerField(validators=[mobile_number_validator])
    full_name = serializers.CharField(validators=[full_name_validator])
    email = serializers.CharField(validators=[email_validator])
    password = serializers.CharField(validators=[password_validator])
    pin_code = serializers.CharField(validators=[pin_code_validator])
    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'full_name', 'email', 'password', 'pin_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        groups = Group.objects.get(name='Author')
        groups.user_set.add(user)
        return user


# Content Serializer
class ContentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(validators=[title_validation])
    body = serializers.CharField(validators=[body_validation])
    summary = serializers.CharField(validators=[summary_validation])
    document = serializers.FileField(validators=[doc_validation])

    def create(self, validated_data):
        email = self.context.get('email')
        user_instance = CustomUser.objects.get(email=email)
        content = Content.objects.create(**validated_data, user=user_instance)
        return content

    def update(self, instance, validated_data):
        """
        Update and return an existing `content` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.document = validated_data.get('document', instance.document)
        instance.save()
        return instance

    class Meta:
        model = Content
        fields = ('id', 'title', 'summary', 'body', 'document', 'user')