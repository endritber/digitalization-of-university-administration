import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {PaymentComponent} from "../paymentcomponent.component";
import {RouterModule} from "@angular/router";



@NgModule({
  declarations: [
    PaymentComponent,
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class PaymentsModule { }
