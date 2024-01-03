import { Component, OnInit } from '@angular/core';
import { VegetablesService } from './services/vegetables.service';
import { IGetVegPriceReq } from './services/vegetables-form';
import * as echarts from 'echarts';
import { NgxEchartsModule } from 'ngx-echarts';
import { EChartsOption } from 'echarts';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'vegetable';

  temperature = '28°C';

  rainMl!: string;

  vegetables!: string[]

  price !: number[]
  time!: string[]
  predict!: string

  selected!: string

  constructor(
    private vegService: VegetablesService
  ) { }

  ngOnInit() {
    this.getVeg(),
      this.getRain()
  }

  getVeg() {
    this.vegService.getVegList().subscribe(res => {
      this.vegetables = res.VegName
    })
  }
  today: number = Date.now();
  loading = false
  getPrice() {
    const params = this.selected
    console.log(params);
    this.vegService.getVegPriceList(params as unknown as IGetVegPriceReq).subscribe(res => {
      this.price = res.VegData.Data
      if (this.price != null){
        this.loading = true
      }
      this.time = res.VegData.TimeStamp
      this.predict = res.Pred
      if (this.predict == 'up'){
        this.predict = '漲價'
      }
      else{
        this.predict = '下降'
      }
      console.log(res.Pred);
      this.option = {
        xAxis: {
          type: 'category',
          data: this.time
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: this.price,
            type: 'line'
          }
        ]

      }
    })
  }

  getRain() {
    this.vegService.getRain().subscribe(res => {
      this.rainMl = res.YesterdayPrec
      console.log(res);
    })
  }

  option!: EChartsOption


}

