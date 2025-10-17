import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './core/services/auth.service';
import { ThemeService } from './core/services/theme.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  standalone: false,
})
export class AppComponent {
  isDark = false;

  constructor(private router: Router, private auth: AuthService, private theme: ThemeService) {
    this.theme.isDark$.subscribe((v) => (this.isDark = v));
  }

  get hideLayout(): boolean {
    return this.router.url.startsWith('/login');
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  toggleTheme(): void {
    this.theme.toggle();
  }
}
