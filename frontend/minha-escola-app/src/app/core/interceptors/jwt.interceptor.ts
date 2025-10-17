import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  private getToken(): string | null {
    // Ajuste a chave conforme sua implementação de auth
    return localStorage.getItem('access_token');
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.getToken();

    const isApiRequest = req.url.startsWith('/api') || req.url.includes('://localhost:8000/api');

    if (token && isApiRequest) {
      const authReq = req.clone({
        setHeaders: { Authorization: `Bearer ${token}` },
      });
      return next.handle(authReq);
    }

    return next.handle(req);
  }
}

