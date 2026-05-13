import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LightListComponent } from './light-list.component';

describe('LightListComponent', () => {
  let component: LightListComponent;
  let fixture: ComponentFixture<LightListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LightListComponent]
    });
    fixture = TestBed.createComponent(LightListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
