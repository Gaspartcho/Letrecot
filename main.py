from copy import deepcopy
from numpy import array, ndarray

from typing import Tuple

class Letrecot:
	"""Letrecot Class: everyting about the game will happend here."""

	# In general, "X" will be 1 (True) and "O" will eb 0 (False)

	board = [[" ", "X", " ", "X", " "],
			 [" ", " ", "O", " ", " "],
			 [" ", " ", " ", " ", " "],
			 [" ", " ", "X", " ", " "],
			 [" ", "O", " ", "O", " "]]

	turn = "X"
	fliped = False
	nb_turn = 0
	selection = array([0, 0])



	def __init__(self) -> None:
		self.board = deepcopy(Letrecot.board)

		return


	def lookup_coo(self, coo: ndarray) -> str:
		"""
		Returns the value of the cell at the coordinate coo. \n
		Returns '' if the coordinates are out os scope.
		"""
		if not coo[0] in range(5) or not coo[1] in range(5):
			return ""

		return self.board[coo[0]][coo[1]]

	def set_coo(self, coo: ndarray, content: str) -> bool:
		"""
		Sets the board at the coorinates 'coo' the value 'content'. \n
		Returns True if everything went well. \n
		Returns False if an the coo where invalid (nothing will be changed).
		"""

		if self.lookup_coo(coo) == "":
			return False

		self.board[coo[0]][coo[1]] = content

		return True


	def display_board(self, reversed: bool = False, removes_before: bool = False, include_select: bool = False) -> None:
		"""Prints the board in the shell for user interaction."""

		return


	def get_board_hashable(self) -> str:
		"""Returns the board as a unique hashable value (string)"""

		counter = 0
		result = ""

		for row in self.board:
			for cell in row:
				if cell == " ":
					counter += 1
				else:
					result += " ".join((str(counter), cell, ""))
					counter = 0

		return result


	def predict_move_piece(self, coo: ndarray, dire: ndarray) -> ndarray:
		"""
		Returns the expected position of the piece at coordinates 'coo'
		if it where to be moven.
		"""

		n_coo = array(coo, copy=True)

		while self.lookup_coo(n_coo + dire) == " ":
			n_coo += dire

		return n_coo


	def move_piece(self, coo: ndarray, dire: ndarray) -> None:
		"""Moves a piece from the coordinates in a choosen direction."""

		piece_type = self.lookup_coo(coo)
		final_coo = self.predict_move_piece(coo, dire)

		self.set_coo(coo, " ")
		self.set_coo(final_coo, piece_type)
		
		return


test = Letrecot()

