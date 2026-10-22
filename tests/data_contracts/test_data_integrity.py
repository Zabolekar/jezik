import re
import pytest # type: ignore
from ...lookup import lookup, data
from ...lookup.charutils import c, four_accents, roman
from ...lookup.paradigm_helpers import cut_AP, has, str_find
from ...lookup.table import LabeledMultiform


first_form = {
   "adjective": "m sg nom", # short or long, we take the 0st one
   "noun": "sg nom",
   "verb": "infinitive",
   "adverb": ""
}


@pytest.mark.slow
def test_no_exceptions():
   """
   Iterate over entries in the database.
   Ensure that their lookup doesn't raise an exception.
   """
   bad_multiforms : list[LabeledMultiform] = []
   for outer_key, yat_mode in data._outer_to_inner:
      try:
         multitable = lookup(outer_key, input_yat=yat_mode)
         if any(not table.pos for table in multitable):
            raise ValueError("invalid part of speech")
      except Exception:
         print(outer_key, yat_mode)
         raise
      else:
         for table in multitable._tables:
            try:
               main_form = list(table[first_form[table.pos]])[0][1][0]
            except Exception:
               print(outer_key)
               raise
            first_acc_main = min(str_find(main_form, x) for x in four_accents)
            last_acc_main = max(main_form.rfind(x) for x in four_accents)
            compound = last_acc_main == first_acc_main > str_find(main_form, c.macron)
            for labeled_multiform in table:
               for form in labeled_multiform[1]:
                  if any(form.startswith(x) for x in four_accents + c.macron):
                     bad_multiforms.append(labeled_multiform)
                  if not compound: # eg not plāvosȋv
                     first_acc = min(str_find(form, x) for x in four_accents)
                     last_acc = max(form.rfind(x) for x in four_accents)
                     if last_acc == first_acc > str_find(form, c.macron): # eg ōvánā
                        bad_multiforms.append(labeled_multiform)
   if bad_multiforms:
      print(bad_multiforms)
      raise ValueError("impossible accentuation")


# internal notation that must never reach the user;
# NB: 'й' is intentionally present in 'je' output (e.g. свйје̑т)
_leaked_marker = re.compile(r"[·ø<>ʲʟʌъꚜꙏЪœʹʺ¦ȷĵˌ~!•°\d,(]|ꙓ|ѣ|  ")


@pytest.mark.slow
def test_every_output_mode_gives_clean_nonempty_forms():
   """
   Iterate over all outer keys (Cyrillic and Latin) and all output yat modes.
   Ensure that no form is empty and no internal notation leaks into forms.
   """
   problems: list[tuple[str, str, str, str]] = []
   for outer_key, input_yat in data._outer_to_inner:
      output_yats = [input_yat, "je"] if input_yat == "ije" else [input_yat]
      for output_yat in output_yats:
         for table in lookup(outer_key, input_yat, output_yat):
            if not table.pos:
               continue # accents not found message
            for label, forms in table:
               if not forms:
                  problems.append((outer_key, output_yat, label, "<empty>"))
               for form in forms:
                  if not form.strip() or _leaked_marker.search(form):
                     problems.append((outer_key, output_yat, label, form))
   assert not problems, problems[:20]


def test_paradigms():
   """Ensure that accent paradigms are desribed well"""
   for outer_key, _ in data._outer_to_inner:
      for inner_key, word in data[outer_key, 'e']:
         paradigms = [cut_AP(x) for x in word.info.split(";")]
         for paradigm in paradigms:
            assert isinstance(paradigm, str), paradigm + " " + inner_key
            assert not has(paradigm, *tuple("АВСКМНабвгдеёжзийклмнопрстуфхцчшщъыьэюяљњјџћђ"))
            if len(paradigm) in (2, 3):
               assert paradigm[0].isalpha() and paradigm[1] in ".:!ʹʺ’¿¡?0", paradigm+" "+inner_key
            elif len(paradigm) == 1:
               assert paradigm == '0', paradigm+" "+inner_key
            elif len(paradigm) > 0:
               raise ValueError(f"bad paradigm len: {paradigm} {inner_key}")

def test_yaml_suffixes():
   """
   Ensure that every ambiguous word has a suffix
   and that the suffixes are Roman numerals only.
   Also good for finding possible duplicates.
   """
   for outer_key, yat_mode in data._outer_to_inner:
      myentries = list(data[(outer_key.lower(), yat_mode)])
      if len(myentries) > 1:
         for _, entry in myentries:
            cpt = entry.caption[0]
            assert ':' in cpt, [x[1].accented_keys for x in myentries]
            assert cpt[:cpt.find(':')] in roman, cpt+" "+entry.accented_keys
