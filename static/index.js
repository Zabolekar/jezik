function displayResults (reply) {
   $('#results').html($(reply).filter("#tables-or-not-found"));
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val(),
       inputYat = $('input[name=inputYat]:checked').val(),
       outputYat = $('input[name=outputYat]:checked').val();
   if (word) {
      var url = $SCRIPT_ROOT + "lookup/" +
                encodeURIComponent(word) +
                "?inputYat=" + inputYat +
                "&outputYat=" + outputYat;
      $.ajax(url).done(displayResults);
   }
   event.preventDefault();
}

function addString (s, input) {
   var old_cursor = input.selectionStart;
   var new_cursor = input.selectionStart + s.length;
   var old_value = input.value;
   input.value = old_value.substring(0, old_cursor) + s + old_value.substring(old_cursor);
   input.selectionStart = input.selectionEnd = new_cursor;
   input.focus();
}

var width;
function setup () {
   $('#search').submit(onSubmit);
   //$('#searchBox').html(width/$(document).width());
   width = $('#options').width();
   $('#search').css('width', width+'px');
}

$(document).ready(setup);
