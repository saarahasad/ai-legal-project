import { Component, OnInit ,ViewChild, ElementRef } from '@angular/core';

import { FsService } from "../services/fs.service";
import { DataSource } from '@angular/cdk/collections';
import { Judgement } from '../models/app.model';
import { Sentences } from '../models/app.model';
import { ActivatedRoute } from '@angular/router';
import { ConnectionService } from 'ng-connection-service';
import { AlertsService } from 'angular-alert-module';
import {MatSnackBar} from '@angular/material';

export interface Category {
  value: string;
  viewValue: string;
}


@Component({
  selector: 'app-annotate-case',
  templateUrl: './annotate-case.component.html',
  styleUrls: ['./annotate-case.component.css']
})

export class AnnotateCaseComponent implements OnInit  {
   status = 'ONLINE';
  isConnected = true;
  items: Judgement[]=[];
  item_name:Judgement;
  sentences: Sentences[];
  printedOption: string;
  selected="2";
 color = 'warm';
  mode = 'indeterminate';
  display_category:string="99";
    foods: Category[] = [
    {value: '99', viewValue: 'Select'},
    {value: '0', viewValue: 'Other'},
    {value: '1', viewValue: 'Identifying the case'},
    {value: '2', viewValue: 'Establishing facts of the case'},
    {value: '3', viewValue:  'Arguing the case'},
    {value: '4', viewValue:  'History of the case'},
    {value: '5', viewValue:  'Arguments '},
    {value: '6', viewValue:  'Ratio'},
    {value: '7', viewValue:  'Final Decision'}
   ];
  case_id: string;
  private sub: any;
  name_to_display:string;
  
  constructor(private fsService:FsService, private route: ActivatedRoute,private connectionService: ConnectionService,private snackBar: MatSnackBar) {
     this.connectionService.monitor().subscribe(isConnected => {
      this.isConnected = isConnected;
      if (this.isConnected) {
        
        this.status = "ONLINE";
      }
      else {
          this.openSnackBar()

        this.status = "OFFLINE";
      }
    })
  }
  openSnackBar() {
    this.snackBar.open("Internet Connection is lost!", "Close", {
      duration: 5000,
    });
  }
  
  
    ngOnInit() {
     
     this.sub = this.route.params.subscribe(params => {
       this.case_id = params['name']; // (+) converts string 'id' to a number

       // In a real app: dispatch action to load the details here.
    });

    console.log("ngonit",this.case_id);
    this.fsService.getItems().subscribe(items => {
      console.log(items);
      this.items = items;     
    
      this.items.forEach(function (value) {
          if(value.id==this.case_id){
            this.name_to_display=value.name;
          }
      }.bind(this));
    });
    
     this.fsService.getSentences(this.case_id).subscribe(sentences => {
      console.log("Sentences get",sentences);
        console.log("Sentences get done");

      this.sentences=sentences;
    
    });
     
  }
  
   onChange(selectedValue, index) {
    
    //console.log("id",this.case_id)
    this.sentences[index].category = selectedValue;
      this.fsService.updateSentence(this.case_id,this.sentences[index],index+1);
      this.foods.forEach(function (element){
      if(element.value==selectedValue){
        this.display_category=element.viewValue;
      }
   }.bind(this));

  }

   onChangePriority(selectedValue, index) {
    
    //console.log("id",this.case_id)
    this.sentences[index].priority = selectedValue;
    console.log("priority",selectedValue)
      this.fsService.updateSentence(this.case_id,this.sentences[index],index+1);

  }
}
