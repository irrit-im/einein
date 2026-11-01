function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        hours = parseInt(timer / (60 * 60), 10);
        minutes = parseInt((timer / 60) % 60, 10);
        seconds = parseInt(timer % 60, 10);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(hours + ":" + minutes + ":" + seconds);

        if (timer > 0) {
            timer--;
        }
    }, 1000);
}

jQuery(function ($) {
    var full_day = 24 * 60 * 60,
        display = $('#clock');
    startTimer(full_day, display);
});