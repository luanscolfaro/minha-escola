from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from io import BytesIO
from datetime import date

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from apps.core.models import Aluno
from apps.academico.models import Nota


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "documentos"})


class BoletimPDFView(APIView):
    def get(self, request, aluno_id: int):
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=404)

        try:
            ano = int(request.query_params.get("ano", str(date.today().year)))
        except ValueError:
            return Response({"detail": "Parâmetro 'ano' inválido."}, status=400)

        notas = (
            Nota.objects.select_related(
                "avaliacao",
                "avaliacao__disciplina",
                "avaliacao__turma",
            )
            .filter(aluno=aluno, avaliacao__turma__ano_letivo=ano)
            .order_by("avaliacao__disciplina__nome", "avaliacao__data")
        )

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 2 * cm
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, y, f"Boletim - {ano}")
        y -= 1 * cm
        p.setFont("Helvetica", 12)
        p.drawString(2 * cm, y, f"Aluno: {aluno.nome} | Matrícula: {aluno.matricula}")
        y -= 0.8 * cm

        current_disc = None
        for n in notas:
            disc = n.avaliacao.disciplina.nome
            if disc != current_disc:
                y -= 0.4 * cm
                p.setFont("Helvetica-Bold", 13)
                p.drawString(2 * cm, y, f"Disciplina: {disc}")
                y -= 0.6 * cm
                current_disc = disc
                p.setFont("Helvetica", 12)

            p.drawString(
                2 * cm,
                y,
                f"{n.avaliacao.data.strftime('%d/%m/%Y')} - {n.avaliacao.titulo} (peso {n.avaliacao.peso}): {n.valor}",
            )
            y -= 0.6 * cm
            if y < 2 * cm:
                p.showPage()
                y = height - 2 * cm
                p.setFont("Helvetica", 12)

        if not notas:
            p.drawString(2 * cm, y, "Sem notas registradas para o ano informado.")

        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        resp = HttpResponse(pdf, content_type="application/pdf")
        resp["Content-Disposition"] = f"inline; filename=boletim-{aluno_id}-{ano}.pdf"
        return resp


class DeclaracaoMatriculaPDFView(APIView):
    def get(self, request, aluno_id: int):
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=404)

        matricula = (
            aluno.matriculas.select_related("turma", "turma__serie").filter(ativa=True).order_by("-ano_letivo").first()
        )

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 2 * cm
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, y, "Declaração de Matrícula")
        y -= 1.2 * cm
        p.setFont("Helvetica", 12)

        if matricula:
            texto = (
                f"Declaramos para os devidos fins que {aluno.nome}, portador(a) da matrícula {aluno.matricula}, "
                f"está regularmente matriculado(a) na turma {matricula.turma.nome} da série {matricula.turma.serie.nome}, "
                f"no ano letivo de {matricula.ano_letivo}."
            )
        else:
            texto = (
                f"Declaramos para os devidos fins que {aluno.nome}, portador(a) da matrícula {aluno.matricula}, "
                f"não possui matrícula ativa no momento."
            )

        # Quebra simples de linhas a cada ~100 caracteres
        max_chars = 100
        while texto:
            p.drawString(2 * cm, y, texto[:max_chars])
            texto = texto[max_chars:]
            y -= 0.8 * cm
            if y < 2 * cm:
                p.showPage()
                y = height - 2 * cm
                p.setFont("Helvetica", 12)

        y -= 1 * cm
        p.drawString(2 * cm, y, f"Fortaleza, {date.today().strftime('%d/%m/%Y')}")

        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        resp = HttpResponse(pdf, content_type="application/pdf")
        resp["Content-Disposition"] = f"inline; filename=declaracao-matricula-{aluno_id}.pdf"
        return resp
