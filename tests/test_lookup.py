from ..lookup import lookup

def test_lookup_drven_1():
   assert lookup("дрвен")["m sg nom long"][0].multiform == ['др̥̏венӣ']

def test_lookup_drven_2():
   assert lookup("дрвен")["m sg dat long"][1].multiform == ['др̥вѐно̄м', 'др̥вѐно̄ме', 'др̥вѐно̄му']

def test_lookup_gvozden_1():
   assert lookup("гвозден")["m pl ins long"][0].multiform == ['гво̏зденӣм', 'гво̏зденӣма']

def test_lookup_gvozden_2():
   assert lookup("гвозден")["m sg gen long"][1].multiform == ['гво̀здено̄г', 'гво̀здено̄га']

def test_lookup_gvozden_3():
   assert lookup("гвозден")["m sg loc long"][2].multiform == ['гвоздѐно̄м', 'гвоздѐно̄ме', 'гвоздѐно̄му']

def test_lookup_magarciti_1():
   assert [a[1] for a in lookup("магарчити се")["aor sg"][0]._data] == [["ма̀га̄рчих се"], ["ма̏га̄рчӣ се"], ["ма̏га̄рчӣ се"]]

def test_lookup_magarciti_2():
   assert [a[1] for a in lookup("магарчити се")["pf f sg"][1]._data] == [["мага́рчила се"]]