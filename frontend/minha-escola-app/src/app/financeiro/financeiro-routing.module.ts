import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../core/guards/auth.guard';
import { FaturasListComponent } from './components/faturas-list/faturas-list.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: FaturasListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class FinanceiroRoutingModule {}

