import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration } from 'chart.js';
@Component({
  selector: 'app-stock-table',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './stock-table.html',
  styleUrl: './stock-table.scss',
})
export class StockTable {
  lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: ['9:00', '9:05', '9:10', '9:15', '9:20'],
    datasets: [
      {
        data: [195.1, 195.3, 195.0, 194.9, 195.2],
        label: 'AAPL Stock',
        fill: false,
        tension: 0.3,
        borderColor: '#5c00d4',
        pointBackgroundColor: 'rgba(0,120,212,0.2)',
        pointRadius: 3,
        borderWidth: 2
      }
    ]
  };

  lineChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false
  };
}
