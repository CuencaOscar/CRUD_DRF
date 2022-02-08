from unicodedata import name
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class Protegida(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"content":"Esta vista esta protegida"})

urlpatterns = [
    path('create/', views.CrudViewSet.as_view({'post': 'crudCreate'})),
    path('read/', views.CrudViewSet.as_view({'get': 'crudRead'})),
    path('update/<str:pk>', views.CrudViewSet.as_view({'post': 'crudUpdate'})),
    path('delete/<str:pk>', views.CrudViewSet.as_view({'delete': 'crudDelete'})),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('protegida/', Protegida.as_view(), name='protegida')
]
