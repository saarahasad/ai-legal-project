import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { NgModule } from '@angular/core';
import { FormsModule ,ReactiveFormsModule}   from '@angular/forms';
import { AngularFireModule } from 'angularfire2';
import { AngularFirestoreModule } from 'angularfire2/firestore';

import { environment } from '../environments/environment';

import { AppComponent } from './app.component';
import {RouterModule, Routes} from '@angular/router';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatGridListModule,MatExpansionModule,MatCheckboxModule,MatRadioModule,MatInputModule, MatTabsModule,MatSnackBarModule, MatDialogModule,MatProgressSpinnerModule, MatSelectModule,MatButtonModule, MatCardModule, MatMenuModule, MatToolbarModule, MatIconModule, MatSidenavModule, MatListModule } from '@angular/material';

import { AnnotateCaseComponent } from './annotate-case/annotate-case.component';
import { HomeComponent } from './home/home.component';

import { FsService } from "./services/fs.service";
 import * as firebase from 'firebase/app';
import { AboutComponent } from './about/about.component';
import { CategorizationComponent } from './categorization/categorization.component';
import { SummarizationComponent } from './summarization/summarization.component';
import { CaseCategoryComponent } from './case-category/case-category.component';
const routes: Routes = [
  {
    path: '',
    redirectTo: 'about',
    pathMatch: 'full'
  },
  {
    path: 'about',
    component: AboutComponent
  },
   {
    path: 'categorization',
    component: CategorizationComponent
  },
  {
    path: 'summarization',
    component: SummarizationComponent
  },
  {
    path: 'case-category',
    component: CaseCategoryComponent
  },
  {
    path: 'annotate',
    component: HomeComponent
  },
    {
    path: 'annotate-case/:name',
    component: AnnotateCaseComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    AnnotateCaseComponent,
    HomeComponent,
    AboutComponent,
    CategorizationComponent,
    SummarizationComponent,
    CaseCategoryComponent,
  ],
  imports: [
   BrowserModule,
   ReactiveFormsModule,
   RouterModule.forRoot(routes),
    BrowserAnimationsModule,
    MatRadioModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    MatInputModule,
     MatSelectModule,
     MatGridListModule,
     MatTabsModule,
     MatSnackBarModule,
    HttpClientModule,
    MatButtonModule,
    MatExpansionModule,
    MatMenuModule,
    MatCardModule,
    MatCheckboxModule,
    MatToolbarModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    FormsModule,
    AngularFireModule.initializeApp(environment.firebase, 'ai-legal-system'),
    AngularFirestoreModule
  ],
  providers: [FsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
