from ...lookup import lookup


def test_input_and_output_yat_modes():
   result = lookup("свет", input_yat="e", output_yat="e")
   assert len(result) == 3
   assert result[0]["m sg nom long"].multiform == ["све̑тӣ"]
   assert result[1]["m sg nom long"].multiform == ["свѐтӣ"]
   assert result[2]["sg nom"].multiform == ["све̑т"]

   result = lookup("свет", input_yat="e", output_yat="je")
   assert len(result) == 3
   assert result[0]["m sg nom long"].multiform == ["све̑тӣ"]
   assert result[1]["m sg nom long"].multiform == ["свѐтӣ"]
   assert result[2]["sg nom"].multiform == ["свйје̑т"]

   result = lookup("свет", input_yat="je", output_yat="e")
   assert len(result) == 2
   assert result[0]["m sg nom long"].multiform == ["све̑тӣ"]
   assert result[1]["m sg nom long"].multiform == ["свѐтӣ"]

   result = lookup("свет", input_yat="je", output_yat="je")
   assert len(result) == 2
   assert result[0]["m sg nom long"].multiform == ["све̑тӣ"]
   assert result[1]["m sg nom long"].multiform == ["свѐтӣ"]

   assert not lookup("свијет", input_yat="e", output_yat="e")
   result = lookup("свијет", input_yat="e", output_yat="ije")
   assert not result

   result = lookup("свијет", input_yat="je", output_yat="e")
   assert len(result) == 1
   assert result[0]["sg nom"].multiform == ["све̑т"]

   result = lookup("свијет", input_yat="je", output_yat="je")
   assert len(result) == 1
   assert result[0]["sg nom"].multiform == ["свйје̑т"]

   result = lookup("свијет", input_yat="ije", output_yat="ije")
   assert result["sg nom"].multiform == ["сви̏јет"]

   result = lookup("белег", input_yat="e", output_yat="ije")
   assert result["sg nom"].multiform == ["бѝљег"]

   result = lookup("вијенац", input_yat="ije", output_yat="e")
   assert result["pl gen"].multiform == ["ве̑на̄ца̄", "ве́на̄ца̄"]


def test_yat_mode_for_ambiguous_forms():
   assert lookup("реч", input_yat="e", output_yat="ije")["sg nom"].multiform == ["ри̏јеч"]
   assert lookup("повијест", input_yat="ije", output_yat="e")["pl gen"].multiform == ["по̏ве̄стӣ"]


def test_yat_mode_changes_the_exposed_form_not_the_lookup_result():
   assert lookup("снијег", input_yat="ije")["sg nom"].multiform == ["сни̏јег"]
   result = lookup("снијег", input_yat="ije", output_yat="je")
   assert result["sg nom"].multiform == ["снйје̑г"]
   assert result["pl nom"].multiform == ["сње̏гови", "снйје̑зи"]
   assert lookup("вијек", input_yat="ije")["sg nom"].multiform == ["ви̏јек"]
   assert lookup("вијек", input_yat="ije", output_yat="je")["sg nom"].multiform == ["вйје̑к"]
