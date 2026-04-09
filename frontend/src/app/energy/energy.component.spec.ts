import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EnergyComponent } from './energy.component';

describe('EnergyComponent', () => {
  let component: EnergyComponent;
  let fixture: ComponentFixture<EnergyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EnergyComponent]
    });
    fixture = TestBed.createComponent(EnergyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
