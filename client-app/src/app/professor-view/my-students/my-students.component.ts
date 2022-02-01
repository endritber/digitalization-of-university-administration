import { Component, OnInit } from '@angular/core';

export interface elems {
  email: string;
  ids: number;
  select: string;

}

const someData: elems[] = [
  { email: 'dd1234@example.com',ids: 123123, select: 'Select' },
  { email: 'dd1235@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1236@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1237@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1238@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1239@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1230@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1231@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1232@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1233@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1234@example.com',ids: 123123 , select: 'Select'},
  { email: 'dd1235@example.com',ids: 123123 , select: 'Select'},


]

@Component({
  selector: 'app-my-students',
  templateUrl: './my-students.component.html',
  styleUrls: ['./my-students.component.css']
})
export class MyStudentsComponent implements OnInit {


  displayStudents: string [] = ['email','ids','select'];
  studentSource = someData;

  constructor() { }

  ngOnInit(): void {
  }


}
