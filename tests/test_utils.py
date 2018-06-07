from ..utils import ungarde

def test_ungarde():
   assert [ungarde(i) for i in [
   "do̍bar", "dā̍n", "noga̍", "ljū̍di", "ljūdī̍",
   "асимилӣ̍ра̄м", "адвокатӣра̍о", "ха!ло̄̍", "зафр̥!ка̍нт"]] == [
   "dȍbar", "dȃn", "nòga", "ljȗdi", "ljúdī",
   "асимѝлӣра̄м", "адвокати́рао", "хало̑", "зафр̥ка̏нт"]
