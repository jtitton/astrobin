import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ApiModule } from "./api/api.module";
import { AppContextService } from "./app-context.service";

@NgModule({
  imports: [
    CommonModule,
    ApiModule
  ],
  providers: [
    AppContextService
  ],
  exports: [
    ApiModule
  ]
})
export class ServicesModule {
}
