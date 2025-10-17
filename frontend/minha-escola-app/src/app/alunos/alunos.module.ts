import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { AlunosRoutingModule } from './alunos-routing.module';
import { AlunosListComponent } from './components/alunos-list/alunos-list.component';
import { AlunoDialogComponent } from './components/aluno-dialog/aluno-dialog.component';
import { AlunoDetailsComponent } from './components/aluno-details/aluno-details.component';

@NgModule({
  declarations: [AlunosListComponent, AlunoDialogComponent, AlunoDetailsComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatTableModule,
    MatPaginatorModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    AlunosRoutingModule,
  ],
})
export class AlunosModule {}
