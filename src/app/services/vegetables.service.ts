import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IGetRainInfoRes, IGetVegInfoReq, IGetVegInfoRes, IGetVegPriceInfoRes, IGetVegPriceReq } from './vegetables-form';

@Injectable({
  providedIn: 'root'
})
export class VegetablesService {

  constructor(
    private http: HttpClient
  ) { }

  baseUrl = 'http://10.25.1.134:5000'

  getVegList(): Observable<IGetVegInfoRes> {
    const apiUrl = this.baseUrl + '/GetAllVeg';
    return this.http.get<IGetVegInfoRes>(apiUrl);
  }


  getVegPriceList(params: IGetVegPriceReq): Observable<IGetVegPriceInfoRes> {
    const apiUrl = this.baseUrl + '/GetData?VegName='+params;
    return this.http.get<IGetVegPriceInfoRes>(apiUrl);
  }

  getRain(): Observable<IGetRainInfoRes> {
    const apiUrl = this.baseUrl + '/getPreDayPrec';
    return this.http.get<IGetRainInfoRes>(apiUrl);
  }
  statisticsOfTheDayOptions() {
    return {
      dataZoom: {
        show: true,
        type: 'slider',
        top: '90%',
        start: 0,
        end: 100
      },
      tooltip: {
        trigger: 'axis'
      },
      grid: {
        bottom: 80,
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
      },
      yAxis: {
        type: 'value'
      }
    }
  }

}
