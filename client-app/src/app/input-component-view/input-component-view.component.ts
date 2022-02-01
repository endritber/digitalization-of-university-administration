import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators, FormControlName } from '@angular/forms';


@Component({
  selector: 'app-input-component-view',
  templateUrl: './input-component-view.component.html',
  styleUrls: ['./input-component-view.component.css']
})
export class InputComponentViewComponent  {



  formgroup = new FormGroup({

    password : new FormControl('',Validators.compose([Validators.required,Validators.minLength(6)])),
    email : new FormControl('',Validators.compose([Validators.required,Validators.email]))

  })
  constructor(private http : HttpClient){}

  sendData(x: any, y: any){
      this.newEmail = x;
      this.newPw = y;
  }

  newEmail = '';
  newPw = '';


  ngOnInit() {
    this.http.post<any>('localhost:8000/api/user-managment/token', { email: this.newEmail, password: this.newPw}).subscribe(data => {
        console.log(data)
    })
}
}
