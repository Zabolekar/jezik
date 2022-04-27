from . import characters as c

all_vowels = "АаЕеИиОоУуӤӥŒœꙒꙓѢѣAaEeIiOoUu°" + c.ring
any_vowel = f"[{all_vowels}]"
four_accents = f"{c.grave}{c.acute}{c.circumflex}{c.doublegrave}"
any_of_four_accents = f"[{four_accents}]"

plain_accents = '`´¨^_'

real_accent = {
    '`': c.grave, '´': c.acute, '¨': c.doublegrave,
    '^': c.circumflex, '_': c.macron, '°': c.ring,
    '!': c.excl
}
all_latin = "abcčćdđefghijklmnoprsštuvzžABCČĆDĐEFGHIJKLMNOPRSŠTUVZŽ"

roman = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII')
