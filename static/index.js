function displayResults (reply) {
   $('#results').html($(reply).filter("#tables-or-not-found"));
   var width = $('#word').width() + $('#button').width(); //TODO: issue #14
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val();
   if (word) {
      var url = $SCRIPT_ROOT + "lookup/" + encodeURIComponent(word);
      $.ajax(url).done(displayResults);
   }
   event.preventDefault();
}

function setup () {
   $('#search').submit(onSubmit);
}

$(document).ready(setup);
