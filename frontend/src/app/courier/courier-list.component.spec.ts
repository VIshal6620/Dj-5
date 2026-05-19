import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CourierListComponent } from './courier-list.component';

describe('CourierListComponent', () => {
  let component: CourierListComponent;
  let fixture: ComponentFixture<CourierListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CourierListComponent]
    });
    fixture = TestBed.createComponent(CourierListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
