function displayResults (reply) {
   $('#results').html(reply);
   ungardeAll();
   var width = $('#word').width() + $('#button').width(); //TODO: issue #14
   $('table').css('width', width+'px');
}

function onSubmit (event) {
   var word = $('#word').val();
   if (word) {
      var c = containsConfusingCharacters(word);
      console.log(c);
      if (c) {
         console.log("ooo");
         $('#results').html("<div id=\"fourhundredfour\">" +
                            "Ваш упит садржи знак " + c +
                            ", такве речи не постоје.</div>");
      } else {
         console.log("uuu");
         var url = $SCRIPT_ROOT + "lookup/" + word;
         $.ajax(url).done(displayResults);
      }
   }
   event.preventDefault();
}

function setup () {
   $('#search').submit(onSubmit);
   $('#ungarde').change(function () {
      $("#results table td#traditional")[this.checked ? "show" : "hide"]();
   });
}

$(document).ready(setup);

/* 
   Some characters have special meaning in URLs. Queries that contain such
   characters might confuse our site if sent via the search bar. It won't
   enable the user to do anything dangerous, but it might look weird. Luckily
   for us, words don't contain characters like that anyway.
*/
function containsConfusingCharacters (word) {
   prohibited = ["/","?","=","&",";","#","[","]","+",".",":","@"];
   var c;
   for(var i = 0; i < prohibited.length; i++) {
      c = prohibited[i];
      if (word.indexOf(c) != -1) {
         return c;
      }
   }
   return "";
}

function isVowel (c) {
   return "aeiouAEIOUаеиоуАЕИОУ\u0325".search(c) != -1;
}

function paste (array, idx, elem) {
   array.splice(idx, 0, elem);
}

function cut (array, idx) {
   array.splice(idx, 1);
}

function ungarde (word) {
   var chars = word.split(""),
       oldAccentIndex = chars.length - 1;
   while (oldAccentIndex >= 0) {
      if (chars[oldAccentIndex] == "\u030d") {
         break;
      }
      oldAccentIndex--;
   }
   cut(chars, oldAccentIndex)

   var newAccentIndex = oldAccentIndex - 1,
       vowelCount = 0,
       shifted = false;
   while (newAccentIndex >= 0) {
      if (chars[newAccentIndex] == "!") {
         cut(chars, newAccentIndex);
         oldAccentIndex--;
         break;
      }
      if (isVowel(chars[newAccentIndex])) {
         vowelCount++;
         if (vowelCount == 2) {
            shifted = true;
            newAccentIndex++;
            break;
         }
      }
      newAccentIndex--;
   }
   if (shifted) {
      paste(chars, newAccentIndex, "\u0300"); //rising
   } else {
      paste(chars, oldAccentIndex, "\u030f"); //falling
   }
      
   return chars.join("")
               .replace("\u0300\u0304", "\u0301")  //long rising
               .replace("\u0304\u030f", "\u0311"); //long falling   
}

/* test:
["do̍bar", "dā̍n", "noga̍", "ljū̍di", "ljūdī̍", "асимилӣ̍ра̄м", "адвокатӣра̍о", "ха!ло̄̍", "зафр̥!ка̍нт"].map(ungarde)
["dȍbar", "dȃn", "nòga", "ljȗdi", "ljúdī", "асимѝлӣра̄м", "адвокати́рао", "хало̑", "зафр̥ка̏нт"]
*/

function ungardeAll () {
   var traditional = $("#results table td#garde");
   $("#results table td#traditional").each(function (i, word) {
      word.innerText = ungarde(traditional[i].innerText);
   });
   $('#ungarde').change();
}
