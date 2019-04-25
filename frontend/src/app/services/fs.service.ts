import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from 'angularfire2/firestore';
import { map } from 'rxjs/operators';
import 'rxjs/add/operator/map'

import { Judgement } from '../models/app.model';
import { Sentences } from '../models/app.model';

 import * as firebase from 'firebase/app';

  
@Injectable()
export class FsService {
  sent_number:string;
  itemsCollection: AngularFirestoreCollection<Judgement>;
  items: Observable<Judgement[]>;
  itemDoc: AngularFirestoreDocument<Judgement>;
  odc:Observable<Judgement[]>;
  userDoc:AngularFirestoreDocument<Judgement>;
  userDoc1:AngularFirestoreDocument<Judgement>;
  item:Sentences;

  tasks: Observable<Judgement[]>;
  sentence: Observable<Sentences[]>;
   id:string;
  constructor( private afs: AngularFirestore ) { 
    //this.itemsCollection = this.afs.collection('items', ref => ref.orderBy('title','asc'));
  
  }
getItems(){
   this.id,this.items = this.afs.collection('cases').snapshotChanges().pipe(
    map(actions => {
    return actions.map(a => {
        const data = a.payload.doc.data() as Judgement;
        const id = a.payload.doc.id;
        return { id, ...data };
    });
    })
);
  console.log(this.items);
   return this.items;
  }

  getItemsNotAnnotated(){
   this.id,this.items = this.afs.collection('cases',ref => ref.where('annotated', '==', 'no').orderBy('id','asc') ).snapshotChanges().pipe(
    map(actions => {
    return actions.map(a => {
        const data = a.payload.doc.data() as Judgement;
        const id = a.payload.doc.id;
        return { id, ...data };
    });
    })
);
  console.log(this.items);
   return this.items;
  }
  getItemsResumeAnnotation(){
   this.id,this.items = this.afs.collection('cases',ref => ref.where('annotated', '==', 'yes').orderBy('id','asc') ).snapshotChanges().pipe(
    map(actions => {
    return actions.map(a => {
        const data = a.payload.doc.data() as Judgement;
        const id = a.payload.doc.id;
        return { id, ...data };
    });
    })
    ); 
  
   return this.items;
  }
  getSentences(case_name:string){
      this.userDoc = this.afs.doc<Judgement>('cases/'+case_name);
    this.tasks = this.userDoc.collection<Judgement>('sentences',ref => ref.orderBy('serial_no', 'asc')).valueChanges();


    //console.log(this.tasks);
 
  
    return this.tasks
  }
  
 updateSentence(id:string,item:Sentences,index:number){  
   this.sent_number=index.toString();
    this.userDoc1 = this.afs.doc('cases/'+id+'/sentences/'+this.sent_number);
    this.userDoc1.update(item);
    console.log("UPDATE done",this.userDoc1);
    
     return this.userDoc1
 }
    updateAnnotator(id:number,item:Judgement){  
    item.annotated="yes"; 
    this.userDoc = this.afs.doc<Judgement>('cases/'+id);
    this.userDoc.update(item);
    console.log("UPDATE done",this.userDoc);
     return this.userDoc
 }
       

}
