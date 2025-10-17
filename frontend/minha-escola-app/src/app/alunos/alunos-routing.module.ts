import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../core/guards/auth.guard';
import { AlunosListComponent } from './components/alunos-list/alunos-list.component';
import { AlunoDetailsComponent } from './components/aluno-details/aluno-details.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: AlunosListComponent },
  { path: ':id', canActivate: [AuthGuard], component: AlunoDetailsComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AlunosRoutingModule {}
