$(document).ready(function(){
  $('#content').summernote({
  minHeight: 300,
  focus: true
  // lang: 'pl-PL'
      });
  $('#reset-btn').on('click', function(){
       $('#content').summernote('reset')
   });
  $('.card').css("width", "100%");


});