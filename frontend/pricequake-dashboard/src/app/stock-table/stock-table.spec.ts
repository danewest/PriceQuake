import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StockTable } from './stock-table';

describe('StockTable', () => {
  let component: StockTable;
  let fixture: ComponentFixture<StockTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StockTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StockTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
