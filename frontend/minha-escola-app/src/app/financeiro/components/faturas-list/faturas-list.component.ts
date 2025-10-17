import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { ApiService } from '../../../core/services/api.service';
import { BaixaDialogComponent } from '../baixa-dialog/baixa-dialog.component';

type Fatura = {
  id: number;
  matricula: number;
  competencia: string;
  vencimento: string;
  valor: string;
  status: string;
};

@Component({
  selector: 'app-faturas-list',
  templateUrl: './faturas-list.component.html',
  styleUrls: ['./faturas-list.component.scss'],
  standalone: false,
})
export class FaturasListComponent implements OnInit {
  displayedColumns = ['id', 'matricula', 'competencia', 'vencimento', 'valor', 'status', 'actions'];
  dataSource = new MatTableDataSource<Fatura>([]);
  loading = false;
  status = '';

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private api: ApiService, private dialog: MatDialog, private toast: ToastrService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    const params: any = {};
    if (this.status) params.status = this.status;
    this.api.get<Fatura[]>('financeiro/faturas/', params).subscribe({
      next: (data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.loading = false;
      },
      error: () => {
        this.toast.error('Falha ao carregar faturas');
        this.loading = false;
      },
    });
  }

  baixar(row: Fatura): void {
    const ref = this.dialog.open(BaixaDialogComponent, { data: row, width: '520px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }
}
