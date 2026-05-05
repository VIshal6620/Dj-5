import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BaseListCtl } from '../base-list.component';
import { ServiceLocatorService } from '../service-locator.service';

@Component({
  selector: 'app-topic-list',
  templateUrl: './topic-list.component.html',
  styleUrls: ['./topic-list.component.css']
})
export class TopicListComponent extends BaseListCtl {
  constructor(locator: ServiceLocatorService, route: ActivatedRoute) {
          super(locator.endpoints.TOPIC, locator, route);
        }
  

}
