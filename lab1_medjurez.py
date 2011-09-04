# implementirati PUNO BOLJU HEURISTIKU


import re
import copy


global GOAL_STATE, GOAL_POSITIONS

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
		
		#trazi prazninu
		for i in range(self.no_rows):
			for j in range(self.no_columns):
				if (tab[i][j] == '0'):
					self.blank_row = i
					self.blank_column = j
		
		#racunaj heuristiku za cvor
		self.h=0
		for i in range(self.no_rows): 
			for j in range(self.no_columns):
				goal_pos = GOAL_POSITIONS[self.state[i][j]]
				x = goal_pos[0]
				y = goal_pos[1]
				self.h += (abs(x-i) + abs(y-j))
				
		self.f = self.g+self.h
		
	def __cmp__(self, other):
		return cmp(self.f, other.f)

	def __eq__(self, other):
		return (self.state == other.state)	    

	def equals(self, other):
		if self.state == other.state:
			return True
		else:
			return False
		
	#~ def calc_f(self):
		#~ self.h=0
		#~ for i in range(self.no_rows):
			#~ for j in range(self.no_columns):
				#~ goal_pos = GOAL_POSITIONS[self.state[i][j]]
				#~ x = goal_pos[0]
				#~ y = goal_pos[1]
				#~ self.h += (abs(x-i) + abs(y-j))
				
		#~ self.f = self.g+self.h
						
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
	return tablica, br_redaka, br_stupaca
		

def calc_goal_state_and_positions (no_rows, no_columns):
	#ciljno stanje
	GOAL_STATE = []
	for i in range(1,no_rows+1):
		if i == no_rows: 
			row = range(i*no_columns-no_columns+1, i*no_columns)
			row.append('0')
		else: 
			row = range(i*no_columns-no_columns+1, i*no_columns+1)
		row_str = []
		for a in row:
			row_str.append(str(a))
		GOAL_STATE.append(row_str)
	
	#ciljne pozicije
	list_for_dict = []
	for i in range(no_rows):
		for j in range(no_columns):
			number_in_question = str((i*no_columns)+j+1)
			position_of_niq = [i,j]
			tapl = str(number_in_question), position_of_niq
			list_for_dict.append(tapl)
	GOAL_POSITIONS = dict(list_for_dict)
	GOAL_POSITIONS['0'] = [no_rows-1,no_columns-1]
	return GOAL_STATE, GOAL_POSITIONS


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
	
def backtrack(node):
	if (node.parent):
		backtrack(node.parent)
	node.print_state()
		
	
tablica, N, M = parse()
GOAL_STATE, GOAL_POSITIONS = calc_goal_state_and_positions(N,M)
start_node = Puzzle(tablica, None, 1)
open_nodes = [start_node]
closed_nodes = []
temp_path = []
g = 1

print "goal state is"
print GOAL_STATE

print "goal positions are"
print GOAL_POSITIONS

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
		
		if (not in_open or not in_closed):
			#~ node.calc_f()
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
