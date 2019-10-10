cring = "\u0325"
cmacron = "\u0304"
cstraight = "\u030d"
cacute = "\u0301"
cgrave = "\u0300"
cdoublegrave = "\u030f"
ccircumflex = "\u0311"
cbreve = "\u0306"
all_vowels = f"АаЕеИиОоУуӤӥŒœꙒꙓѢѣAaEeIiOoUu{cring}"
any_vowel = f"[{all_vowels}]"
any_of_four_accents = f"[{cgrave}{cacute}{ccircumflex}{cdoublegrave}]"
all_accent_marks = [
    cring, cmacron, cstraight,
    cacute, cgrave, cdoublegrave,
    ccircumflex, cbreve, '!'
    ]
real_accent = {
    '`': cgrave, '´': cacute, '¨': cdoublegrave,
    '^': ccircumflex, '_': cmacron, '!': '!'
    }
