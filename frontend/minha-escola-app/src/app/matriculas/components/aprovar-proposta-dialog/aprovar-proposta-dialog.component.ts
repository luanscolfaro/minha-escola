import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-aprovar-proposta-dialog',
  templateUrl: './aprovar-proposta-dialog.component.html',
  standalone: false,
})
export class AprovarPropostaDialogComponent implements OnInit {
  turmas: any[] = [];
  planos: any[] = [];

  form = this.fb.group({
    turma: [null as number | null, Validators.required],
    plano: [null as number | null, Validators.required],
    ano_letivo: [new Date().getFullYear(), Validators.required],
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { id: number },
    private ref: MatDialogRef<AprovarPropostaDialogComponent>,
    private fb: FormBuilder,
    private api: ApiService,
    private toast: ToastrService
  ) {}

  ngOnInit(): void {
    this.api.get<any[]>('academico/turmas/').subscribe((t) => (this.turmas = t));
    this.api.get<any[]>('matriculas/planos/').subscribe((p) => (this.planos = p));
  }

  aprovar(): void {
    const v = this.form.getRawValue();
    this.api
      .post(`matriculas/propostas/${this.data.id}/aprovar_proposta/`, {
        turma: v.turma,
        plano: v.plano,
        ano_letivo: v.ano_letivo,
      })
      .subscribe({
        next: () => {
          this.toast.success('Proposta aprovada');
          this.ref.close(true);
        },
        error: () => this.toast.error('Falha ao aprovar proposta'),
      });
  }
}
