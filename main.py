
from copy import deepcopy
from numpy import array
from numpy._typing import NDArray
import click
import sys



class Letrecot:
	"""Letrecot Class: everyting about the game will happend here."""

	# In general, "X" will be 1 (True) and "O" will eb 0 (False)

	board = [[" ", "X", " ", "X", " "],
			 [" ", " ", "O", " ", " "],
			 [" ", " ", " ", " ", " "],
			 [" ", " ", "X", " ", " "],
			 [" ", "O", " ", "O", " "]]

	neighbords_cells = {"ul": array((-1, -1)),
						"u":  array((-1,  0)),
						"ur": array((-1,  1)),
						"l":  array(( 0, -1)),
						"r":  array(( 0,  1)),
						"dl": array(( 1, -1)),
						"d":  array(( 1,  0)),
						"dr": array(( 1,  1))}

	selection = array([0, 0])


	def __init__(self) -> None:
		self.board = deepcopy(Letrecot.board)

		return


	def lookup_coo(self, coo: NDArray) -> str:
		"""
		Returns the value of the cell at the coordinate coo. \n
		Returns "" if the coordinates are out os scope.
		"""
		if not coo[0] in range(5) or not coo[1] in range(5):
			return ""

		return self.board[coo[0]][coo[1]]


	def set_coo(self, coo: NDArray, content: str) -> bool:
		"""
		Sets the board at the coorinates 'coo' the value 'content'. \n
		Returns True if everything went well. \n
		Returns False if an the coo where invalid (nothing will be changed).
		"""

		if self.lookup_coo(coo) == "":
			return False

		self.board[coo[0]][coo[1]] = content

		return True


	def display_board(self, removes_before: int = 0, include_select: bool = False) -> None:
		"""Prints the board in the shell for user interaction."""

		if removes_before:
			nb_lines = str(12 + removes_before)
			sys.stdout.write("\x1B[" + nb_lines + "F")

		data = ["   | A | B | C | D | E |"]

		for i in range(5):
			data.append("---|---|---|---|---|---|")
			line = [f" {i + 1} "]
			for j in range(5):
				pos = array((i, j))
				if (pos == self.selection).all() and include_select:
					line.append(f"[{self.lookup_coo(pos)}]")
				else:
					line.append(f" {self.lookup_coo(pos)} ")
			line.append("")
			data.append("|".join(line))

		data.append("---|---|---|---|---|---|")
		data.append("")

		sys.stdout.write("\n".join(data))
		sys.stdout.write("\x1B[" + str(removes_before) + "E")


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


	def predict_move_piece(self, coo: NDArray, dire: NDArray) -> NDArray:
		"""
		Returns the expected position of the piece at coordinates 'coo'
		if it where to be moven.
		"""

		n_coo = array(coo, copy=True)

		while self.lookup_coo(n_coo + dire) == " ":
			n_coo += dire

		return n_coo


	def move_piece(self, coo: NDArray, dire: NDArray) -> None:
		"""Moves a piece from the coordinates in a choosen direction."""

		piece_type = self.lookup_coo(coo)
		final_coo = self.predict_move_piece(coo, dire)

		self.set_coo(coo, " ")
		self.set_coo(final_coo, piece_type)
		
		return


	def move_cursor(self, dire: NDArray, is_coo: bool = False) -> None:
		if is_coo:
			new_selection = dire.copy()

		new_selection = self.selection.copy() + dire.copy()

		if new_selection[0] in range(5) and new_selection[1] in range(5):
			self.selection = new_selection

		return


	def check_win(self, player: str) -> bool:
		"""Checks if the player 'player' won."""

		for row in range(5):
			for column in range(5):
				pos = array((row, column))
				if self.lookup_coo(pos) != player:
					continue

				for dire in Letrecot.neighbords_cells.values():
					if self.lookup_coo(pos + dire) != player:
						continue
					if self.lookup_coo(pos + 2*dire) == player:
						return True

		return False


#region 2 player game

