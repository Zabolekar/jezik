cring = "\u0325"
cmacron = "\u0304"
cstraight = "\u030d"
cacute = "\u0301"
cgrave = "\u0300"
cdoublegrave = "\u030f"
ccircumflex = "\u0311"
cbreve = "\u0306"
all_vowels = "АаЕеИиОоУуӤӥŒœꙒꙓѢѣAaEeIiOoUu°" + cring
any_vowel = f"[{all_vowels}]"
four_accents = f"{cgrave}{cacute}{ccircumflex}{cdoublegrave}"
any_of_four_accents = f"[{four_accents}]"
all_accent_marks = [
    cring, cmacron, cstraight,
    cacute, cgrave, cdoublegrave,
    ccircumflex, cbreve, '!'
]

plain_accents = '`´¨^_'


real_accent = {
    '`': cgrave, '´': cacute, '¨': cdoublegrave,
    '^': ccircumflex, '_': cmacron, '°': cring,
    '!': '!'
}
all_latin = "abcčćdđefghijklmnoprsštuvzžABCČĆDĐEFGHIJKLMNOPRSŠTUVZŽ"

roman = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII')
