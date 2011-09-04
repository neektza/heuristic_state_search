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
		self.size = len(tab)
		self.parent = parent
		self.g=g
		
		#trazi prazninu
		for i in range(self.size):
			for j in range(self.size):
				if (tab[i][j] == '0'):
					self.blank_row = i
					self.blank_column = j
		
		#racunaj heuristiku za cvor
		self.h=0
		for i in range(self.size): 
			for j in range(self.size):
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
	
	# ili tu ili u konstrutoru
	# trenutna implementacija u konstruktoru
	# losije, ali radi !
	#~ def calc_f(self):
		#~ self.h=0
		#~ for i in range(self.size):
			#~ for j in range(self.size):
				#~ goal_pos = GOAL_POSITIONS[self.state[i][j]]
				#~ x = goal_pos[0]
				#~ y = goal_pos[1]
				#~ self.h += (abs(x-i) + abs(y-j))
				
		#~ self.f = self.g+self.h
						
	def print_state(self):
		for i in range(self.size):
			print self.state[i]
		print

	def possible_moves(self):
		moves=[]
		if (self.blank_row > 0):
			moves.append("U")
		if (self.blank_row < self.size-1):
			moves.append("D")
		if (self.blank_column > 0):
			moves.append("L")
		if (self.blank_column < self.size-1):
			moves.append("R")
		return moves
		
	
def parse():
	fajl = open('input/input3_1' , 'r')
	format = fajl.readline()
	regex = re.compile('[1-9][0-9]*')
	if regex.match(format):
		velicina = int(format)
		retci = fajl.readlines(velicina)
		tablica = []
		if len(retci) != velicina:
			raise PuzzleError('Slagalica ne odgovara zadanom opisniku')
		for redak in retci:
			redak = redak.replace('\n','')
			redak = redak.replace('\r','')
			redak = redak.split(',')
			tablica.append(redak)
			if len(redak) != velicina:
				raise PuzzleError('Slagalica ne odgovara zadanom opisniku')
	else:
		raise PuzzleError('Prvi redak datoteke mora biti opisnik slagalice (velicina)')
	return tablica, velicina
		

def calc_goal_state_and_positions (size):
	#ciljno stanje
	GOAL_STATE = []
	for i in range(1,size+1):
		if i == size: 
			row = range(i*size-size+1, i*size)
			row.append('0')
		else: 
			row = range(i*size-size+1, i*size+1)
		row_str = []
		for a in row:
			row_str.append(str(a))
		GOAL_STATE.append(row_str)
	
	#ciljne pozicije
	list_for_dict = []
	for i in range(size):
		for j in range(size):
			number_in_question = str((i*size)+j+1)
			position_of_niq = [i,j]
			tapl = str(number_in_question), position_of_niq
			list_for_dict.append(tapl)
	GOAL_POSITIONS = dict(list_for_dict)
	GOAL_POSITIONS['0'] = [size-1,size-1]
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
	print "f(" + str(node.f) + ") = g("+ str(node.g) + ") + h(" + str(node.h) + ")"
	print
		
	
tablica, velicina = parse()
GOAL_STATE, GOAL_POSITIONS = calc_goal_state_and_positions(velicina)
start_node = Puzzle(tablica, None, 1)
open_nodes = [start_node]
closed_nodes = []
temp_path = []
iter = 1

#~ print "goal state is"
#~ print GOAL_STATE

#~ print "goal positions are"
#~ print GOAL_POSITIONS

# ... A* pocinje ...
while (open_nodes != []):
	current_node = open_nodes.pop(0)
	
	#~ print "current total heuristic value is: "
	#~ print current_node.f
	
	if current_node.state == GOAL_STATE:
		print "USPJEH"
		print "put do rjesenja:"
		print
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
			child_node = Puzzle(new_table, current_node, current_node.g+1)
			expanded_nodes.append(child_node)
		
		#~ OGROMAN BUG!!!!
		#~ for node in expanded_nodes:
			#~ open_nodes.append(node)
		#~ OGROMAN BUG!!!!
			
		#~ print "expanded_nodes are: "
		#~ for node in expanded_nodes:
			#~ node.print_state()
			#~ print
	
		#~ in_open = 0
		#~ in_closed = 0
		
		for node in expanded_nodes:
			
			#popraviti ovaj dio da radi direktno s indexom i hvata errore jer je tako brze
			#~ if (open_nodes.count(node) != 0): in_open = 1
			#~ if (closed_nodes.count(node) != 0): in_closed= 1
				
			#~ if in_closed: print "node is in closed"
			#~ if in_open: print "node is in open"
			
			if (open_nodes.count(node) == 0 and closed_nodes.count(node) == 0):
				#~ node.calc_f()
				open_nodes.append(node)
			elif (open_nodes.count(node) != 0):
				#ako je put kojim smo dosli do cvora kraci od prijasnjeg, zapisi novi g(nivo) u cvor, i daj mu novi put
				if (open_nodes[(open_nodes.index(node))].g>node.g):
					open_nodes[(open_nodes.index(node))].g = node.g
					open_nodes[(open_nodes.index(node))].parent = current_node
			elif (closed_nodes.count(node)!= 0):
				#ako smo dosli do njega kracim putem stavi ga u open i makni iz closed
				if (closed_nodes[(closed_nodes.index(node))].g>node.g):
					open_nodes.append(closed_nodes.pop(closed_nodes.index(node)))
		
		closed_nodes.append(current_node)
		
		open_nodes.sort()
	
	#~ print "open:" + str(len(open_nodes))
	
	#~ print "open"
	#~ for o in open_nodes:
		#~ o.print_state()
		#~ print "hje:" + str(o.h)
		
	#~ print "closed:" + str(len(open_nodes))
		
	#~ print "closed"
	#~ for c in closed_nodes:
		#~ c.print_state()
		#~ print c.h
	#~ print g

	iter=iter+1
