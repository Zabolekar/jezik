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
["do̍bar", "dā̍n", "noga̍", "ljū̍di", "ljūdī̍", "асимилӣ̍ра̄м", "адвокатӣра̍о", "ха!ло̄̍", "зафр̥!ка̍нт"].map(function (word) {
   return ungarde(word);
})
["dȍbar", "dȃn", "nòga", "ljȗdi", "ljúdī", "асимѝлӣра̄м", "адвокати́рао", "хало̑", "зафр̥ка̏нт"]
*/

function ungardeAllInPlace () {
   $("#results table tr").each(function (i, word) {
      word.innerText = ungarde(word.innerText); //TODO backup and restoring
   });
}