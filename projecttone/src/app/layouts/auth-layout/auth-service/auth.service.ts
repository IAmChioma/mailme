import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { routerNgProbeToken } from '@angular/router/src/router_module';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  baseUrl = environment.apiUrl;
 // username: string;
 // password: string;
/* https://api.lexigram.io/v1/lexigraph/search?q=diabetes This is an openAPi with only bearer token to access public health details */
  constructor(private http : HttpClient, private router: Router) { }

  LoginUser(username:string, password:string){
    const user = {
      "username":username,
      "password": password
    }
    return this.http.post(`${this.baseUrl}/auth_api/login/`, user).subscribe(
      (data)=>{
        this.router.navigate(['/dashboard']);
        console.log(data)
      },
      (err)=>{
        console.log(err)
      }
    );
  }
  onLogout(){
    return this.http.get(`${this.baseUrl}/auth_api/logout`).subscribe(
      (data)=>{
        this.router.navigate(['/login']);
        console.log(data)}
    )
  }

  RegisterUser(username:string, password:string, firstname:string,lastname:string,email:string){
    const newuser ={
      "username":username,
      "password": password,
      "firstname": firstname,
      "lastname":lastname,
      "email": email
    }
    return this.http.post(`${this.baseUrl}/auth_api/register`, newuser).subscribe(
      (data)=>{
        this.router.navigate(['/login']);
        console.log(data)
      },
      (err)=>{
        console.log(err)
      }
    )
  }
}
