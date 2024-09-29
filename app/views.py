import requests
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_expedition():
    return Expedition.objects.filter(status=1).first()


def get_user():
    return User.objects.filter(is_superuser=False).first()


def get_moderator():
    return User.objects.filter(is_superuser=True).first()


@api_view(["GET"])
def search_climbers(request):
    query = request.GET.get("query", "")

    climbers = Climber.objects.filter(status=1).filter(name__icontains=query)

    serializer = ClimberSerializer(climbers, many=True)

    draft_expedition = get_draft_expedition()

    resp = {
        "climbers": serializer.data,
        "draft_expedition": draft_expedition.pk if draft_expedition else None
    }

    return Response(resp)


@api_view(["GET"])
def get_climber_by_id(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)
    serializer = ClimberSerializer(climber, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_climber(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)

    image = request.data.get("image")
    if image is not None:
        climber.image = image
        climber.save()

    serializer = ClimberSerializer(climber, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_climber(request):
    Climber.objects.create()

    climbers = Climber.objects.filter(status=1)
    serializer = ClimberSerializer(climbers, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_climber(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)
    climber.status = 2
    climber.save()

    climbers = Climber.objects.filter(status=1)
    serializer = ClimberSerializer(climbers, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_climber_to_expedition(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)

    draft_expedition = get_draft_expedition()

    if draft_expedition is None:
        draft_expedition = Expedition.objects.create()
        draft_expedition.owner = get_user()
        draft_expedition.date_created = timezone.now()
        draft_expedition.save()

    if ClimberExpedition.objects.filter(expedition=draft_expedition, climber=climber).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    item = ClimberExpedition.objects.create()
    item.expedition = draft_expedition
    item.climber = climber
    item.save()

    serializer = ExpeditionSerializer(draft_expedition, many=False)

    return Response(serializer.data["climbers"])


@api_view(["GET"])
def get_climber_image(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)
    response = requests.get(climber.image.url.replace("localhost", "minio"))

    return HttpResponse(response, content_type="image/png")


@api_view(["PUT"])
def update_climber_image(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)

    image = request.data.get("image")
    if image is not None:
        climber.image = image
        climber.save()

    serializer = ClimberSerializer(climber)

    return Response(serializer.data)


@api_view(["GET"])
def search_expeditions(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    expeditions = Expedition.objects.exclude(status__in=[1, 5])

    if status > 0:
        expeditions = expeditions.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        expeditions = expeditions.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        expeditions = expeditions.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = ExpeditionsSerializer(expeditions, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_expedition_by_id(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)
    serializer = ExpeditionSerializer(expedition, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_expedition(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)
    serializer = ExpeditionSerializer(expedition, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)

    if expedition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition.status = 2
    expedition.date_formation = timezone.now()
    expedition.save()

    serializer = ExpeditionSerializer(expedition, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition = Expedition.objects.get(pk=expedition_id)

    if expedition.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition.date_complete = timezone.now()
    expedition.status = request_status
    expedition.moderator = get_moderator()
    expedition.save()

    serializer = ExpeditionSerializer(expedition, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_expedition(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)

    if expedition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition.status = 5
    expedition.save()

    serializer = ExpeditionSerializer(expedition, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_climber_from_expedition(request, expedition_id, climber_id):
    if not ClimberExpedition.objects.filter(expedition_id=expedition_id, climber_id=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ClimberExpedition.objects.get(expedition_id=expedition_id, climber_id=climber_id)
    item.delete()

    expedition = Expedition.objects.get(pk=expedition_id)

    serializer = ExpeditionSerializer(expedition, many=False)
    climbers = serializer.data["climbers"]

    if len(climbers) == 0:
        expedition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(climbers)


@api_view(["PUT"])
def update_climber_in_expedition(request, expedition_id, climber_id):
    if not ClimberExpedition.objects.filter(climber_id=climber_id, expedition_id=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ClimberExpedition.objects.get(climber_id=climber_id, expedition_id=expedition_id)

    serializer = ClimberExpeditionSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, data=request.data, many=False, partial=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data)