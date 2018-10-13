from ..lookup import lookup

def test_nonsense():
   assert not lookup("абырвалг")._tables

def test_inner_notation():
   assert not lookup("абецедън")._tables
   assert not lookup("свꙓтъʌ")._tables

def test_ije():
   l = lookup("свет", input_yat="ekav", output_yat="ekav") # свет, свет
   assert len(l._tables) == 3
   assert l._tables[0].pos == "adjective"
   assert l._tables[1].pos == "adjective"
   assert l._tables[2].pos == "noun"
   assert l._tables[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l._tables[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l._tables[2]["sg nom"].multiform == ['све̑т']

   l = lookup("свет", input_yat="ekav", output_yat="ijekav") # свет, свијет
   assert len(l._tables) == 3
   assert l._tables[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l._tables[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l._tables[2]["sg nom"].multiform == ['свйје̑т']

   l = lookup("свет", input_yat="ijekav", output_yat="ekav") # свет (*svętъ)
   assert len(l._tables) == 2
   assert l._tables[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l._tables[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свет", input_yat="ijekav", output_yat="ijekav") # свет (*svętъ)
   assert len(l._tables) == 2
   assert l._tables[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l._tables[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свијет", input_yat="ekav", output_yat="ekav") # not found
   assert len(l._tables) == 0

   l = lookup("свијет", input_yat="ekav", output_yat="ijekav") # not found
   assert len(l._tables) == 0

   l = lookup("свијет", input_yat="ijekav", output_yat="ekav") # свет (*světъ)
   assert len(l._tables) == 1
   assert l._tables[0]["sg nom"].multiform == ['све̑т']

   l = lookup("свијет", input_yat="ijekav", output_yat="ijekav") # свијет
   assert len(l._tables) == 1
   assert l._tables[0]["sg nom"].multiform == ['свйје̑т']

def test_drven():
   assert lookup("дрвен")["m sg nom long"][0].multiform == ['др̥̏венӣ']
   assert lookup("дрвен")["m sg dat long"][1].multiform == ['др̥вѐно̄м', 'др̥вѐно̄ме', 'др̥вѐно̄му']

def test_gvozden():
   assert lookup("гвозден")["m pl ins long"][0].multiform == ['гво̏зденӣм', 'гво̏зденӣма']
   assert lookup("гвозден")["m sg gen long"][1].multiform == ['гво̀здено̄г', 'гво̀здено̄га']
   assert lookup("гвозден")["m sg loc long"][2].multiform == ['гвоздѐно̄м', 'гвоздѐно̄ме', 'гвоздѐно̄му']

def test_magarciti():
   assert [a[1] for a in lookup("магарчити се")["aor sg"][0]._data] == [["ма̀га̄рчих се"], ["ма̏га̄рчӣ се"], ["ма̏га̄рчӣ се"]]
   assert [a[1] for a in lookup("магарчити се")["pf f sg"][1]._data] == [["мага́рчила се"]]

#def test_dub():
#   assert [a[1] for a in lookup("дуб")["ins pl"]._data] == [["дубо̀вима", "ду̏бовима", "ду́бима", "ду̑бима"]]
#   assert [a[1] for a in lookup("дуб")["gen pl"]._data] == [["дубо́ва̄", "ду̏бо̄ва̄", "ду́ба̄"]]

    