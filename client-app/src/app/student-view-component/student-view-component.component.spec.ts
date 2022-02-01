import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentViewComponentComponent } from './student-view-component.component';

describe('StudentViewComponentComponent', () => {
  let component: StudentViewComponentComponent;
  let fixture: ComponentFixture<StudentViewComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StudentViewComponentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StudentViewComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
