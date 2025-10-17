import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly KEY = 'theme';
  private darkSubject = new BehaviorSubject<boolean>(false);
  isDark$ = this.darkSubject.asObservable();

  constructor() {
    const saved = localStorage.getItem(this.KEY);
    if (saved === 'dark') {
      this.applyDark(true);
    } else {
      this.applyDark(false);
    }
  }

  toggle(): void {
    this.applyDark(!this.darkSubject.value);
  }

  private applyDark(dark: boolean): void {
    this.darkSubject.next(dark);
    if (dark) {
      document.body.classList.add('dark-theme');
      localStorage.setItem(this.KEY, 'dark');
    } else {
      document.body.classList.remove('dark-theme');
      localStorage.setItem(this.KEY, 'light');
    }
  }
}

