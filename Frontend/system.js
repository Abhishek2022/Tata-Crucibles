let counter1=0;
function clickCounter1() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter1 = counter1+1;
      document.querySelector(".progress-bar").style.width = counter1 + "%";
      document.getElementById("person").innerHTML = "Person";
    }
    document.getElementById("result1").innerHTML = counter1;
  }
}
function clickCounter2() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter1 = counter1-1;
      document.querySelector(".progress-bar").style.width = counter1 + "%";
    }
    if(counter1<0){
      counter1=0;
    }
    document.getElementById("result1").innerHTML = counter1;
  }
}

let counter2=0;
function clickCounter3() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter2 = counter2+1;
    }
    document.getElementById("result2").innerHTML = counter2;
  }
}
function clickCounter4() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter2 = counter2-1;
    }
    if(counter2<0){
      counter2=0;
    }
    document.getElementById("result2").innerHTML = counter2;
  }
}

let counter3=0;
function clickCounter5() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter3 = counter3+1;
    }
    document.getElementById("result3").innerHTML = counter3;
  }
}
function clickCounter6() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter3 = counter3-1;
    }
    document.getElementById("result3").innerHTML = counter3;
  }
  if(counter3<0){
    counter3=0;
  }
}

let counter4=0;
function clickCounter7() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter4 = counter4+1;
    }
    document.getElementById("result4").innerHTML = counter4;
  }
}
function clickCounter8() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter4 = counter4-1;
    }
    if(counter4<0){
      counter4=0;
    }
    document.getElementById("result4").innerHTML = counter4;
  }
}

let counter5=0;
function clickCounter9() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter5 = counter5+1;
    }
    document.getElementById("result5").innerHTML = counter5;
  }
}
function clickCounter10() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      counter5 = counter5-1;
    }
    if(counter5<0){
      counter5=0;
    }
    document.getElementById("result5").innerHTML = counter5;
  }
}

/*
if((counter1<=counter2) && (counter1<=counter3) && (counter1<=counter4) && (counter1<=counter5)){
  document.getElementById("result").innerHTML = "Counter1";
}
*/
let arr = [counter2, counter3, counter4, counter5];
let min = MATH.min(...arr)
document.getElementById("result").innerHTML = min;