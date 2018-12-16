import { HttpClientModule } from "@angular/common/http";
import { NgModule } from '@angular/core';
import { UserApiService } from "./user-api.service";

@NgModule({
  imports: [
    HttpClientModule
  ],
  providers: [
    UserApiService
  ]
})
export class ApiModule {
}
