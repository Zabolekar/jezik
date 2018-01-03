$(document).ready( function() {
  $('#search').submit(function(event) {
     $.ajax($SCRIPT_ROOT + $('#word').val()).done(function (reply) {
        $('#results').html(reply);
     });
     event.preventDefault();
  });
});