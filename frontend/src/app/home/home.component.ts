import { Component, OnInit ,ViewEncapsulation} from '@angular/core';
import { FsService } from "../services/fs.service";
import { Judgement } from '../models/app.model';
import { Sentences } from '../models/app.model';
import {Router} from '@angular/router';

export interface Annotator {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
    encapsulation: ViewEncapsulation.None

})

export class HomeComponent implements OnInit {
  selected_case:Judgement;
  selected_annotated="annotator-1";
  selected_case_2:Judgement;
  selected_annotated_2="annotator-1";
  items: Judgement[];
  resumeItems: Judgement[];
  item_name:Judgement;
  constructor(private fsService:FsService, private router: Router) { }
title = 'frontend';
 foods: Annotator[] = [
    {value: 'steak-0', viewValue: 'Steak'},
    {value: 'pizza-1', viewValue: 'Pizza'},
    {value: 'tacos-2', viewValue: 'Tacos'}
  ];
  annotators: Annotator[] = [
    {value: 'annotator-1', viewValue: 'Annotator 1'},
    {value: 'annotator-2', viewValue: 'Annotator 2'},
    {value: 'annotator-3', viewValue: 'Annotator 3'}
  ];
  ngOnInit() {
       this.fsService.getItemsNotAnnotated().subscribe(items => {
 //     console.log(items);
      this.items = items;
      
    });
    this.fsService.getItemsResumeAnnotation().subscribe(items => {
      this.resumeItems = items;
    });

  }

  onSubmit() {
  //console.log("annoator",this.selected_annotated)
  this.selected_case.annotator_name=this.selected_annotated;
  this.fsService.updateAnnotator(this.selected_case.id,this.selected_case);
  this.router.navigate(['/annotate-case/', this.selected_case.id]); 
}
onSubmitResume() {
  //console.log("annoator",this.selected_annotated)
  this.selected_case_2.annotator_name=this.selected_annotated_2;
  this.fsService.updateAnnotator(this.selected_case_2.id,this.selected_case_2);
  this.router.navigate(['/annotate-case/', this.selected_case_2.id]); 
}

}
