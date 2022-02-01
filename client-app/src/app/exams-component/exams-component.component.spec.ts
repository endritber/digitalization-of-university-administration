import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamsComponentComponent } from './exams-component.component';

describe('ExamsComponentComponent', () => {
  let component: ExamsComponentComponent;
  let fixture: ComponentFixture<ExamsComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExamsComponentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExamsComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
