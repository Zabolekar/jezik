function displayResults (reply) {
   $('#results').html($(reply).filter("#tables-or-not-found"));
   var width = $('#word').width() + $('#button').width(); //TODO: issue #14
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val().replace(/^\/*/, "");
   /*
      Flask needs a custom converter for handling leading slashes in queries.
      Luckily for us, a word shouldn't contain them anyway, a user might only
      enter them by accident, so it's easier to just remove them.
   */
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
