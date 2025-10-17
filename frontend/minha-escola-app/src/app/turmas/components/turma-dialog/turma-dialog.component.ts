import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-turma-dialog',
  templateUrl: './turma-dialog.component.html',
  standalone: false,
})
export class TurmaDialogComponent implements OnInit {
  series: { id: number; nome: string }[] = [];
  professores: { id: number; username: string }[] = [];

  form = this.fb.group({
    id: [null as number | null],
    nome: ['', Validators.required],
    serie: [null as number | null, Validators.required],
    ano_letivo: [new Date().getFullYear(), Validators.required],
    turno: [''],
    professores: [[] as number[]],
    ativo: [true],
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private ref: MatDialogRef<TurmaDialogComponent>,
    private fb: FormBuilder,
    private api: ApiService,
    private toast: ToastrService
  ) {}

  ngOnInit(): void {
    this.api.get<any[]>('academico/series/').subscribe((s) => (this.series = s));
    this.api.get<any[]>('usuarios/usuarios/').subscribe((u) => (this.professores = u));
    if (this.data) {
      this.form.patchValue(this.data);
    }
  }

  save(): void {
    const v = this.form.getRawValue();
    const payload: any = {
      nome: v.nome,
      serie: v.serie,
      ano_letivo: v.ano_letivo,
      turno: v.turno,
      professores: v.professores,
      ativo: v.ativo,
    };
    const req = v.id ? this.api.put(`academico/turmas/${v.id}/`, payload) : this.api.post('academico/turmas/', payload);
    req.subscribe({
      next: () => {
        this.toast.success('Turma salva');
        this.ref.close(true);
      },
      error: () => this.toast.error('Falha ao salvar turma'),
    });
  }
}