def move_cursor_sequence(game: Letrecot, remove: bool = False, reverse: bool = False, message: str = "") -> None:
	
	usr_key = ""
	dire = {"\x1b[A": array((-1,  0)), #Up
			"\x1b[B": array(( 1,  0)), #Down
			"\x1b[C": array(( 0,  1)), #Right
			"\x1b[D": array(( 0, -1))} #Left

	game.display_board(removes_before=4*remove , include_select=True)
	if remove:
		sys.stdout.write("\x1B[3F")
	sys.stdout.write("Use the directional arrows to move te cursor.\n")
	sys.stdout.write("Press 'esc' or 'enter' to exit.\n")
	sys.stdout.write(message + "\n")

	while usr_key not in ("\x1b", "\r"):
		usr_key = click.getchar()

		if usr_key in dire:
			game.move_cursor(dire[usr_key])
			game.display_board(removes_before=4, include_select=True)

	return


def choose_dir_sequence(game: Letrecot, message: str = "", remove: bool = False) -> NDArray:
	
	usr_key = ""
	curent_dir = array((0, 0))

	dire = {"\x1b[A": array((-1,  0)), #Up
			"\x1b[B": array(( 1,  0)), #Down
			"\x1b[C": array(( 0,  1)), #Right
			"\x1b[D": array(( 0, -1))} #Left

	dir_arrows = {"[0 1]":    "🡢",
				  "[1 1]" :   "🡦",
				  "[1 0]":    "🡣",
				  "[ 1 -1]":  "🡧",
				  "[ 0 -1]":  "🡠",
				  "[-1 -1]":  "🡤",
				  "[-1  0]":  "🡡",
				  "[-1  1]":  "🡥",
				  "[0 0]":    "."}
	if remove:
		sys.stdout.write("\x1B[1F")
	sys.stdout.write("\x1B[3F")
	sys.stdout.write("Use the directional arrows to choose your direction.\n")
	sys.stdout.write("Press 'esc' or 'enter' to exit.\n")
	sys.stdout.write("\x1B[K")
	sys.stdout.write(message + "\n")
	sys.stdout.write(".\n")


	while usr_key not in ("\x1b", "\r"):
		usr_key = click.getchar()

		if usr_key in dire:
			curent_dir += dire[usr_key]
			if abs(curent_dir[0]) == 2:
				curent_dir[0] = curent_dir[0] // 2
				curent_dir[1] = 0
			elif abs(curent_dir[1]) == 2:
				curent_dir[1] = curent_dir[1] // 2
				curent_dir[0] = 0

		sys.stdout.write("\x1B[1F")
		sys.stdout.write(dir_arrows[str(curent_dir)] + "\n")

	return curent_dir


def play():
	#initialisation
	main_game = Letrecot()
	has_won = False
	turn = True
	players = {True: "X", False: "O"}
	nb_turn = 0

	error_message_cursor = "You have no piece in this position."
	error_message_direction = "Your piece will not move at all in this situation."


	sys.stdout.write("Welcome to Letrecot \n\n")

	while not has_won:
		nb_turn += 1
		sys.stdout.write(f"Turn {nb_turn} ({players[turn]})\n")

		move_cursor_sequence(main_game)
		choosed_pos_val = main_game.lookup_coo(main_game.selection)
		while choosed_pos_val != players[turn]:
			move_cursor_sequence(main_game, message=error_message_cursor, remove=True)
			choosed_pos_val = main_game.lookup_coo(main_game.selection)

		choosed_dir = choose_dir_sequence(main_game)
		next_pos = main_game.predict_move_piece(main_game.selection, choosed_dir)
		while (next_pos == main_game.selection).all():
			choosed_dir = choose_dir_sequence(main_game, message=error_message_direction, remove=True)
			next_pos = main_game.predict_move_piece(main_game.selection, choosed_dir)

		main_game.move_piece(main_game.selection, choosed_dir)
		has_won = main_game.check_win(players[turn])

		sys.stdout.write("\x1B[19F\x1B[0J\n")

		turn = not turn

	sys.stdout.write(f"Turn {nb_turn}\n")
	main_game.display_board()
	sys.stdout.write(f"\nPlayer ({players[not turn]}) Won!!!\n")
	sys.stdout.write("Press any key to finish.\n")
	click.pause()
	sys.stdout.write("\n")

#endregion


if __name__ == "__main__":
	play()