import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-aluno-dialog',
  templateUrl: './aluno-dialog.component.html',
  standalone: false,
})
export class AlunoDialogComponent {
  form = this.fb.group({
    id: [null as number | null],
    nome: ['', Validators.required],
    matricula: ['', Validators.required],
    cpf: [''],
    ativo: [true],
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private ref: MatDialogRef<AlunoDialogComponent>,
    private fb: FormBuilder,
    private api: ApiService,
    private toast: ToastrService
  ) {
    if (data) {
      this.form.patchValue(data);
    }
  }

  save(): void {
    const v = this.form.getRawValue();
    const payload: any = { nome: v.nome, matricula: v.matricula, cpf: v.cpf, ativo: v.ativo };
    const req = v.id ? this.api.put(`core/alunos/${v.id}/`, payload) : this.api.post('core/alunos/', payload);
    req.subscribe({
      next: () => {
        this.toast.success('Registro salvo');
        this.ref.close(true);
      },
      error: () => this.toast.error('Falha ao salvar'),
    });
  }
}
