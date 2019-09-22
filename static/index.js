function displayResults (reply) {
   $('#results').html($(reply));
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

function insertString (s) {
   var input = document.getElementById("word"),
       backup = { start: input.selectionStart, end: input.selectionEnd };
   
   input.value = input.value.substring(0, backup.start) + 
                  s + input.value.substring(backup.start);
   input.selectionStart = backup.start + s.length;
   input.selectionEnd = backup.end + s.length;
   input.focus();
}

var width;
function setup () {
   $('#search').submit(onSubmit);
   $('#options :button').click(function () {
      insertString(this.value);
   });
   width = $('#main').width();
   $('#header').css('width', width+'px');
   $('#search').css('width', width+'px');
}

$(document).ready(setup);
