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
import { MatSelectModule } from '@angular/material/select';
import { MatTabsModule } from '@angular/material/tabs';
import { MatriculasRoutingModule } from './matriculas-routing.module';
import { PropostasListComponent } from './components/propostas-list/propostas-list.component';
import { MatriculasListComponent } from './components/matriculas-list/matriculas-list.component';
import { AprovarPropostaDialogComponent } from './components/aprovar-proposta-dialog/aprovar-proposta-dialog.component';

@NgModule({
  declarations: [PropostasListComponent, MatriculasListComponent, AprovarPropostaDialogComponent],
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
    MatSelectModule,
    MatTabsModule,
    MatriculasRoutingModule,
  ],
})
export class MatriculasModule {}

