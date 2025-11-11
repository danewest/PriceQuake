import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { StockTable } from './stock-table/stock-table';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, StockTable],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('pricequake-dashboard');
}
