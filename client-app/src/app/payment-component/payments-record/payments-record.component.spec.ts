import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaymentsRecordComponent } from './payments-record.component';

describe('PaymentsRecordComponent', () => {
  let component: PaymentsRecordComponent;
  let fixture: ComponentFixture<PaymentsRecordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PaymentsRecordComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PaymentsRecordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
