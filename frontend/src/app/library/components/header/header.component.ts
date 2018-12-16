import { Component, OnInit } from '@angular/core';
import { AppContextService, IAppContext } from "../../services/app-context.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  appContext: IAppContext;

  constructor(appContext: AppContextService) {
    this.appContext = appContext.get();
  }

  ngOnInit() {
  }
}
