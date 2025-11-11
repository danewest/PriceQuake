import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
// import { provideAnimations } from '@angular/platform-browser/animations';
// import { provideCharts, withDefaultRegisterables } from 'ng2-charts';

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
