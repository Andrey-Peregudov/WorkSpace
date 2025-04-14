//Создание переменных обращающихся к элементам по id
var span = document.getElementById('span');
var dateNow = document.getElementById('date_now'); 

// Функция определения текущего времени
function updateTime() {
  var d = new Date();
  var s = d.getSeconds();
  var m = d.getMinutes();
  var h = d.getHours();
//Форматирование времени в формат “чч:мм:сс"
  span.textContent = ("0" + h).substr(-2) + ":" + ("0" + m).substr(-2) + ":" + ("0" + s).substr(-2);
}

// Функция определения текущей даты
function updateDate() {
  var d = new Date();
  var day = d.getDate();
  var month = d.getMonth();
  var year = d.getFullYear();
// Форматирование даты в "ГГГГ-ММ-ДД"
  var formattedDate = year + "-" + ("0" + month).substr(-2) + "-" + ("0" + day).substr(-2);
  dateNow.textContent = formattedDate;
}

// Обновление даты и времени каждую секунду
setInterval(updateTime, 1000);
setInterval(updateDate, 1000);

// Вызов функций
updateTime();
updateDate();