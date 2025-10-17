import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt';
import { ApiService } from './api.service';

type TokenResponse = { access: string; refresh?: string };

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly ACCESS_KEY = 'access_token';
  private readonly REFRESH_KEY = 'refresh_token';

  constructor(private api: ApiService, private http: HttpClient, private jwt: JwtHelperService) {}

  login(username: string, password: string): Observable<TokenResponse> {
    return this.api.post<TokenResponse>('auth/token', { username, password }).pipe(
      tap((res) => {
        if (res.access) localStorage.setItem(this.ACCESS_KEY, res.access);
        if (res.refresh) localStorage.setItem(this.REFRESH_KEY, res.refresh);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(this.ACCESS_KEY);
    localStorage.removeItem(this.REFRESH_KEY);
  }

  get accessToken(): string | null {
    return localStorage.getItem(this.ACCESS_KEY);
  }

  isLogged(): boolean {
    const token = this.accessToken;
    if (!token) return false;
    try {
      return !this.jwt.isTokenExpired(token);
    } catch {
      return !!token; // fallback simples
    }
  }
}

