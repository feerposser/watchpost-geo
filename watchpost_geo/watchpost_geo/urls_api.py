from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from core.api.viewsets import ViewSetCidade
from core.api.cbv_watchpost_geo import WatchpostGeocode

router = routers.DefaultRouter()
router.register(r'cidades', ViewSetCidade, base_name="A")


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token),
    path('watchpostgeo/', WatchpostGeocode.as_view()),
    path('', include(router.urls))
]
