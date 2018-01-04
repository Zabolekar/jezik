function displayResults (reply) {
   $('#results').html(reply);
   var width = $('#word').width() + $('#button').width();
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val();
   if (word) {
      var url = $SCRIPT_ROOT + word;
      $.ajax(url).done(displayResults);
   }
   event.preventDefault();
}

function setup () {
   $('#search').submit(onSubmit);
}

$(document).ready(setup);