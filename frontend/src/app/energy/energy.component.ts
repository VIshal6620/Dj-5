import { Component } from '@angular/core';
import { ServiceLocatorService } from '../service-locator.service';
import { BaseCtl } from '../base.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-energy',
  templateUrl: './energy.component.html',
  styleUrls: ['./energy.component.css']
})
export class EnergyComponent extends BaseCtl {
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.ENERGY, locator, route);
    }

}
