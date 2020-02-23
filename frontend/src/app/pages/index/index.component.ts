import { Component, OnInit, OnDestroy, Inject, ViewChild, ElementRef, AfterViewInit } from "@angular/core";
import noUiSlider from "nouislider";
const axios = require('axios');
declare var require: any
declare const Buffer

// let res_id = ""

@Component({
  selector: "app-index",
  templateUrl: "index.component.html"
})
export class IndexComponent implements OnInit, OnDestroy {
  isCollapsed = true;
  api: string = "Your API will be here."
  focus;
  focus1;
  focus2;
  date = new Date();
  pagination = 3;
  pagination1 = 1;
  constructor() { }
  scrollToDownload(element: any) {
    element.scrollIntoView({ behavior: "smooth" });
  }
  ngOnInit() {
    var body = document.getElementsByTagName("body")[0];
    body.classList.add("index-page");

    var slider = document.getElementById("sliderRegular");

    noUiSlider.create(slider, {
      start: 40,
      connect: false,
      range: {
        min: 0,
        max: 100
      }
    });

    var slider2 = document.getElementById("sliderDouble");

    noUiSlider.create(slider2, {
      start: [20, 60],
      connect: true,
      range: {
        min: 0,
        max: 100
      }
    });
  }

  ngOnDestroy() {
    var body = document.getElementsByTagName("body")[0];
    body.classList.remove("index-page");
  }

  @ViewChild('urlbox', { static: true }) input: ElementRef;

  ngAfterViewInit(): string {
    console.log(this.input.nativeElement.value);
    return this.input.nativeElement.value;
  };

  makePostRequest() {

    // return res.response.data;
  }

  submitCode(): void {

    // get url from text input
    var u = this.ngAfterViewInit();

    // remove last / if it exists
    if (u.charAt(u.length - 1) == '/') {
      u = u.substr(0, u.length - 1);
    }

    // split by /
    var uSplit = u.split('/');

    // get last two element
    var uName = uSplit[uSplit.length - 2];
    var uRepo = uSplit[uSplit.length - 1];

    // concat uname , project
    uName = uName.concat(',');
    var uLink = uName.concat(uRepo);
    console.log(uLink);

    // pass to server
    var serverUrl = 'http://127.0.0.1:5000/post/'.concat(uLink);

    let res = axios.post(serverUrl, {
      headers: {
        'Access-Control-Allow-Origin:': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'multipart/form-data'
      },
    }).then((response) => {
      console.log(response.data)
      this.api = 'http://127.0.0.1:5000/r/' + response.data
    });
    // var api = this.makePostRequest();
    // this.api = api;
    // console.log(api);
  }
}
