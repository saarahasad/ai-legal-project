import { Component, OnInit } from '@angular/core';
import { Category } from '../models/app.model';
import { FsService } from "../services/fs.service";
import { Sentences } from '../models/app.model';

@Component({
  selector: 'app-categorization',
  templateUrl: './categorization.component.html',
  styleUrls: ['./categorization.component.css']
})
export class CategorizationComponent implements OnInit {
  categories:Category[]= [];
  sentences: Sentences[]=[];

  constructor(private fsService:FsService) {
   
   }
  ngOnInit() {
      this.categories[0]={};
      this.categories[1]={};
      this.categories[2]={};
      this.categories[3]={};
      this.categories[4]={};
      this.categories[5]={};
      this.categories[6]={};
      this.categories[7]={};
      this.categories[0].id=0;
      this.categories[0].name='Others';
       this.categories[0].sentences=[]
      this.categories[1].id=1;
      this.categories[1].name='Identifying the case';
      this.categories[1].sentences=[]
      this.categories[2].id=2;
      this.categories[2].name='Establishing facts of the case';
      this.categories[2].sentences=[]
      this.categories[3].id=3;
      this.categories[3].name='Arguing the case';
      this.categories[3].sentences=[]
      this.categories[4].id=4;
      this.categories[4].name=' History of the case';
      this.categories[4].sentences=[]
      this.categories[5].id=5;
      this.categories[5].name='Arguments';
      this.categories[5].sentences=[]
      this.categories[6].id=6;
      this.categories[6].sentences=[]
      this.categories[6].name=' Ratio decidendi';
      this.categories[7].id=7;
      this.categories[7].name=' Final decision';
      this.categories[7].sentences=[]
      this.fsService.getSentences('1').subscribe(sentences => {
      console.log("Sentences get",sentences);
      console.log("Sentences get done");
      this.sentences=sentences;
      
      this.sentences.forEach(function (element){
         if(element.category==0){
       this.categories[0].sentences.push(element.data);
      }
      if(element.category==1){
       this.categories[1].sentences.push(element.data);
      }
      if(element.category==2){
       this.categories[2].sentences.push(element.data);
      }
      if(element.category==3){
       this.categories[3].sentences.push(element.data);
      } 
       if(element.category==4){
       this.categories[4].sentences.push(element.data);
      }      
       if(element.category==5){
       this.categories[5].sentences.push(element.data);
      } 
       if(element.category==6){
       this.categories[6].sentences.push(element.data);
      } 
       if(element.category==7){
       this.categories[7].sentences.push(element.data);
      } 
      }.bind(this));
    
    });

  
    
  }

  


}
