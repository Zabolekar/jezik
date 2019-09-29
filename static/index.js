function displayResults (reply) {
   $('#results').html($(reply).filter("#tables-or-not-found"));
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val(),
       inputYat = $('input[name=in]:checked').val(),
       outputYat = $('input[name=out]:checked').val();
   if (word) {
      var url = $SCRIPT_ROOT + "/lookup/" +
                encodeURIComponent(word) +
                "?in=" + inputYat +
                "&out=" + outputYat;
      location.href = url;
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

   var url = new URL(location.href);
   var inputYat = url.searchParams.get("in") || "e";
   var outputYat = url.searchParams.get("out") || "e";
   $('input[name=in]').val([inputYat]);
   $('input[name=out]').val([outputYat]);
}

$(document).ready(setup);
