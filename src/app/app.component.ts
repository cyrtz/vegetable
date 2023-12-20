import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'vegetable';

  temperature = '28°C';

  rainMl = '100ml';

  vegControl = new FormControl<vegetable | null>(null, Validators.required);
  vegetables: vegetable[] = [
    {name: '蔥', price: '20'},
    {name: '高麗菜', price: '30'},
    {name: '空心菜', price: '40'},
  ];

}

interface vegetable {
  name: string;
  price: string;
}
