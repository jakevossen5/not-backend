import { Component, OnInit, OnDestroy } from "@angular/core";
import noUiSlider from "nouislider";
const axios = require('axios');
declare var require: any
declare const Buffer

@Component({
  selector: "app-index",
  templateUrl: "index.component.html"
})
export class IndexComponent implements OnInit, OnDestroy {
  isCollapsed = true;
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

  makePostRequest() {

    let res = axios.post('http://127.0.0.1:5000/post', {
        'url': 'https://github.com/calebrotello/test'
    });

        /*
    console.log(`Status code: ${res.status}`);
    console.log(`Status text: ${res.statusText}`);
    console.log(`Request method: ${res.request.method}`);
    console.log(`Path: ${res.request.path}`);

    onsole.log(`Date: ${res.headers.date}`);
    console.log(`Data: ${res.data}`);
    */

  }
 
  submitCode(): void {
    this.makePostRequest();


/*
    var https = require('follow-redirects').https;
    var fs = require('fs');
    
    var options = {
      'method': 'POST',
      'hostname': 'localhost',
      'port': 5000,
      'path': '/post',
      'headers': {
        'Content-Type': 'application/json'
      },
      'maxRedirects': 20
    };
    
    var req = https.request(options, function (res) {
      var chunks = [];
    
      res.on("data", function (chunk) {
        chunks.push(chunk);
      });
      res.on("end", function (chunk) {
        var body = Buffer.concat(chunks);
        console.log(body.toString());
      });
      res.on("error", function (error) {
        console.error(error);
      });
    });
   var postData = JSON.stringify({"url":"https://github.com/calebrotello/test"});
    req.write(postData);    
   req.end();
*/
  }
}
