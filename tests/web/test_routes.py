from unittest.mock import patch

from ... import app


def test_static_pages_favicon_and_not_found_are_served():
   client = app.test_client()

   assert client.get("/").status_code == 200
   assert client.get("/about").status_code == 200
   assert client.get("/favicon.ico").mimetype == "image/vnd.microsoft.icon"
   assert client.get("/missing").status_code == 404


def test_results_accepts_par_and_subpar_filters_together():
   response = app.test_client().get("/lookup/свет?par=missing&subpar=missing")

   assert response.status_code == 200
   assert "Реч&nbsp;„свет”&nbsp;није" in response.get_data(as_text=True)


def test_random_route_maps_jekavian_input_to_ijekavian_lookup_mode():
   with patch("jezik.random_key", return_value=("свијет", "je")):
      response = app.test_client().get("/random")

   assert response.status_code == 302
   assert response.location.endswith("/lookup/%D1%81%D0%B2%D0%B8%D1%98%D0%B5%D1%82?in=ije&out=je")


def test_random_route_preserves_other_yat_modes():
   with patch("jezik.random_key", return_value=("свет", "e")):
      response = app.test_client().get("/random")

   assert response.status_code == 302
   assert response.location.endswith("/lookup/%D1%81%D0%B2%D0%B5%D1%82?in=e&out=e")
