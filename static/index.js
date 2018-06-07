function displayResults (reply) {
   $('#results').html(reply);
   var width = $('#word').width() + $('#button').width(); //TODO: issue #14
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val();
   if (word) {
      var c = confusingCharacters(word);
      if (c) {
         $('#results').html("<div id=\"fourhundredfour\">" +
                            "Ваш упит садржи знак " + c +
                            ", такве речи не постоје.</div>");
      } else {
         var url = $SCRIPT_ROOT + "lookup/" + word;
         $.ajax(url).done(displayResults);
      }
   }
   event.preventDefault();
}

function setup () {
   $('#search').submit(onSubmit);
}

$(document).ready(setup);

/* 
   Some characters have special meaning in URLs. Queries that contain such
   characters might confuse our site if sent via the search bar. It won't
   enable the user to do anything dangerous, but it might look weird. Luckily
   for us, words don't contain characters like that anyway.
*/
function confusingCharacters (word) {
   prohibited = "/?=&;#[]+.:@".split("");
   var c;
   for(var i = 0; i < prohibited.length; i++) {
      c = prohibited[i];
      if (word.indexOf(c) != -1) {
         return c;
      }
   }
   return "";
}
