import { Component, OnInit } from '@angular/core';
import { Table } from '../../models/table';
import { OdooService } from '../../shared/services/odoo.service';
import * as jsonexport from "jsonexport/dist";
import { DomSanitizer } from '@angular/platform-browser';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit {

  elementData: Table[] = [];
  options: any;
  headers = [
    {label: 'CUIT', key: 'cuit'},
    {label: 'Nombre', key: 'cliente'},
    {label: 'Monto', key: 'monto'},
    {label: 'Moneda', key: 'moneda'},
    {label: 'Forma Pago', key: 'formaPago'},
    {label: 'CBU/ALIAS', key: 'cbuAlias'}
  ]

  displayedColumns: string[] = ['CUIT', 'Nombre', 'Monto', 'Moneda', 'Forma Pago', 'CBU/ALIAS'];
  dataSource = this.elementData;  

  headerUSD:any;
  exportUSD: any = '';
  footerUSD: any;
  resultExportUSD: any = '';
  fileUSD;

  headerARS: any;
  exportARS: any = '';
  footerARS: any;
  resultExportARS: any = '';
  fileARS;
  constructor(private odooService: OdooService, private sanitizer: DomSanitizer) { }

  async ngOnInit() {
    await this.odooService.getAll().subscribe(res=>{
      console.log(res);
      for(let i=0; i<res.length; i++){
        if(res[i].MONTO_ARS_TRANSFER === "0" && res[i].MONTO_ARS_ATM ==="0"){
          let paramMonto;
          let cbu;
          let pago;
          let moneda;
          if(res[i].MONTO_USD_TRANSFER === "0"){
            paramMonto = res[i].MONTO_USD_ATM
            cbu = '-'
            pago = 'Ventanilla'
            moneda = 'USD'
          }else{
            paramMonto = res[i].MONTO_USD_TRANSFER
            cbu = res[i].CBU_USD
            pago = 'Transferencia'
            moneda = 'USD'
          }
          const params = {
            cuit: res[i].CUIT,
            cliente: res[i].CLIENTE,
            monto: paramMonto,
            moneda: moneda,
            formaPago: pago,
            cbuAlias: cbu,
          }
          this.elementData.push(params)
        }else{
          let paramMonto;
          let cbu;
          let pago;
          let moneda;
          if(res[i].MONTO_ARS_TRANSFER === "0"){
            paramMonto = res[i].MONTO_ARS_ATM
            cbu = '-'
            pago = 'Ventanilla'
            moneda = 'ARS'
          }else{
            paramMonto = res[i].MONTO_ARS_TRANSFER
            cbu = res[i].CBU_USD
            pago = 'Transferencia'
            moneda = 'ARS'
          }
          const params = {
            cuit: res[i].CUIT,
            cliente: res[i].CLIENTE,
            monto: paramMonto,
            moneda: moneda,
            formaPago: pago,
            cbuAlias: cbu,
          }
          this.elementData.push(params)
        }
        
      }
      
    })

    this.odooService.getArs().subscribe(res=>{
      console.log(res);
      for(let i=0; i<res.length; i++){
        if(i===0){
          this.headerARS = res[0].header;
        }else{
          if(i===res.length-1){
            this.footerARS = res[i].footer;
          }else{
            this.exportARS += res[i].body + '\n';
          }
        }
      }
      this.resultExportARS= this.headerARS + '\n' + this.exportARS +  this.footerARS
      console.log(this.resultExportARS);
    })

    this.odooService.getUsd().subscribe(res=>{
      //console.log('Lista USD: ', res);
      for(let i=0; i<res.length; i++){
        if(i===0){
          this.headerUSD = res[0].header;
        }else{
          if(i===res.length-1){
            this.footerUSD = res[i].footer;
          }else{
            this.exportUSD += res[i].body + '\n';
          }
        }
      }
      this.resultExportUSD= this.headerUSD + '\n' + this.exportUSD +  this.footerUSD
      console.log(this.resultExportUSD);
    })

    if(this.elementData.length>0){
      this.dataSource = this.elementData
    }

    console.log('tipo de dato de resultexport ', typeof this.resultExportUSD)

    
    const dataUSD = this.resultExportUSD;
    const blobUSD = new Blob([dataUSD], { type: 'text/plain;charset=utf-8' });
    this.fileUSD = this.sanitizer.bypassSecurityTrustResourceUrl(window.URL.createObjectURL(blobUSD));
  }

  downloadFiles(){
    var blob = new Blob([this.resultExportARS], {type: "text/plain;charset=utf-8"});
    saveAs(blob,'exportARS.txt') 

    var blob2 = new Blob([this.resultExportUSD], {type: "text/plain;charset=utf-8"});
    saveAs(blob2,'exportUSD.txt')
  }

}
