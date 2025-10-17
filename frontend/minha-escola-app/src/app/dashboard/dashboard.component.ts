import { Component, OnInit } from '@angular/core';
import { ApiService } from '../core/services/api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  standalone: false,
})
export class DashboardComponent implements OnInit {
  loading = false;
  counts = { alunos: 0, turmas: 0, matriculas: 0, faturasAbertas: 0 };

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    Promise.all([
      this.api.get<any[]>('core/alunos/').toPromise(),
      this.api.get<any[]>('academico/turmas/').toPromise(),
      this.api.get<any[]>('matriculas/matriculas/').toPromise(),
      this.api.get<any[]>('financeiro/faturas/', { status: 'ABERTA' }).toPromise(),
    ])
      .then(([alunos, turmas, matriculas, faturas]) => {
        this.counts.alunos = alunos?.length || 0;
        this.counts.turmas = turmas?.length || 0;
        this.counts.matriculas = matriculas?.length || 0;
        this.counts.faturasAbertas = faturas?.length || 0;
      })
      .finally(() => (this.loading = false));
  }
}
