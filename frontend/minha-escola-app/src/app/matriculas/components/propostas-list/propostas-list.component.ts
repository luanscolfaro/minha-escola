import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { ApiService } from '../../../core/services/api.service';
import { AprovarPropostaDialogComponent } from '../aprovar-proposta-dialog/aprovar-proposta-dialog.component';

type Proposta = {
  id: number;
  aluno: number;
  status: string;
  criado_em: string;
};

@Component({
  selector: 'app-propostas-list',
  templateUrl: './propostas-list.component.html',
  styleUrls: ['./propostas-list.component.scss'],
  standalone: false,
})
export class PropostasListComponent implements OnInit {
  displayedColumns = ['id', 'aluno', 'status', 'criado_em', 'actions'];
  dataSource = new MatTableDataSource<Proposta>([]);
  loading = false;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private api: ApiService, private dialog: MatDialog, private toast: ToastrService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    this.api.get<Proposta[]>('matriculas/propostas/').subscribe({
      next: (data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.loading = false;
      },
      error: () => {
        this.toast.error('Falha ao carregar propostas');
        this.loading = false;
      },
    });
  }

  aprovar(row: Proposta): void {
    const ref = this.dialog.open(AprovarPropostaDialogComponent, { data: row, width: '520px' });
    ref.afterClosed().subscribe((ok) => ok && this.load());
  }
}
