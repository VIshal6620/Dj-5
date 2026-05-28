import { Component } from '@angular/core';
import { ServiceLocatorService } from '../service-locator.service';
import { BaseCtl } from '../base.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent extends BaseCtl {
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.CAR, locator, route);
    }

}
