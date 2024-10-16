from rest_framework import serializers

from .models import *


class ClimberSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, climber):
        return climber.image.url.replace("minio", "localhost", 1)
        
    class Meta:
        model = Climber
        fields = "__all__"


class ClimberItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField('get_value')

    def get_image(self, climber):
        return climber.image.url.replace("minio", "localhost", 1)

    def get_value(self, climber):
        return self.context.get("value")

    class Meta:
        model = Climber
        fields = ("id", "name", "image", "value")


class ExpeditionsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, expedition):
        return expedition.owner.username

    def get_moderator(self, expedition):
        if expedition.moderator:
            return expedition.moderator.username

        return ""

    class Meta:
        model = Expedition
        fields = "__all__"


class ExpeditionSerializer(serializers.ModelSerializer):
    climbers = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, expedition):
        return expedition.owner.username

    def get_moderator(self, expedition):
        return expedition.moderator.username if expedition.moderator else ""
    
    def get_climbers(self, expedition):
        items = ClimberExpedition.objects.filter(expedition=expedition)
        return [ClimberItemSerializer(item.climber, context={"value": item.value}).data for item in items]
    
    class Meta:
        model = Expedition
        fields = "__all__"


class ClimberExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimberExpedition
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)