import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { LoginComponent } from './auth/login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', canActivate: [AuthGuard], component: DashboardComponent },
  { path: 'alunos', canActivate: [AuthGuard], loadChildren: () => import('./alunos/alunos.module').then(m => m.AlunosModule) },
  { path: 'turmas', canActivate: [AuthGuard], loadChildren: () => import('./turmas/turmas.module').then(m => m.TurmasModule) },
  { path: 'matriculas', canActivate: [AuthGuard], loadChildren: () => import('./matriculas/matriculas.module').then(m => m.MatriculasModule) },
  { path: 'financeiro', canActivate: [AuthGuard], loadChildren: () => import('./financeiro/financeiro.module').then(m => m.FinanceiroModule) },
  { path: 'documentos', canActivate: [AuthGuard], loadChildren: () => import('./documentos/documentos.module').then(m => m.DocumentosModule) },
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  { path: '**', redirectTo: 'dashboard' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
