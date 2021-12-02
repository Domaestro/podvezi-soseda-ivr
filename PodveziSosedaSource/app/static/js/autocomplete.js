"use strict";

let autocomplete = (inp, arr) => {
  let currentFocus;

  inp.addEventListener("input", function(e) {
    let a, //OUTER html
      b, // INNER html
      i, //Counter
      val = this.value;

    /*Закрыть все открытые подсказки*/
    closeAllLists();

    if (!val) {
      return false;
    }

    currentFocus = -1;

    /*Создание div со списком адресов*/
    a = document.createElement("DIV");
    
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items list-group text-left fs-6");
    

    this.parentNode.appendChild(a);


    for (i = 0; i < arr.length; i++) {
      b = document.createElement("DIV");
      b.setAttribute("class","list-group-item list-group-item-action");
      b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
      b.innerHTML += arr[i].substr(val.length);
      b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

      b.addEventListener("click", function(e) {
        inp.value = this.getElementsByTagName("input")[0].value;
        closeAllLists();
      });
      a.appendChild(b);
    }
  });
  
  inp.addEventListener("keydown", function(e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });
  
  let addActive = (x) => {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    x[currentFocus].classList.add("active");
  }
  
  let removeActive = (x) => {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("active");
    }
  }
  
  let closeAllLists = (elmnt) => {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  
  document.addEventListener("click", function(e) {
    closeAllLists(e.target);
  });
  
};

/*Массив адресов*/
let address_labels = [
];


const user_agent = Math.random().toString(16).substr(2, 8)
const provider = new GeoSearch.OpenStreetMapProvider({
    params: {
        email: user_agent,
        'accept-language': 'ru', 
        countrycodes: 'ru',
        },
})

const addressInput = document.getElementById('addressInput')

async function search() {
    // Вывод подсказок
    if (addressInput.value.length > 2) {
      const results = await provider.search({ query: addressInput.value });
      address_labels = [ ]
      for (var i = 0; i < results.length; i++) {
          address_labels.push(results[i].label)
      }
      autocomplete(addressInput, address_labels);
    } 
}


// Функция, вызывающаяся при нажатии на кнопку очистки адреса
function clear_input() {
  addressInput.value = ""
}


// Все поля формы
const tripTypeRadio = document.getElementsByName("tripType");
const tripDay = document.getElementById("tripDay");
const timeInput = document.getElementById("timepicker")
const passengersNum = document.getElementById("passengersNum")


// Функция при нажатии на ссылку выбора места с карты
function safe_form_input() {
  // const request = new XMLHttpRequest();
  // request.open("POST", `/drive/safe_form_input`);
  // request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  // let data = JSON.stringify({ "tripType": tripTypeRadio, 
  //                             "address": addressInput.value, 
  //                             "tripDay": tripDay.value, 
  //                             "timeInput": timeInput.value, 
  //                             "passengersNum": passengersNum.value})
  // request.send(data);
  // console.log(data)
  const request = new XMLHttpRequest();
  let tripType_;
  if (tripTypeRadio[0].checked) tripType_ = 1
  else tripType_ = 2
  request.open('GET', `/drive/safe_form_input?triptype=`+tripType_+`&address=`+addressInput.value+`&tripday=`+tripDay.value+`&timeinput=`+timeInput.value+`&passengers=`+passengersNum.value);
  request.send();
}


// Автозаполнение формы сохраненными значениями

const request = new XMLHttpRequest();
request.open('GET', `/drive/get_form_input`);
request.responseType = 'json';
request.send();
request.onload = () => {
  let responseObj = request.response
  addressInput.value = responseObj.address;
  tripTypeRadio[responseObj.radioChecked].checked = true;
  tripDay.options[responseObj.tripDayNum].selected = true;
  if (responseObj.rawTime != "") timeInput.value = responseObj.rawTime;
  passengersNum.options[responseObj.passengersValue].selected = true;
}; 
