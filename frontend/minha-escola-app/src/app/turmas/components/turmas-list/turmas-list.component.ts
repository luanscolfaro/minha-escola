import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { ApiService } from '../../../core/services/api.service';
import { TurmaDialogComponent } from '../turma-dialog/turma-dialog.component';

type Turma = {
  id: number;
  nome: string;
  serie: number;
  ano_letivo: number;
  turno?: string;
  ativo: boolean;
};

@Component({
  selector: 'app-turmas-list',
  templateUrl: './turmas-list.component.html',
  styleUrls: ['./turmas-list.component.scss'],
  standalone: false,
})
export class TurmasListComponent implements OnInit {
  displayedColumns = ['id', 'nome', 'serie', 'ano_letivo', 'turno', 'ativo', 'actions'];
  dataSource = new MatTableDataSource<Turma>([]);
  loading = false;
  query = '';

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private api: ApiService, private dialog: MatDialog, private toast: ToastrService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    const params: any = {};
    if (this.query) params.search = this.query;
    this.api.get<Turma[]>('academico/turmas/', params).subscribe({
      next: (data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.loading = false;
      },
      error: () => {
        this.toast.error('Falha ao carregar turmas');
        this.loading = false;
      },
    });
  }

  openCreate(): void {
    const ref = this.dialog.open(TurmaDialogComponent, { data: null, width: '520px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }

  openEdit(row: Turma): void {
    const ref = this.dialog.open(TurmaDialogComponent, { data: row, width: '520px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }

  remove(row: Turma): void {
    if (!confirm('Remover turma?')) return;
    this.api.delete(`academico/turmas/${row.id}/`).subscribe({
      next: () => {
        this.toast.success('Turma removida');
        this.load();
      },
      error: () => this.toast.error('Falha ao remover turma'),
    });
  }
}
