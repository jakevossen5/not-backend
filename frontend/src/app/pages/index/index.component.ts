import { Component, OnInit, OnDestroy, Inject,ViewChild,ElementRef,AfterViewInit } from "@angular/core";
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

  @ViewChild('urlbox', {static: true}) input:ElementRef;

  ngAfterViewInit() {
    console.log(this.input.nativeElement.value);
    return this.input.nativeElement.value;
  };

  makePostRequest() {

    // get url from text input
    var u = this.ngAfterViewInit();

    // remove last / if it exists
    if (u.charAt(u.length-1) == '/'){
      u = u.substr(0, u.length-1);
    }

    // split by /
    var uSplit = u.split('/');

    // get last two element
    var uName = uSplit[uSplit.length-2];
    var uRepo = uSplit[uSplit.length-1];

    // concat uname , project
    uName = uName.concat(',');
    var uLink = uName.concat(uRepo);
    console.log(uLink);

    // pass to server
    //var bodyFormData = new FormData();
    //bodyFormData.set('url', 'asdfa');

    var serverUrl = 'http://localhost:5000/post/'.concat(uLink);

    let res = axios.post(serverUrl, {
      headers: {
        'Access-Control-Allow-Origin:': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'multipart/form-data'
      },
    }).then(function (response) {
      console.log(response)

    });
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
