function displayResults (reply) {
   $('#results').html(reply);
}

function onSubmit (event) {
   var url = $SCRIPT_ROOT + $('#word').val();
   $.ajax(url).done(displayResults);
   event.preventDefault();
}

$(document).ready(function() {
  $('#search').submit(onSubmit);
});