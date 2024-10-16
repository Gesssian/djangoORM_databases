from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_expedition(request):
    user = identity_user(request)

    if user is None:
        return None

    expedition = Expedition.objects.filter(owner=user).filter(status=1).first()

    return expedition


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
def search_climbers(request):
    climber_name = request.GET.get("climber_name", "")

    climbers = Climber.objects.filter(status=1)

    if climber_name:
        climbers = climbers.filter(name__icontains=climber_name)

    serializer = ClimberSerializer(climbers, many=True)

    draft_expedition = get_draft_expedition(request)

    resp = {
        "climbers": serializer.data,
        "climbers_count": ClimberExpedition.objects.filter(expedition=draft_expedition).count() if draft_expedition else None,
        "draft_expedition_id": draft_expedition.pk if draft_expedition else None
    }

    return Response(resp)


@api_view(["GET"])
def get_climber_by_id(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)
    serializer = ClimberSerializer(climber)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
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
@permission_classes([IsModerator])
def create_climber(request):
    climber = Climber.objects.create()

    serializer = ClimberSerializer(climber)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_climber(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)
    climber.status = 2
    climber.save()

    climber = Climber.objects.filter(status=1)
    serializer = ClimberSerializer(climber, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_climber_to_expedition(request, climber_id):
    if not Climber.objects.filter(pk=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    climber = Climber.objects.get(pk=climber_id)

    draft_expedition = get_draft_expedition(request)

    if draft_expedition is None:
        draft_expedition = Expedition.objects.create()
        draft_expedition.date_created = timezone.now()
        draft_expedition.owner = identity_user(request)
        draft_expedition.save()

    if ClimberExpedition.objects.filter(expedition=draft_expedition, climber=climber).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = ClimberExpedition.objects.create()
    item.expedition = draft_expedition
    item.climber = climber
    item.save()

    serializer = ExpeditionSerializer(draft_expedition)
    return Response(serializer.data["climbers"])


@api_view(["POST"])
@permission_classes([IsModerator])
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
@permission_classes([IsAuthenticated])
def search_expeditions(request):
    status_id = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    expeditions = Expedition.objects.exclude(status__in=[1, 5])

    user = identity_user(request)
    if not user.is_staff:
        expeditions = expeditions.filter(owner=user)

    if status_id > 0:
        expeditions = expeditions.filter(status=status_id)

    if date_formation_start and parse_datetime(date_formation_start):
        expeditions = expeditions.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        expeditions = expeditions.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = ExpeditionsSerializer(expeditions, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_expedition_by_id(request, expedition_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)
    serializer = ExpeditionSerializer(expedition)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=ExpeditionSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_expedition(request, expedition_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)
    serializer = ExpeditionSerializer(expedition, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, expedition_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)

    expedition.status = 2
    expedition.date_formation = timezone.now()
    expedition.save()

    serializer = ExpeditionSerializer(expedition)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, expedition_id):
    if not Expedition.objects.filter(pk=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition = Expedition.objects.get(pk=expedition_id)

    if expedition.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition.status = request_status
    expedition.date_complete = timezone.now()
    expedition.moderator = identity_user(request)
    expedition.save()

    serializer = ExpeditionSerializer(expedition)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_expedition(request, expedition_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    expedition = Expedition.objects.get(pk=expedition_id)

    if expedition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    expedition.status = 5
    expedition.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_climber_from_expedition(request, expedition_id, climber_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ClimberExpedition.objects.filter(expedition_id=expedition_id, climber_id=climber_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ClimberExpedition.objects.get(expedition_id=expedition_id, climber_id=climber_id)
    item.delete()

    expedition = Expedition.objects.get(pk=expedition_id)

    serializer = ExpeditionSerializer(expedition)
    climbers = serializer.data["climbers"]

    if len(climbers) == 0:
        expedition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(climbers)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_climber_expedition(request, expedition_id, climber_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ClimberExpedition.objects.filter(climber_id=climber_id, expedition_id=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ClimberExpedition.objects.get(climber_id=climber_id, expedition_id=expedition_id)

    serializer = ClimberExpeditionSerializer(item)

    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=ClimberExpeditionSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_climber_in_expedition(request, expedition_id, climber_id):
    user = identity_user(request)

    if not Expedition.objects.filter(pk=expedition_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ClimberExpedition.objects.filter(climber_id=climber_id, expedition_id=expedition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ClimberExpedition.objects.get(climber_id=climber_id, expedition_id=expedition_id)

    serializer = ClimberExpeditionSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True)

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='PUT', request_body=UserSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = identity_user(request)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
