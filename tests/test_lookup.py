import pytest
from ..lookup import lookup

def test_nonsense():
   assert not lookup("абырвалг")

def test_inner_notation():
   assert not lookup("абецедън")
   assert not lookup("свꙓтъʌ")

def test_ije():
   l = lookup("свет", input_yat="ekav", output_yat="ekav") # свет, свет
   assert len(l) == 3
   assert l[0].pos == "adjective"
   assert l[1].pos == "adjective"
   assert l[2].pos == "noun"
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l[2]["sg nom"].multiform == ['све̑т']

   l = lookup("свет", input_yat="ekav", output_yat="ijekav") # свет, свијет
   assert len(l) == 3
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l[2]["sg nom"].multiform == ['свйје̑т']

   l = lookup("свет", input_yat="ijekav", output_yat="ekav") # свет (*svętъ)
   assert len(l) == 2
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свет", input_yat="ijekav", output_yat="ijekav") # свет (*svętъ)
   assert len(l) == 2
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свијет", input_yat="ekav", output_yat="ekav") # not found
   assert not l

   l = lookup("свијет", input_yat="ekav", output_yat="ijekav") # not found
   assert not l

   l = lookup("свијет", input_yat="ijekav", output_yat="ekav") # свет (*světъ)
   assert len(l) == 1
   assert l[0]["sg nom"].multiform == ['све̑т']

   l = lookup("свијет", input_yat="ijekav", output_yat="ijekav") # свијет
   assert len(l) == 1
   assert l[0]["sg nom"].multiform == ['свйје̑т']

def test_drven():
   assert lookup("дрвен")["m sg nom long"][0].multiform == ['др̥̏венӣ']
   assert lookup("дрвен")["m sg dat long"][1].multiform == ['др̥вѐно̄м', 'др̥вѐно̄ме', 'др̥вѐно̄му']

def test_gvozden():
   assert lookup("гвозден")["m pl ins long"][0].multiform == ['гво̏зденӣм', 'гво̏зденӣма']
   assert lookup("гвозден")["m sg gen long"][1].multiform == ['гво̀здено̄г', 'гво̀здено̄га']
   assert lookup("гвозден")["m sg loc long"][2].multiform == ['гвоздѐно̄м', 'гвоздѐно̄ме', 'гвоздѐно̄му']

def test_magarciti():
   assert [a for _, [a] in lookup("магарчити се")["aor sg"][0]] == ["ма̀га̄рчих се", "ма̏га̄рчӣ се", "ма̏га̄рчӣ се"]
   assert [a for _, [a] in lookup("магарчити се")["pf f sg"][1]] == ["мага́рчила се"]

@pytest.mark.xfail
def test_dub():
   assert [a for _, a in lookup("дуб")["ins pl"]] == [["дубо̀вима", "ду̏бовима", "ду́бима", "ду̑бима"]]
   assert [a for _, a in lookup("дуб")["gen pl"]] == [["дубо́ва̄", "ду̏бо̄ва̄", "ду́ба̄"]]

def test_srp():
   assert lookup("срп")["pl gen"].multiform == ['ср̥по́ва̄', 'ср̥̏по̄ва̄', 'ср̥́па̄']
   assert lookup("срп")["sg gen"].multiform == ['ср̥̑па']
   assert lookup("срп")["pl dat"].multiform == ['ср̥по̀вима', 'ср̥̏повима', 'ср̥́пима', 'ср̥̑пима']

def test_sluchaj():
   assert lookup("случај")["pl dat"].multiform == ['случајѐвима', 'слу̏чајевима', 'случа́јима', 'слу̏ча̄јима']

def test_apB():
   assert [a for _, [a] in lookup("пиљак")["gen"]] == ["пи́љка", "пи̑ља̄ка̄"]
   assert lookup("грош")["pl gen"].multiform == ["гро̏ше̄ва̄", "гро̀ше̄ва̄", "гро́ша̄"]
   assert [a for _, [a] in lookup("аминаш")["nom"]] == ["амѝна̄ш", "амина́ши"]

def test_neocirk():
   assert lookup("језик")["pl gen"].multiform == ["је̏зӣка̄"]
   # TODO: нѐпце : не̏ба̄ца̄ when neuter is ready?

def test_snjegovi():
   l = lookup("снијег", input_yat="ijekav", output_yat="jekav")
   assert l["sg nom"].multiform == ['снйје̑г']
   assert l["pl nom"].multiform == ['сње̏гови', 'снйје̑зи']

@pytest.mark.xfail
def test_multiple_results():
   assert len(lookup("апсорбовати")) == 2
   assert len(lookup("зор")) == 2

@pytest.mark.xfail
def test_different_ije():
 
   la1 = lookup("снијег", input_yat="ijekav")
   la2 = lookup("снијег", input_yat="ijekav", output_yat="jekav")
   assert la1["sg nom"].multiform == ['сни̏јег']
   assert la2["sg nom"].multiform == ['снйје̑г']

   lb1 = lookup("вијек", input_yat="ijekav")
   lb2 = lookup("вијек", input_yat="ijekav", output_yat="jekav")
   assert lb1["sg nom"].multiform == ['ви̏јек']
   assert lb2["sg nom"].multiform == ['вйје̑к']

   # TODO: йје́ vs ијѐ

@pytest.mark.xfail
def test_advokatirati():
   """
   This test was added to cover issue #25
   """
   assert lookup("адвокатирати")["prs 1 sg"].multiform == ['адвока̀тӣра̄м']
   assert lookup("алудирати")["prs 1 sg"].multiform == ['алу̀дӣра̄м']
   assert lookup("ачити се")["prs 1 sg"].multiform == ['а̑чӣм се']
