import pytest # type: ignore
from ..lookup import lookup

def test_nonsense():
   assert not lookup("абырвалг")

def test_inner_notation():
   assert not lookup("абецедън")
   assert not lookup("свꙓтъʌ")

def test_ije():
   l = lookup("свет", input_yat="e", output_yat="e") # свет, свет
   assert len(l) == 3
   assert l[0].pos == "adjective"
   assert l[1].pos == "adjective"
   assert l[2].pos == "noun"
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l[2]["sg nom"].multiform == ['све̑т']

   l = lookup("свет", input_yat="e", output_yat="je") # свет, свијет
   assert len(l) == 3
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']
   assert l[2]["sg nom"].multiform == ['свйје̑т']

   l = lookup("свет", input_yat="je", output_yat="e") # свет (*svętъ)
   assert len(l) == 2
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свет", input_yat="je", output_yat="je") # свет (*svętъ)
   assert len(l) == 2
   assert l[0]["m sg nom long"].multiform == ['све̑тӣ']
   assert l[1]["m sg nom long"].multiform == ['свѐтӣ']

   l = lookup("свијет", input_yat="e", output_yat="e") # not found
   assert not l

   l = lookup("свијет", input_yat="e", output_yat="je") # not found
   assert not l

   l = lookup("свијет", input_yat="je", output_yat="e") # свет (*světъ)
   assert len(l) == 1
   assert l[0]["sg nom"].multiform == ['све̑т']

   l = lookup("свијет", input_yat="je", output_yat="je") # свијет
   assert len(l) == 1
   assert l[0]["sg nom"].multiform == ['свйје̑т']

   l = lookup("свијет", input_yat="ije", output_yat="ije")
   assert len(l) == 1
   assert l[0]["sg nom"].multiform == ['сви̏јет']

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

def test_gpl():
   assert lookup("језик")["pl gen"].multiform == ["је̏зӣка̄"]
   assert set(lookup("грош")["pl gen"].multiform) == set(["гро̏ше̄ва̄", "гро̀ше̄ва̄", "гро́ша̄"])
   assert set(lookup("бик")["pl gen"].multiform) == set(["би̏ко̄ва̄", "бѝко̄ва̄"])
   assert lookup("аманет")["pl gen"].multiform == ["а̀ма̄не̄та̄"]
   assert set(lookup("отац")["pl gen"].multiform) == set(["о̀че̄ва̄", "ота́ца̄"])
   assert lookup("Македонац")["pl gen"].multiform == ["Макѐдо̄на̄ца̄"]
   assert lookup("новац")["pl gen"].multiform == ["но̏ва̄ца̄"]
   assert lookup("пуж")["pl gen"].multiform == ["пу́же̄ва̄", "пу́жа̄"]
   # TODO: нѐпце : не̏ба̄ца̄ when neuter is ready

def test_snjegovi():
   l = lookup("снијег", input_yat="ije", output_yat="je")
   assert l["sg nom"].multiform == ['снйје̑г']
   assert l["pl nom"].multiform == ['сње̏гови', 'снйје̑зи']

def test_multiple_results():
   assert len(lookup("апсорбовати")) == 2
   assert len(lookup("зор")) == 2

def test_different_ije():

   la1 = lookup("снијег", input_yat="ije")
   la2 = lookup("снијег", input_yat="ije", output_yat="je")
   assert la1["sg nom"].multiform == ['сни̏јег']
   assert la2["sg nom"].multiform == ['снйје̑г']

   lb1 = lookup("вијек", input_yat="ije")
   lb2 = lookup("вијек", input_yat="ije", output_yat="je")
   assert lb1["sg nom"].multiform == ['ви̏јек']
   assert lb2["sg nom"].multiform == ['вйје̑к']

def test_advokatirati():
   """
   This test was added to cover issue #25
   """
   assert lookup("адвокатирати")["prs 1 sg"].multiform == ['адвока̀тӣра̄м']
   assert lookup("алудирати")["prs 1 sg"].multiform == ['алу̀дӣра̄м']
   assert lookup("ачити се")["prs 1 sg"].multiform == ['а̑чӣм се']

def test_lll():
   assert lookup("го")["nom sg m short"].multiform == ['го̑', 'го̑л']
   assert lookup("бо")["nom sg"].multiform == ['бо̑', 'бо̑л']

def test_abang_paradigm():
   assert lookup("агитатор")["gen sg"].multiform == ['агѝта̄тора']
   assert lookup("аманет")["gen sg"].multiform == ['ама́нета']
   assert lookup("анђео")["ins sg"].multiform == ['а̑нђелом']
   assert lookup("амбасадор")["pl nom"].multiform == ['амба̀са̄дори']

def test_krnjeme():
   a = lookup("крњ")["dat sg long m"].multiform
   assert all([not x.endswith("ме") for x in a])

def test_mo_mo():
   assert lookup("знати")["prs 1 pl"][0].multiform == ["зна́мо", "зна̑мо"]
   assert lookup("дознати")["prs 2 pl"].multiform == ["дозна́те", "до̀зна̄те"]

def test_latin():
   assert lookup("amanet")["gen pl"].multiform == ["àmānētā"]
   assert lookup("ačiti se")["prs 3 pl"].multiform == ["ȃčē se"]
   assert lookup("sudžuk")["acc pl"].multiform == ["sùdžuke"]

def test_hmeljem_hmeljom():
   assert set(lookup("хмељ")["ins sg"].multiform) == set(["хмѐљем", "хмѐљом"])

def test_boj_se():
   assert lookup("бојати се")["imv 2 sg"].multiform == ['бо̑ј се']
   assert lookup("дојити")["imv 2 sg"].multiform == ['до̑ј']

def test_vocative():
   assert lookup("јелен")["sg voc"].multiform == ["јѐлене"]
   assert lookup("јелен")["pl voc"].multiform == ["јѐлени"]
   assert lookup("орач")["sg voc"].multiform == ["о̏ра̄чу"]
   assert lookup("орач")["pl voc"].multiform == ["о̏ра̄чи"]
   assert lookup("пуж")["sg voc"].multiform == ["пу̑жу"]
   assert lookup("пуж")["pl voc"].multiform == ["пу́жеви", "пу̑жи"]
   assert lookup("град")["sg voc"].multiform == ["гра̑де"]
   assert lookup("град")["pl voc"].multiform == ["гра̏дови", "гра̑ди"]
