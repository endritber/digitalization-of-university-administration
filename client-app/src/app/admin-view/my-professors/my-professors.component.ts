import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-my-professors',
  templateUrl: './my-professors.component.html',
  styleUrls: ['./my-professors.component.css']
})
export class MyProfessorsComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  displayStudents: string [] = ['email','ids','select'];
  studentSource = someData;

}




export interface elems {
  email: string;
  ids: number;
  select: string;

}

const someData: elems[] = [
  { email: 'as1234@professor.com',ids: 111111, select: 'Select' },
  { email: 'sd1235@professor.com',ids: 122222 , select: 'Select'},
  { email: 'ds1236@professor.com',ids: 634535 , select: 'Select'},
  { email: 'ab1237@professor.com',ids: 523123 , select: 'Select'},
  { email: 'hd1238@professor.com',ids: 223223 , select: 'Select'},
  { email: 'ak1239@professor.com',ids: 123123 , select: 'Select'},
  { email: 'gd1230@professor.com',ids: 123123 , select: 'Select'},
  { email: 'dd1231@professor.com',ids: 723123 , select: 'Select'},
  { email: 'dd1232@professor.com',ids: 123123 , select: 'Select'},
  { email: 'dd1233@professor.com',ids: 123123 , select: 'Select'},
  { email: 'dd1234@professor.com',ids: 123123 , select: 'Select'},
  { email: 'dd1235@professor.com',ids: 123123 , select: 'Select'},


]
