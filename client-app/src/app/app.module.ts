import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InputComponentViewComponent } from './input-component-view/input-component-view.component';
import { StudentViewComponentComponent } from './student-view-component/student-view-component.component';
import { MyProfileComponentComponent } from './my-profile-component/my-profile-component.component';

import { ExamsComponentComponent } from './exams-component/exams-component.component';
import {PaymentsModule} from "./payment-component/payments/payments.module";
import { PaymentsRecordComponent } from './payment-component/payments-record/payments-record.component';
import {CommonModule} from "@angular/common";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatTableModule} from "@angular/material/table";
import {ProfessorViewComponent} from "./professor-view/professor-view.component";
import {MyStudentsComponent} from "./professor-view/my-students/my-students.component";
import { StudentProfileComponent } from './professor-view/my-students/student-profile/student-profile.component';
import { AdminViewComponent } from './admin-view/admin-view.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MyProfessorsComponent } from './admin-view/my-professors/my-professors.component';


@NgModule({
  declarations: [
    AppComponent,
    InputComponentViewComponent,
    StudentViewComponentComponent,
    MyProfileComponentComponent,
    ExamsComponentComponent,
    PaymentsRecordComponent,
    ProfessorViewComponent,
    MyStudentsComponent,
    StudentProfileComponent,
    AdminViewComponent,
    MyProfessorsComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    RouterModule,
    PaymentsModule,
    CommonModule,
    BrowserAnimationsModule,
    MatTableModule,
    HttpClientModule
    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
