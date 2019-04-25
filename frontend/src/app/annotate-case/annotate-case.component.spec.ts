import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnotateCaseComponent } from './annotate-case.component';

describe('AnnotateCaseComponent', () => {
  let component: AnnotateCaseComponent;
  let fixture: ComponentFixture<AnnotateCaseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AnnotateCaseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AnnotateCaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
