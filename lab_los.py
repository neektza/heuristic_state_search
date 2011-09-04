# implementirati PUNO BOLJU HEURISTIKU


import re
import copy

class PuzzleError(Exception):
	def __init__(self, value):
		value = value
	def __str__(self):
		return repr(value)
		
class Puzzle:
	def __init__(self, tab, parent,g):
		self.state = tab
		self.no_rows = len(tab)
		self.no_columns = len(tab[0])
		self.parent = parent
		self.g=g
		for i in range(self.no_rows):
			for j in range(self.no_columns):
				if (tab[i][j] == '0'):
					self.blank_row = i
					self.blank_column = j
		self.h=100
		self.f=self.g+self.h
					

	def __cmp__(self, other):
		return cmp(self.f, other.f)

	def __eq__(self, other):
		return (self.state == other.state)	    

	def equals(self, other):
		if self.state == other.state:
			return True
		else:
			return False
			
	def calc_f(self):
		#heuristicka funkcija 
		# implementirati manhattan udaljenosti umjesto ovog smeca
		self.h=0
		for i in range(self.no_rows):
			for j in range(self.no_columns):
				if self.state[i][j] != str(i*self.no_columns+j+1):
					self.h = self.h + 1
					
		self.f = self.h+self.g
		
	def print_state(self):
		for i in range(self.no_rows):
			print self.state[i]
		print

	def possible_moves(self):
		moves=[]
		if (self.blank_row > 0):
			moves.append("U")
		if (self.blank_row < self.no_rows-1):
			moves.append("D")
		if (self.blank_column > 0):
			moves.append("L")
		if (self.blank_column < self.no_columns-1):
			moves.append("R")
		return moves
		
def parse():
	"""Vraca listu listi charova - tablicu."""
	fajl = open('input2.txt' , 'r')
	format = fajl.readline()
	format = format.lower()
	regex = re.compile('[1-9][0-9]*x[1-9][0-9]*')
	if regex.match(format):
		dimenzije = format.split("x")
		br_redaka = int(dimenzije[0])
		br_stupaca = int(dimenzije[1])
		retci = fajl.readlines(br_redaka)
		tablica = []
		if len(retci) != br_redaka:
			raise PuzzleError('Slagalica ne odgovara zadanom opisniku')
		for redak in retci:
			redak = redak.replace('\n','')
			redak = redak.replace('\r','')
			redak = redak.split(',')
			tablica.append(redak)
			if len(redak) != br_stupaca:
				raise PuzzleError('Slagalica ne odgovara zadanom opisniku')
	else:
		raise PuzzleError('Prvi redak datoteke mora biti opisnik slagalice (NxM)')
	return tablica
		
#implementirati ovo sranje za NxN ALI da je 0 na zadnjem mjestu
#~ def calc_goal_state(no_rows, no_columns):
	#~ """ Racuna kako bi trebalo izgledati ciljno stanje za NxM tablicu."""
	#~ table = []
	#~ for i in range(1,no_rows+1):
		#~ if (i != no_rows+1):
			#~ row = range(i*no_columns-no_columns+1, i*no_columns+1)
		#~ else:
			#~ row = range((i-1)*no_columns
		#~ row_str = []
		#~ for a in row:
			#~ row_str.append(str(a))
		#~ table.append(row_str)
	#~ GOAL_STATE = table
	#~ return GOAL_STATE


def move_blank(table_in,blank_row, blank_column, direction):
	"""Pomice prazninu u zadanom smjeru."""
	table_out = copy.deepcopy(table_in)
	if direction== "U":
		temp = table_out[blank_row-1][blank_column]
		table_out[blank_row-1][blank_column] = '0'
		table_out[blank_row][blank_column] = temp
	elif direction== "D":
		temp = table_out[blank_row+1][blank_column]
		table_out[blank_row+1][blank_column] = '0'
		table_out[blank_row][blank_column] = temp
	elif direction== "L":
		temp = table_out[blank_row][blank_column-1]
		table_out[blank_row][blank_column-1] = '0'
		table_out[blank_row][blank_column] = temp
	elif direction== "R":
		temp = table_out[blank_row][blank_column+1]
		table_out[blank_row][blank_column+1] = '0'
		table_out[blank_row][blank_column] = temp
	return table_out
	
#implementirati kao rekurziju...
def backtrack(node):
	if (node.parent):
		backtrack(node.parent)
	node.print_state()
		
	

#argumenti su (tablica - [][], referenca na roditelja, dubina g)
start_node = Puzzle(parse(), None, 1)
#~ GOAL_STATE = calc_goal_state(start_node.no_rows, start_node.no_columns)
open_nodes = [start_node]
closed_nodes = []
temp_path = []
g = 1

GOAL_STATE = [['1','2','3'],['4','5','6'],['7','8','0']]
#~ print GOAL_STATE

# ... A* pocinje ...
while (open_nodes != []):
	current_node = open_nodes.pop(0)
	closed_nodes.append(current_node)
	print current_node.f
	
	if current_node.state == GOAL_STATE:
		print "USPJEH"
		print "nivo (g) jest " + str(g)
		print "put do rjesenja:"
		backtrack(current_node)
		break
	
	else:
		moves = current_node.possible_moves()
		expanded_nodes = []
		
		#~ print "current_node is:"
		#~ current_node.print_state()
		#~ print
		
		#~ print "moves are:"
		#~ print moves
		#~ print
		
		# generacija djece...
		for move in moves: 
			new_table = move_blank(current_node.state, current_node.blank_row, current_node.blank_column, move)			
			child_node = Puzzle(new_table, current_node, g+1)
			expanded_nodes.append(child_node)
		
		for node in expanded_nodes:
			open_nodes.append(node)
			
		#~ print "expanded_nodes are: "
		#~ for node in expanded_nodes:
			#~ node.print_state()
			#~ print
	
	in_open = 0
	in_closed = 0
	for node in expanded_nodes:
		if (open_nodes.count(node) != 0): in_open = 1
		if (closed_nodes.count(node) != 0): in_closed= 1
		
		if (not in_open and not in_closed):
			node.calc_f()
			open_nodes.append(node)
		elif (in_open):
			#ako je put kojim smo dosli do cvora kraci od prijasnjeg, zapisi novi g(nivo) u cvor, i daj mu novi put
			if (open_nodes[(open_nodes.index(node))].g>g):
				open_nodes[(open_nodes.index(node))].g = g
				open_nodes[(open_nodes.index(node))].parent = current_node
		elif (in_closed):
			#ako smo dosli do njega kracim putem stavi ga u open i makni iz closed
			if (open_nodes[(open_nodes.index(node))].g>g):
				closed_nodes.append(open_nodes.pop(open_nodes.index(node)))
			
	
	open_nodes.sort()
	
	#~ print "open"
	#~ for o in open_nodes:
		#~ o.print_state()
		#~ print o.h
		
	#~ print "closed"
	#~ for c in closed_nodes:
		#~ c.print_state()
		#~ print c.h
	#~ print g
	g=g+1
