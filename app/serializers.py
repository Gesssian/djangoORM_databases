from rest_framework import serializers

from .models import *


class ClimberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climber
        fields = "__all__"


class ExpeditionSerializer(serializers.ModelSerializer):
    climbers = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(selfself, expedition):
        return expedition.owner.username

    def get_moderator(selfself, expedition):
        if expedition.moderator:
            return expedition.moderator.username
            
    def get_climbers(self, expedition):
        items = ClimberExpedition.objects.filter(expedition=expedition)
        serializer = ClimberSerializer([item.climber for item in items], many=True)
        return serializer.data

    class Meta:
        model = Expedition
        fields = '__all__'


class ExpeditionsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, expedition):
        return expedition.owner.username

    def get_moderator(self, expedition):
        if expedition.moderator:
            return expedition.moderator.username

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
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'password', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user