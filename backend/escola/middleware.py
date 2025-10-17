from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("auditoria")


class AuditoriaMiddleware:
    """Middleware simples de auditoria.

    Registra usuário (id/anon), método, path e timestamp de cada requisição.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        user_str = "anon"
        try:
            if getattr(request, "user", None) and request.user.is_authenticated:
                user_str = f"user={request.user.id}:{request.user.username}"
        except Exception:
            pass

        logger.info(
            "AUDIT | %s | %s | %s | %s",
            datetime.utcnow().isoformat(),
            request.method,
            request.get_full_path(),
            user_str,
        )
        return self.get_response(request)

