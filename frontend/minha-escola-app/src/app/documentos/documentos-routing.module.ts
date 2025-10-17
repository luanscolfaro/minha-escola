import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../core/guards/auth.guard';
import { DocumentosPageComponent } from './documentos-page/documentos-page.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: DocumentosPageComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DocumentosRoutingModule {}

