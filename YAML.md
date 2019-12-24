# YAML structure

## Noun example

```
чо¨вѣк,чо`вѣк,чо`вѣк\љу^ди:
 t: N\m
 i: бошњ.\a.\an;срп.\a.\an;хрв.\b.\an
 except:
  pl nom: љу^ди
  pl acc: љу^де
  pl gen: љу´ди_
  pl dat: љу´дима
  pl ins: љу´дима
  pl loc: љу´дима
  pl voc: љу^ди
```

Headline (mandatory): ```чо¨вѣк,чо`вѣк,чо`вѣк\љу^ди```

First, the lemma with accents, as many times as many different tables there are.

Optional, after backslash: other forms to search by, without accents.

**t** (type/kind) field (mandatory): basic word info pieces divided by backslashes. Here we see **N** (noun) and **m** (masculine).

**i** (info) field (mandatory): info about its APs and other stuff. May contain multiple variants (the same quantity as in the headline) divided by **;**.

In this example we see three variants divided by two semicolons, so we get three possible descriptions (and subsequently declension tables) for the same word:

```
бошњ.\a.\an
срп.\a.\an
хрв.\b.\an
```

It consists of three parts divided by backslashes.

First, a comment (may be empty). Here the comment say that the first variant is Bosnian, the second one is Serbian, the third one is Croatian.

Second, the AP. See the NOUN_PARADIGMS.md file. A paradigm name usually consists of two symbols: a Latin letter (e.g., **a** means the accent remains (almost) static on the stem), and a mark denoting length and other peculiarities (here, **.** means the stem contains short vowels only).

Third, other pieces of info divided by commas. **an** means **animate**, **+** means mandatory -ov- suffix in plural, **±** means optional -ov- suffix in plural, the possible list of marks may be extended.

**except** and/or **add** field (both optional) shows us the word's irregular forms.

All these forms may contain yats, yers and other sophisticatedly treated symbols. See full list in NOTATION.md.


## Verb examples

```
нꙓ´кати,нꙓ´кати:
 t: V\Tr\Ipf
 i: \p:\delta;\k:\beta
 c: само јекавски

изу`зе_ти:
 t: V\Refl\Pf\изузм
 i: \i:\kappa2
 
адвокати´рати:
 t: V\Itr\Ipf
 i: \k:\beta
 v: адвокатисати
 ```

Actually, pretty much the same. BTW I forgot to mention that we also have an optional **c** (comment) field and an optional **v** (view) field. The comment field is for comments which concern the whole word, not one of its specific variants. The view field means: you may view some other word in this dictionary, which somehow relates to the current word. 

The **t** field of a verb contains 3 or 4 subfields. **V** means Verb. **Tr** or **Itr** or **Refl** shows its transitivity and/or reflexivity. (Why do we need that? Well, for example, intransitive verbs do not have a past participle in this language.) **Pf** or **Ipf** or **Dv** shows its aspectuality: perfect, imperfect, biaspectual. The fourth field (and the third backslash) is optional. It means: the verb has a second trunk, different enough to me mentioned here. Here, we got *izuze-ti* and *izuzm-em*.

The **i** field contains one or multiple declension variants, again divided by semicolons.

A variant contains three subfields.

First, a comment.

Second, the AP.

Third, the MP (set of verbal endings, like *-im -iš* or *-em -eš* or *-am -aš* or whatever).

## Adjective examples

```
адво`ка_тски_:
 t: A\ski
 i: \0,a:\
 
лꙓ^н:
 t: A\all
 i: \b:,b:\
 v: лењ
 ```

The **t** field contains 2 subfields. First, **A**, which means "Adjective". Then, **ski** or **ov** or **all** which means its set of possible forms.

The ski-type adjectives have only long forms, like *advokatski*.

The all-type adjectives have short and long forms, like *dobar*.

The ov-type adjectives have a mixed paradigm: sometimes a short form is preferred (*bratov*), sometimes a long one (*bratovog*), sometimes they come together.

The **i** field has three fields again.

First, the comment (here it is empty).

Second, the TWO accent paradigms, for the short subparadigm and for the long subparadigm. *Advokatski* does not possess short forms, so we write **0** for its short subparadigm.

Third, the space for other marks. Not used so far. The YAML format does not allow a colon (**:**) to end a line, so we always put a backslash at the end of an **i** field.
