from ....lookup.utils.expose import expose_replacement

def test_expose_replacement_preserves_long_yat_before_traditional_accent():
   form = "звꙓ´ри_"

   assert expose_replacement(form, "e") == "зве́рӣ"
   assert expose_replacement(form, "je") == "звйје́рӣ"
   assert expose_replacement(form, "ije") == "звијѐрӣ"
