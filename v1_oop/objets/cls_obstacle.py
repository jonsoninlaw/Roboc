class Obstacle:

	def __init__(self, symbole):

		self.type = symbole
		self.passage = self._verif_passage(symbole)
		self.victoire = self._verif_victoire(symbole)

	def _verif_passage(self, symbole):

		if symbole == "O":
			passage = False
		else:
			passage = True
		return passage

	def _verif_victoire(self, symbole):

		if symbole == "U":
			victoire = True
		else:
			victoire = False
		return victoire