import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  serverData: JSON;
  employeeData: JSON;
  
  constructor(private httpClient: HttpClient) {
  }

  getImage() {
    this.httpClient.get('http://127.0.0.1:5000/image/image.jpeg').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }


  getPdf() {
    this.httpClient.get('http://127.0.0.1:5000/pdf/pdf1.pdf').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }

}
