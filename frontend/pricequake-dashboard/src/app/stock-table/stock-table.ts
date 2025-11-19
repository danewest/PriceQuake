import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration } from 'chart.js';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-stock-table',
  standalone: true,
  imports: [CommonModule, BaseChartDirective, MatFormFieldModule, MatSelectModule],
  templateUrl: './stock-table.html',
  styleUrl: './stock-table.scss',
})
export class StockTable {
  tickers = ['AAPL', 'MSFT', 'GOOGL'];
  selectedTicker = 'AAPL';

  lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: ['9:00', '9:05', '9:10', '9:15', '9:20'],
    datasets: [
      {
        type: 'line',
        showLine: true,
        data: [195.1, 195.3, 195.0, 194.9, 195.2],
        label: 'AAPL Stock',
        fill: false,
        tension: 0.3,
        borderColor: '#5c00d4',
        backgroundColor: 'rgba(0,120,212,0.1)',
        pointBackgroundColor: 'rgba(0,120,212,0.2)',
        pointRadius: 3,
      }
    ]
  };

  lineChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    elements: { line: { borderWidth: 2} },
    scales: {
      x: { title: { display: true, text: 'Time'} },
      y: { title: { display: true, text: 'Price ($)' } },
    },
  };

  onTickerChange() {
    // later will fetch backend data
    this.lineChartData.datasets[0].label = this.selectedTicker;
  }
}
