import { Component } from '@angular/core';
import { BaseListCtl } from '../base-list.component';
import { ServiceLocatorService } from '../service-locator.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-cloud-list',
  templateUrl: './cloud-list.component.html',
  styleUrls: ['./cloud-list.component.css']
})
export class CloudListComponent extends BaseListCtl {
  constructor(locator: ServiceLocatorService, route: ActivatedRoute) {
          super(locator.endpoints.CLOUD, locator, route);
        }
  

}
