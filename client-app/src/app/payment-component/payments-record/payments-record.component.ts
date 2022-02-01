import { Component, OnInit } from '@angular/core';



export interface Elements {
  number:number;
  level: string;
  universityDirection: string;
  fCode: number;
  billing: string;
  paid: string;
  own: string;
  data: string;
}

  const someData: Elements[] = [

    {number: 1,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1122,billing: '$100', paid: '$100', own: '$0',data: '10.06.2021'},
    {number: 2,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1123,billing: '$100', paid: '$50', own: '$50',data: '10.07.2021'},
    {number: 3,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1124,billing: '$100', paid: '$100',own: '$50',data: '10.08.2021'},
    {number: 4,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1125,billing: '$100', paid: '$150', own: '$0',data: '10.09.2021'},
    {number: 5,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1126,billing: '$100', paid: '$50', own: '$50',data: '10.10.2021'},
    {number: 6,level: 'Bachelor',universityDirection: 'Computer Science',fCode: 1127,billing: '$100', paid: '$150', own: '$0',data: '10.11.2021'},
  ]




@Component({
  selector: 'app-payments-record',
  templateUrl: './payments-record.component.html',
  styleUrls: ['./payments-record.component.css']
})
export class PaymentsRecordComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  displayColumns: string[] = ['number','level','universityDirection','fCode','billing','paid','own','data'];
  dataSource = someData;

}

