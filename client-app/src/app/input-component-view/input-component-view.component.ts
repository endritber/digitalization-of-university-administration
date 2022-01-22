import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-input-component-view',
  templateUrl: './input-component-view.component.html',
  styleUrls: ['./input-component-view.component.css']
})
export class InputComponentViewComponent implements OnInit {

  mail = new FormControl('',Validators.compose([Validators.required,Validators.email]));
  password = new FormControl('',Validators.compose([Validators.required,Validators.minLength(6)]))

  constructor() { }

  ngOnInit(): void {
  }

}
