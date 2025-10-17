import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../core/guards/auth.guard';
import { PropostasListComponent } from './components/propostas-list/propostas-list.component';
import { MatriculasListComponent } from './components/matriculas-list/matriculas-list.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'propostas' },
  { path: 'propostas', canActivate: [AuthGuard], component: PropostasListComponent },
  { path: 'matriculas', canActivate: [AuthGuard], component: MatriculasListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MatriculasRoutingModule {}

