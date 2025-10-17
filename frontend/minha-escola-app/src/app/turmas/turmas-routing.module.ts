import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../core/guards/auth.guard';
import { TurmasListComponent } from './components/turmas-list/turmas-list.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: TurmasListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TurmasRoutingModule {}

