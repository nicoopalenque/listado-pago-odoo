import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

const cudOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};
const cudOptionsXWWForm = {
    headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
};
const cudOptionsHtml = {
    headers: new HttpHeaders({ 'Content-Type': 'text/html; charset=utf-8' })
};

@Injectable({
    providedIn: 'root'
})
export class OdooService {
    private urlBase = environment.url_servicios_base;

    private api_get_ars = this.urlBase + '/list-ars'
    private api_get_all = this.urlBase + '/get-all'
    private api_get_usd = this.urlBase + '/list-usd'

    constructor(public http: HttpClient) { }

    getAll(): Observable<any>{
        return this.http.get(this.api_get_all);
    }

    getArs(): Observable<any> {
        return this.http.get(this.api_get_ars);
    }

    getUsd(): Observable<any>{
        return this.http.get(this.api_get_usd);
    }


    
}