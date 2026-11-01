$(document).ready(function(){
    $('.header').height($(window).height());
})

function updateProgress(percentage, increment){
    if(percentage > 100) percentage = 100;
    $('#progressBar').css('width', percentage+'%');
    $('#progressBar').html(percentage.toFixed(2)+'%');
    if(percentage < 100) setTimeout(updateProgress, 300, percentage+increment, increment);
    else{
        $('#result').css('visibility', 'visible')
    }
}