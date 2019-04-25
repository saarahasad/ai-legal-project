import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-case-category',
  templateUrl: './case-category.component.html',
  styleUrls: ['./case-category.component.css']
})
export class CaseCategoryComponent{

  constructor(private httpClient: HttpClient) {
  }
  serverData: any;
  Case(){
    this.httpClient.get('http://127.0.0.1:5000/case-category').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }
}