import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfessorViewComponent } from './professor-view.component';

describe('ProfessorViewComponent', () => {
  let component: ProfessorViewComponent;
  let fixture: ComponentFixture<ProfessorViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfessorViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfessorViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
