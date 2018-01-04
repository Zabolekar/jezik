function displayResults (reply) {
   $('#results').html(reply);
}

function onSubmit (event) {
   var url = $SCRIPT_ROOT + $('#word').val();
   $.ajax(url).done(displayResults);
   event.preventDefault();
}

function setup () {
   $('#search').submit(onSubmit);
}

$(document).ready(setup);