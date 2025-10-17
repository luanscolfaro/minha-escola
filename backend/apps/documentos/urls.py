from django.urls import path
from .views import HealthCheckView, BoletimPDFView, DeclaracaoMatriculaPDFView


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="documentos-health"),
    path("boletim/<int:aluno_id>/", BoletimPDFView.as_view(), name="boletim-pdf"),
    path(
        "declaracao_matricula/<int:aluno_id>/",
        DeclaracaoMatriculaPDFView.as_view(),
        name="declaracao-matricula-pdf",
    ),
]
