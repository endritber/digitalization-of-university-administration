import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExamsComponentComponent } from './exams-component/exams-component.component';
import { MyProfileComponentComponent } from './my-profile-component/my-profile-component.component';
import { StudentViewComponentComponent } from './student-view-component/student-view-component.component';
import {PaymentComponent} from "./payment-component/paymentcomponent.component";
import {PaymentsRecordComponent} from "./payment-component/payments-record/payments-record.component";
import {ProfessorViewComponent} from "./professor-view/professor-view.component";
import {MyStudentsComponent} from "./professor-view/my-students/my-students.component";
import { StudentProfileComponent } from './professor-view/my-students/student-profile/student-profile.component';
import { InputComponentViewComponent } from './input-component-view/input-component-view.component';
import { AdminViewComponent } from './admin-view/admin-view.component';
import { MyProfessorsComponent } from './admin-view/my-professors/my-professors.component';

const routes: Routes = [

  


      {path: 'studentProfile', component: MyProfileComponentComponent},
      { path: 'payments', component: PaymentComponent, children: [
        {path: 'records', component: PaymentsRecordComponent}
      ]},
      {path: 'exams', component: ExamsComponentComponent}
    ,
    
      { path: 'studentProfile', component: MyProfileComponentComponent},
      { path: 'myStudents', component: MyStudentsComponent}
    ,
    { path: 'login', component: InputComponentViewComponent}
    ,
    { path: 'adminView', component: AdminViewComponent}
    ,{path: 'myproff', component: MyProfessorsComponent }
      

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
