import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ComponentsModule } from "./components/components.module";
import { ServicesModule } from "./services/services.module";

@NgModule({
  imports: [
    CommonModule,
    ComponentsModule,
    ServicesModule
  ],
  exports: [
    ComponentsModule,
    ServicesModule
  ]
})
export class LibraryModule { }
