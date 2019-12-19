# YAML structure

## Noun example

```
човѣк\људи:
 t: N\m
 i: бошњ.\1¨\a.\an;срп.\1`\a.\an;хрв.\1`\b.\an
 except:
  pl nom: љу^ди
  pl acc: љу^де
  pl gen: љу´ди_
  pl dat: љу´дима
  pl ins: љу´дима
  pl loc: љу´дима
  pl voc: љу^ди
```

Headline (mandatory): ```човѣк\људи:```

First, the lemma without accents: ```човѣк```.
Optional, after backslash: other forms to search by, without accents.

**t** (type/kind) field (mandatory): basic word info pieces divided by backslashes. Here we se **N** (noun) and **m** (masculine).

**i** (info) field (mandatory): info about its APs and other stuff. May contain multiple variants divided by **;**.
Here we see three variants divided by two semicolons, so we get three possible descriptions for the same word:

```бошњ.\1¨\a.\an
срп.\1`\a.\an
хрв.\1`\b.\an
```

It consists of four parts divided by backslashes.
First, a comment (may be empty). Here the comment say that the first variant is Bosnian, the second one is Serbian, the third one is Croatian.
Second, the accents: syllable's number and the accent over it. Multiple accent marks are divided by a comma, e.g. ```1¨,2_,3_,4_```.
Third, the AP. See the NOUN_PARADIGMS.md file. A paradigm name usually consists of two symbols: a Latin letter (e.g., **a** means the accent remains (almost) static on the stem), and a mark denoting length and other peculiarities (here, **.** means the stem contains short vowels only).
Fourth, other pieces of info divided by commas. **an** means **animate**, **+** means mandatory -ov- suffix in plural, **±** means optional -ov- suffix in plural, the possible list of marks may be extended.

**except** and/or **add** field (optional) shows us the word's irregular forms.

All these forms may contain yats, yers and other sofisticatedly treated symbols. See full list in NOTATION.md.


## Verb example

```нꙓкати:
 t: V\Tr\Ipf
 i: \1´\p:\delta;\1´\k:\beta
 c: само јекавски

 изузети:
 t: V\Refl\Pf\изузм
 i: \2`,3_\i:\kappa2
 
 адвокатирати:
 t: V\Itr\Ipf
 i: \4´\k:\beta
 v: адвокатисати
 ```

Actually, pretty much the same. BTW I forgot to mention that we also have an optional **c** (comment) field and an optional **v** (view) field. The comment field is for comments which concern the whole word, not one of its specific variants. The view field means: you may view some other word in this dictionary, which somehow relates to the current word. 

The **t** field of a verb contains 3 of 4 subfields. **V** means Verb. **Tr/Itr/Refl** shows its transitivity and/or reflexivity. (Why do we need that? Well, for example, intransitive verbs do not have a past participle in this language.) **Pf/Ipf/Dv** shows its aspectuality: perfect, imperfect, biaspectual. The fourth field (and the third backslash) is optional. It means: the verb has a second trunk, different enough to me mentioned here. Here, we got *izuze-ti* and *izuzm-em*.

The **i** field contains one or multiple declension variants, again divided by semicolons.
A variant contains four subfields.
First, a comment.
Second, the accents.
Third, the AP.
Fourth, the MP (set of verbal endings, like *-im -iš* or *-em -eš* or *-am -aš* or whatever).

## Adjective example

```адвокатски:
 t: A\ski
 i: \2`,3_,4_\0,a:\
 
 лꙓн:
 t: A\all
 i: \1^\b:,b:\
 v: лењ
 ```

The **t** field contains 2 subfields. First, **A**, which means "Adjective". Then, **ski/ov/all** which means its set of possible forms.
The ski-type adjectives have only long forms, like *advokatski*.
The all-type adjectives have short and long forms, like *dobar*.
The ov-type adjevtives have a mixed paradigms: sometimes a short form is preferred (*bratov*), sometimes a long one (*bratovog*), sometimes they come together.

The **i** field has four fields again.
First, the comment (here it is empty).
Second, the accents.
Third, the TWO accent paradigms, for the short subparadigm and for the long subparadigm. *Advokatski* does not possess short forms, so we write **0** for its short subparadigm.
Fourth, the space for other marks. Not used so far. The YAML format does not allow a colon (**:**) to end a line, so we always put a backslash at the end of an **i** field.
