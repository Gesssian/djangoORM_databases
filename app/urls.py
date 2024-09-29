from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('climbers/<int:climber_id>/', climber),
    path('expeditions/<int:expedition_id>/', expedition),
]