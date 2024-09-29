from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('climbers/<int:climber_id>/', climber_details),
    path('climbers/<int:climber_id>/add_to_expedition/', add_climber_to_draft_expedition),
    path('expeditions/<int:expedition_id>/delete/', delete_expedition),
    path('expeditions/<int:expedition_id>/', expedition)
]
