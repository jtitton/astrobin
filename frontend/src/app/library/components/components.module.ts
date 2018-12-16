import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FontAwesomeModule } from "@fortawesome/angular-fontawesome";
import { NgbDropdownModule } from "@ng-bootstrap/ng-bootstrap";
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from "./header/header.component";

@NgModule({
  imports: [
    CommonModule,
    FontAwesomeModule,
    NgbDropdownModule
  ],
  declarations: [
    HeaderComponent,
    FooterComponent
  ],
  exports: [
    FontAwesomeModule,
    NgbDropdownModule,
    HeaderComponent,
    FooterComponent
  ]
})
export class ComponentsModule { }
