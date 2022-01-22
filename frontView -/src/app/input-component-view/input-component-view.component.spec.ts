import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InputComponentViewComponent } from './input-component-view.component';

describe('InputComponentViewComponent', () => {
  let component: InputComponentViewComponent;
  let fixture: ComponentFixture<InputComponentViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InputComponentViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputComponentViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
