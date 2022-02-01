import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyProfessorsComponent } from './my-professors.component';

describe('MyProfessorsComponent', () => {
  let component: MyProfessorsComponent;
  let fixture: ComponentFixture<MyProfessorsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MyProfessorsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MyProfessorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
