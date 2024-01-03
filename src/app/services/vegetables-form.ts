export interface IGetVegInfoReq{
  VegName: string
}
export interface IGetVegInfoRes{
  VegName:string[]
}

export interface IGetVegPriceInfoRes{
  Pred: string;
  VegData:IGetVegPriceInfo
}
export interface IGetVegPriceInfo{
  Data: number[],
  dataLen: number,
  TimeStamp: string[]
}
export interface IGetVegPriceReq{
  VegName: string
}
export interface IGetRainInfoRes{
  YesterdayPrec: string
}
