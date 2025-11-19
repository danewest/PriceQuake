import { Component, signal } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { StockTable } from './stock-table/stock-table';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MatToolbarModule, MatCardModule, StockTable],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('pricequake-dashboard');
}
