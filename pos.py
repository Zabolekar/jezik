from typing import Any, Dict, List
from .paradigm_helpers import AccentedTuple, GramInfo, nice_name, oa
from .utils import swap_length, first_vowel_index, last_vowel_index, insert

class PartOfSpeech():
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      self.key = key 
      self.value = value 
      i, t = self.value['i'].split(';'), self.value['t'] 
      self.info = GramInfo(i, t) 

   def _swap(self, trunk_: str, length_inconstant: bool, AP: str, target_AP: str) -> str:
      # at first we process words like boos ~ bosa
      if length_inconstant and AP == target_AP:
         word_form = swap_length(trunk_, AP)
      # this part is about words where length is the same in most forms:
      else:
         word_form = trunk_
      return word_form

   def _append_morpheme(self, i: int, word_form: str, ending_part: AccentedTuple) -> str:
      # if this ending_part should be accented in this AP,
      # then first we delete the now unnecessary accent in the stem in case it is there;
      # second we put the accent into the ending_part,
      # the word hereby being accented;
      # and if it shouldn't, we just do nothing and leave it unaccented;
      # after that, we append the morpheme
      morpheme = ending_part.morpheme
      if morpheme.startswith('>'):
         word_form = word_form.replace('\u0304', '')
         morpheme = morpheme.replace('>', '')
      if morpheme.startswith('<'):
         lvi = last_vowel_index(word_form)
         if not '\u0304' in word_form[lvi:] and lvi is not None:
            word_form = insert(word_form, {lvi+1: '\u0304'})
            word_form = word_form.replace('\u0304·', '·\u0304')
            fvi = first_vowel_index(word_form)
            if lvi != fvi and '\u0304\u030d' in word_form[lvi:] \
                  and not '\u0304' in word_form[:lvi] :
               lvi2 = last_vowel_index(word_form[:lvi])               
               word_form = word_form.replace('\u030d', '')
               word_form = insert(word_form, {lvi2+1: '\u030d'})
         morpheme = morpheme.replace('<', '')
      if self.info.AP[i] in ending_part.accent:
         if self.info.AP[i] in oa:
            word_form = word_form.replace('\u030d', '') # straight
         if 'b' in self.info.AP[i] and '\u030d' in word_form and not '0' in morpheme:
            morpheme = morpheme.replace('·', '')
         #print('do: ', ending_part.morpheme)
         morpheme = morpheme.replace('·', '\u030d') # to straight
         #print('posle: ', morpheme)
      return word_form + morpheme

   def _unstick(self, s: str):
      return set([s[x:x+2] for x in range(0, len(s), 2)])

   def _reduce_doublets(self, endings_: List[List[AccentedTuple]], AP: str) -> List[List[AccentedTuple]]:
      # necessary in verbs and nouns;
      # not needed in adjectives.
      # it deletes endings identical in future
      ready_endings: List[Any] = []
      if len(endings_) > 1:
         for ending_ in endings_:
            addendum = True
            # next statement means: the AP is in every intersection of APs of an ending_ with another ending_
            # TODO: please make the code less sofisticated and more comprehensible
            ok = all([AP in self._unstick(x.accent).intersection(self._unstick(y.accent)) for x in ending_ for y in ending_])
            supr_ = ''.join([x.morpheme for x in ending_]).replace('·', '')
            for ending in ready_endings:
               supr = ''.join([d.morpheme for d in ending]).replace('·', '')
               accents_ = ''.join([z.accent for z in ending])
               if (AP not in accents_ or ok) and supr_ == supr:
                  addendum = False
            if addendum:   
               ready_endings.append(ending_)
      else:
         ready_endings = endings_
         
      return ready_endings