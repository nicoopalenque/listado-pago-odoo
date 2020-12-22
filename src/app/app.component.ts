import { Component, OnInit } from '@angular/core';
import { OdooService } from './shared/services/odoo.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'lista-pagos';

  constructor(private odooService: OdooService){}

  ngOnInit(){
    
  }
}
