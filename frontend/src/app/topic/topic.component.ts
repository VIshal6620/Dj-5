import { Component } from '@angular/core';
import { BaseCtl } from '../base.component';
import { ServiceLocatorService } from '../service-locator.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-topic',
  templateUrl: './topic.component.html',
  styleUrls: ['./topic.component.css']
})
export class TopicComponent extends BaseCtl {
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.TOPIC, locator, route);
    }

}
