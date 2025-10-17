import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { ApiService } from '../../../core/services/api.service';
import { AlunoDialogComponent } from '../aluno-dialog/aluno-dialog.component';

type Aluno = {
  id: number;
  nome: string;
  matricula: string;
  cpf?: string;
  ativo: boolean;
};

@Component({
  selector: 'app-alunos-list',
  templateUrl: './alunos-list.component.html',
  styleUrls: ['./alunos-list.component.scss'],
  standalone: false,
})
export class AlunosListComponent implements OnInit {
  displayedColumns = ['id', 'nome', 'matricula', 'cpf', 'ativo', 'actions'];
  dataSource = new MatTableDataSource<Aluno>([]);
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
    this.api.get<Aluno[]>('core/alunos/', params).subscribe({
      next: (data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.loading = false;
      },
      error: () => {
        this.toast.error('Falha ao carregar alunos');
        this.loading = false;
      },
    });
  }

  openCreate(): void {
    const ref = this.dialog.open(AlunoDialogComponent, { data: null, width: '420px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }

  openEdit(row: Aluno): void {
    const ref = this.dialog.open(AlunoDialogComponent, { data: row, width: '420px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }

  remove(row: Aluno): void {
    if (!confirm('Remover aluno?')) return;
    this.api.delete(`core/alunos/${row.id}/`).subscribe({
      next: () => {
        this.toast.success('Aluno removido');
        this.load();
      },
      error: () => this.toast.error('Falha ao remover aluno'),
    });
  }
}
