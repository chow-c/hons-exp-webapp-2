function countdown() {
var seconds = parseInt($('#countdown').html(), 10);
if (seconds == 0) {
  //$('#countdown').html('Finished!');
  $('#submit').click();
  $('#countdown').html('46')
  countdown();
  return;
}
--seconds;
$('#countdown').html(seconds)
setTimeout(countdown, 1000);
};