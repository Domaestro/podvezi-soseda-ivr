// Переключатель типа поездки
switcher = document.getElementsByName('tripType');
addressSelectTitle = document.getElementById('addressSelectTitle');
function changeAddressTitle() {
    if (switcher[0].checked) {
        addressSelectTitle.innerHTML = "Откуда";
    }
    else {
        addressSelectTitle.innerHTML = "Куда";
    }
}


//TimePicker
var timepick = document.getElementById('timepicker');

// Установка текущего времени в форму
var now = new Date();
if (now.getMinutes() < 10)
    timepick.value = now.getHours()+":0"+now.getMinutes();
else
    timepick.value = now.getHours()+":"+now.getMinutes();

// Крутилка в модальном окне
var picker = new Picker(timepick, {
    container: '.picker-container',
    headers: true,
    format: 'HH:mm',
    inline: true,
    rows: 5
});

