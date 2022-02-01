import { Component, OnInit } from '@angular/core';


export interface ExamsElements {
  subjectName: string;
  professor: string;
  grade: number;
}


const someData: ExamsElements[] = [
  { subjectName: 'Java', professor:'Havush Politanka', grade: 10},
  { subjectName: 'Software Engineering', professor:'Drenush Papuqja', grade: 8},
  { subjectName: 'Mathematic', professor:'Petell Harushka', grade: 8},
  { subjectName: 'IT', professor:'Guugel Kromi', grade: 6},
  { subjectName: 'Managment', professor:'Treg Sallata', grade: 5},
]


@Component({
  selector: 'app-exams-component',
  templateUrl: './exams-component.component.html',
  styleUrls: ['./exams-component.component.css']
})
export class ExamsComponentComponent implements OnInit {




  displayGrades: string[] = ['subjectName','professor','grade'];
  Source = someData;


  constructor() { }

  ngOnInit(): void {
  }

}
