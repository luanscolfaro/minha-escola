import { Component } from '@angular/core';
import { ApiService } from '../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-documentos-page',
  templateUrl: './documentos-page.component.html',
  styleUrls: ['./documentos-page.component.scss'],
  standalone: false,
})
export class DocumentosPageComponent {
  alunoId: number | null = null;
  ano: number = new Date().getFullYear();

  constructor(private api: ApiService, private toast: ToastrService) {}

  private downloadBlob(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  gerarBoletim(): void {
    if (!this.alunoId) { this.toast.warning('Informe o ID do aluno'); return; }
    this.api.getBlob(`documentos/boletim/${this.alunoId}/`, { ano: String(this.ano) }).subscribe({
      next: (blob) => this.downloadBlob(blob, `boletim-${this.alunoId}-${this.ano}.pdf`),
      error: () => this.toast.error('Falha ao gerar boletim'),
    });
  }

  gerarDeclaracao(): void {
    if (!this.alunoId) { this.toast.warning('Informe o ID do aluno'); return; }
    this.api.getBlob(`documentos/declaracao_matricula/${this.alunoId}/`).subscribe({
      next: (blob) => this.downloadBlob(blob, `declaracao-matricula-${this.alunoId}.pdf`),
      error: () => this.toast.error('Falha ao gerar declaração'),
    });
  }
}
