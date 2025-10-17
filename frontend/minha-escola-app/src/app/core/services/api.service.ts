import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  readonly baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  private buildUrl(path: string): string {
    const p = path.startsWith('/') ? path.substring(1) : path;
    return `${this.baseUrl}/${p}`;
  }

  get<T>(path: string, params?: HttpParams | { [param: string]: string | number | boolean | ReadonlyArray<string | number | boolean> }): Observable<T> {
    return this.http.get<T>(this.buildUrl(path), { params });
  }

  getBlob(path: string, params?: HttpParams | { [param: string]: string | number | boolean | ReadonlyArray<string | number | boolean> }): Observable<Blob> {
    return this.http.get(this.buildUrl(path), { params, responseType: 'blob' });
  }

  post<T>(path: string, body: any): Observable<T> {
    return this.http.post<T>(this.buildUrl(path), body);
  }

  put<T>(path: string, body: any): Observable<T> {
    return this.http.put<T>(this.buildUrl(path), body);
  }

  patch<T>(path: string, body: any): Observable<T> {
    return this.http.patch<T>(this.buildUrl(path), body);
  }

  delete<T>(path: string): Observable<T> {
    return this.http.delete<T>(this.buildUrl(path));
  }
}
