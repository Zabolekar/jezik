function onSubmit (event) {
   var word = document.getElementById("word").value,
       inputYat = document.querySelector("input[name=in]:checked").value,
       outputYat = document.querySelector("input[name=out]:checked").value;
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

function setup () {
   document.getElementById("search").addEventListener("submit", onSubmit);
   
   for (button of document.querySelectorAll("#options [type=button]")) {
      button.addEventListener("click", function () {
         insertString(this.value);
      });
   }
   
   var width = getComputedStyle(document.getElementById("main")).width;
   document.getElementById("header").style.width = width;
   document.getElementById("search").style.width = width;

   var url = new URL(location.href);
   var input = document.getElementById("word");

   var match = url.pathname.match("/lookup/(.*)");
   if (match) input.value = decodeURIComponent(match[1]);
   input.focus();

   var inputYat = url.searchParams.get("in") || "e";
   var outputYat = url.searchParams.get("out") || "e";
   document.querySelector("input[name=in][value='" + inputYat + "']").checked = true;
   document.querySelector("input[name=out][value='" + outputYat + "']").checked = true;
}

document.addEventListener("DOMContentLoaded", setup);
