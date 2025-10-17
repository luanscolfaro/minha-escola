from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Auth (JWT)
    path("api/auth/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),

    # API schema and docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Apps
    path("api/usuarios/", include("apps.usuarios.urls")),
    path("api/core/", include("apps.core.urls")),
    path("api/academico/", include("apps.academico.urls")),
    path("api/matriculas/", include("apps.matriculas.urls")),
    path("api/financeiro/", include("apps.financeiro.urls")),
    path("api/comunicacao/", include("apps.comunicacao.urls")),
    path("api/documentos/", include("apps.documentos.urls")),
]
