import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms'; // Assicurati che sia importato
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { RegisterComponent } from './register/register.component';
import { AuthService } from './auth.service';
import { routes } from './app.routes'; // Importa le rotte

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent // Assicurati che RegisterComponent sia dichiarato qui
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule, // Aggiungi ReactiveFormsModule qui
    HttpClientModule,
    RouterModule.forRoot(routes) // Configura le rotte
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
