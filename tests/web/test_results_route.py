from ... import app


def test_filtered_lookup_keeps_the_normalized_input_word():
   client = app.test_client()

   response = client.get("/lookup/%20свет%20?par=missing")

   assert response.status_code == 200
   assert "Реч&nbsp;„свет”&nbsp;није" in response.get_data(as_text=True)
