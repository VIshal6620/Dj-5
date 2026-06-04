import { Component } from '@angular/core';
import { ServiceLocatorService } from '../service-locator.service';
import { BaseCtl } from '../base.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-claim',
  templateUrl: './claim.component.html',
  styleUrls: ['./claim.component.css']
})
export class ClaimComponent extends BaseCtl {
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.CLAIM, locator, route);
    }

}
