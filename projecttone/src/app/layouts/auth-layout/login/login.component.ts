import { Component, OnInit, OnDestroy } from '@angular/core';
import { NgForm } from '@angular/forms';
import { AuthService } from '../auth-service/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
 // username: string;
 // password : string;

  constructor(private authservice: AuthService) {}

  ngOnInit() {
  }
  ngOnDestroy() {
  }
  onLogin(form: NgForm){
    const username = form.value.username;
    const password = form.value.password;
    this.authservice.LoginUser(username,password);


  }
}
