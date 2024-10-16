from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/climbers/', search_climbers),  # GET
    path('api/climbers/<int:climber_id>/', get_climber_by_id),  # GET
    path('api/climbers/<int:climber_id>/update/', update_climber),  # PUT
    path('api/climbers/<int:climber_id>/update_image/', update_climber_image),  # POST
    path('api/climbers/<int:climber_id>/delete/', delete_climber),  # DELETE
    path('api/climbers/create/', create_climber),  # POST
    path('api/climbers/<int:climber_id>/add_to_expedition/', add_climber_to_expedition),  # POST

    # Набор методов для заявок
    path('api/expeditions/', search_expeditions),  # GET
    path('api/expeditions/<int:expedition_id>/', get_expedition_by_id),  # GET
    path('api/expeditions/<int:expedition_id>/update/', update_expedition),  # PUT
    path('api/expeditions/<int:expedition_id>/update_status_user/', update_status_user),  # PUT
    path('api/expeditions/<int:expedition_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/expeditions/<int:expedition_id>/delete/', delete_expedition),  # DELETE

    # Набор методов для м-м
    path('api/expeditions/<int:expedition_id>/climbers/<int:climber_id>/', get_climber_expedition),  # GET
    path('api/expeditions/<int:expedition_id>/update_climber/<int:climber_id>/', update_climber_in_expedition),  # PUT
    path('api/expeditions/<int:expedition_id>/delete_climber/<int:climber_id>/', delete_climber_from_expedition),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/users/register/", register),  # POST
    path("api/users/login/", login),  # POST
    path("api/users/logout/", logout),  # POST
    path("api/users/<int:user_id>/update/", update_user)  # PUT
]
