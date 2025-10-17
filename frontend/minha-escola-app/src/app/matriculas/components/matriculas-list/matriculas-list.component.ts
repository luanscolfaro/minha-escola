import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ToastrService } from 'ngx-toastr';
import { ApiService } from '../../../core/services/api.service';

type Matricula = {
  id: number;
  aluno: number;
  turma: number;
  plano: number;
  ano_letivo: number;
  ativa: boolean;
};

@Component({
  selector: 'app-matriculas-list',
  templateUrl: './matriculas-list.component.html',
  styleUrls: ['./matriculas-list.component.scss'],
  standalone: false,
})
export class MatriculasListComponent implements OnInit {
  displayedColumns = ['id', 'aluno', 'turma', 'plano', 'ano_letivo', 'ativa'];
  dataSource = new MatTableDataSource<Matricula>([]);
  loading = false;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private api: ApiService, private toast: ToastrService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    this.api.get<Matricula[]>('matriculas/matriculas/').subscribe({
      next: (data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.loading = false;
      },
      error: () => {
        this.toast.error('Falha ao carregar matrículas');
        this.loading = false;
      },
    });
  }
}
