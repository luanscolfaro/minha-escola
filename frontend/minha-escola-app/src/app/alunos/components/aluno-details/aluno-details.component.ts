import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-aluno-details',
  templateUrl: './aluno-details.component.html',
  styleUrls: ['./aluno-details.component.scss'],
  standalone: false,
})
export class AlunoDetailsComponent implements OnInit {
  id!: number;
  aluno: any;

  anoForm = this.fb.group({ ano: [new Date().getFullYear()] });

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
    private fb: FormBuilder,
    private toast: ToastrService
  ) {}

  ngOnInit(): void {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
    this.load();
  }

  load(): void {
    this.api.get<any>(`core/alunos/${this.id}/`).subscribe({
      next: (aluno) => (this.aluno = aluno),
      error: () => this.toast.error('Falha ao carregar aluno'),
    });
  }

  private downloadBlob(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  baixarBoletim(): void {
    const ano = this.anoForm.value.ano || new Date().getFullYear();
    this.api.getBlob(`documentos/boletim/${this.id}/`, { ano: String(ano) }).subscribe({
      next: (blob) => this.downloadBlob(blob, `boletim-${this.id}-${ano}.pdf`),
      error: () => this.toast.error('Falha ao gerar boletim'),
    });
  }

  baixarDeclaracao(): void {
    this.api.getBlob(`documentos/declaracao_matricula/${this.id}/`).subscribe({
      next: (blob) => this.downloadBlob(blob, `declaracao-matricula-${this.id}.pdf`),
      error: () => this.toast.error('Falha ao gerar declaração'),
    });
  }
}
