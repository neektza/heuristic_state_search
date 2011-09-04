#GRESKA
#SVE POTEZE RADI NA ISTOM OBJEKTU 
#(NE GENERIRA DJECU, VEC SAMO MIJENJA TEMPX)


import re

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
		for i in range(self.no_rows):
			for j in range(self.no_columns):
				if (tab[i][j] == '0'):
					self.blank_row = i
					self.blank_column = j
					
		self.g=g
		
		#heuristicka funkcija
		self.h=0
		for i in range(self.no_rows):
			for j in range(self.no_columns):
				if self.state[i][j] != str(i*self.no_columns+j):
					self.h = self.h + 1
					
		self.f = self.h+self.g

	def __cmp__(self, other):
		return cmp(self.f, other.f)

	def __eq__(self, other):
		return (self.state == other.state)	    

	def equals(self, other):
		if self.state == other.state:
			return True
		else:
			return False
		
	def print_state(self):
		for i in range(self.no_rows):
			print self.state[i]
		print
		
	def move_up(self):
		if (self.blank_row > 0):
			temp = self.state[self.blank_row-1][self.blank_column]
			self.state[self.blank_row-1][self.blank_column] = '0'
			self.state[self.blank_row][self.blank_column] = temp
			self.blank_row = self.blank_row - 1
		else:
			raise PuzzleError('Nedopusten pomak praznog polja!')
		#~ return self.state   

	def move_down(self):
		if (self.blank_row < self.no_rows-1):
			temp = self.state[self.blank_row+1][self.blank_column]
			self.state[self.blank_row+1][self.blank_column] = '0'
			self.state[self.blank_row][self.blank_column] = temp
			self.blank_row = self.blank_row + 1
		else:
			raise PuzzleError('Nedopusten pomak praznog polja!')
		#~ return self.state

	def move_left(self):
		if (self.blank_column > 0):
			temp = self.state[self.blank_row][self.blank_column-1]
			self.state[self.blank_row][self.blank_column-1] = '0'
			self.state[self.blank_row][self.blank_column] = temp
			self.blank_column = self.blank_column - 1
		else:
			raise PuzzleError('Nedopusten pomak praznog polja!')
		#~ return self.state

	def move_right(self):
		if (self.blank_column < self.no_columns-1):
			temp = self.state[self.blank_row][self.blank_column+1]
			self.state[self.blank_row][self.blank_column+1] = '0'
			self.state[self.blank_row][self.blank_column] = temp
			self.blank_column = self.blank_column + 1
		else:
			raise PuzzleError('Nedopusten pomak praznog polja!')
		#~ return self.state

	def possible_moves(self):
		moves = []
		if (self.blank_row > 0):
			moves.append(self.move_up)
		if (self.blank_row < self.no_rows-1):
			moves.append(self.move_down)
		if (self.blank_column > 0):
			moves.append(self.move_left)
		if (self.blank_column < self.no_columns-1):
			moves.append(self.move_right)
		return moves
		
def parse():
	"""Vraca listu listi charova - tablicu."""
	fajl = open('input.txt' , 'r')
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
		
def calc_goal_state(no_rows, no_columns):
	""" Racuna kako bi trebalo izgledati ciljno stanje za NxM tablicu."""
	table = []
	for i in range(1,no_rows+1):
		row = range(i*no_columns-no_columns, i*no_columns)
		row_str = []
		for a in row:
			row_str.append(str(a))
		table.append(row_str)
	GOAL_STATE = table
	return GOAL_STATE
	
#implementirati kao rekurziju...
def backtrack():
	return "da"

#argumenti su (tablica - [][], referenca na roditelja, dubina g)
start_node = Puzzle(parse(), None, 1)
GOAL_STATE = calc_goal_state(start_node.no_rows, start_node.no_columns)
open_nodes = [start_node]
closed_nodes = []
temp_path = []
g = 1

# ... A* pocinje ...
while (open_nodes != [] and g<3):
	current_node = open_nodes.pop(0)
	closed_nodes.append(current_node)
	
	if current_node.state == GOAL_STATE:
		print "USPJEH"
		print "put do rjesenja:"
		#~ backtrack()
	
	else:
		moves = current_node.possible_moves()
		expanded_nodes = []
		
		print "parent is:"
		current_node.print_state()
		print
		
		#~ print "moves are:"
		#~ print moves
		#~ print
		
		# generacija djece
		for move in moves: 
			child_node = Puzzle(current_node.state, current_node, g+1)
			print move
			move()
			
			print "dijete i"
			child_node.print_state()
		
			expanded_nodes.append(child_node)
	
		for node in expanded_nodes:
			open_nodes.append(node)

	
	#popraviti uvjetovanje
	#~ for node in expanded_nodes:
		#~ if (open_nodes.count(node)!=0 or closed_nodes.count(node)!=0):
			#~ open_nodes.append(node)
		#~ elif (open_nodes.count(node)!=0):
			#~ if (g<node.g):
				#~ node.parent = current_node
		#~ elif (closed_nodes.count(node)!=0):
			#~ if (g<node.g):
				#~ closed_nodes.remove(node)
				#~ open_nodes.append(node)
	
	open_nodes.sort()
	
	print "open"
	for o in open_nodes:
		o.print_state()
		#~ print o.f
		
	print "closed"
	for c in closed_nodes:
		c.print_state()
		#~ print c.f
	
	g=g+1
