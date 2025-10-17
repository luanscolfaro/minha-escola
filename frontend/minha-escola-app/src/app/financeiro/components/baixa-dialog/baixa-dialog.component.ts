import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-baixa-dialog',
  templateUrl: './baixa-dialog.component.html',
  standalone: false,
})
export class BaixaDialogComponent {
  form = this.fb.group({
    data_pagamento: ['', Validators.required],
    valor_pago: ['', Validators.required],
    observacao: [''],
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { id: number },
    private ref: MatDialogRef<BaixaDialogComponent>,
    private fb: FormBuilder,
    private api: ApiService,
    private toast: ToastrService
  ) {}

  salvar(): void {
    const v = this.form.getRawValue();
    this.api.post(`financeiro/faturas/${this.data.id}/baixar/`, v).subscribe({
      next: () => {
        this.toast.success('Baixa registrada');
        this.ref.close(true);
      },
      error: () => this.toast.error('Falha ao registrar baixa'),
    });
  }
}
