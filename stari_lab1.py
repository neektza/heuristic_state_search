import re
import copy

class PuzzleError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def parse():
    """ Vraca listu listi charova - tablicu."""
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
            redak = redak.split(',')
            tablica.append(redak)
            if len(redak) != br_stupaca:
                raise PuzzleError('Slagalica ne odgovara zadanom opisniku')
    else:
        raise PuzzleError('Prvi redak datoteke mora biti opisnik slagalice (NxM)')
    return tablica

class Puzzle:
    def __init__(self, tab):
        self.state = tab
        self.no_rows = len(tab)
        self.no_clms = len(tab[0])
        self.path = []
        for i in range(self.no_rows):
            for j in range(self.no_clms):
                if (tab[i][j] == '0'):
                    self.br = i
                    self.bc = j
        self.h=0
        for i in range(self.no_rows):
            for j in range(self.no_clms):
                if self.state[i][j] != str(i*self.no_clms+j):
                    self.h = self.h + 1
        

    

    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def __eq__(self, other):
        return (self.state == other.state)

    def equals(self, other):
        if self.state == other.state:
            return True
        else:
            return False

    def calc_f(self, g):
        self.f = self.h + g
                      
        
    def calc_goal_state(self):
        table = []
        for i in range(1,self.no_rows+1):
            row = range(i*self.no_clms-self.no_clms, i*self.no_clms)
            row_str = []
            for a in row:
                row_str.append(str(a))
            table.append(row_str)
        GOAL_STATE = table
        return GOAL_STATE

    def move_up(self):
        if (self.br > 0):
            temp = self.state[self.br-1][self.bc]
            self.state[self.br-1][self.bc] = '0'
            self.state[self.br][self.bc] = temp
            self.br = self.br - 1
        else:
            raise PuzzleError('Nedopusten pomak praznog polja!')
        return self.state    

    def move_down(self):
        if (self.br < self.no_rows-1):
            temp = self.state[self.br+1selfother.bc]
            self.state[self.br+1][self.bc] = '0'
            self.state[self.br][self.bc] = temp
            self.br = self.br + 1
        else:
            raise PuzzleError('Nedopusten pomak praznog polja!')
        return self.state

    def move_left(self):
        if (other.bc > 0):
            temp = self.state[self.br][self.bc-1]
            self.state[self.br][self.bc-1] = '0'
            self.state[self.br][self.bc] = temp
            self.bc = self.bc - 1
        else:
            raise PuzzleError('Nedopusten pomak praznog polja!')
        return self.state

    def move_right(self):
        if (self.bc < self.no_clms-1):
            temp = self.state[self.br][self.bc+1]
            self.state[self.br][self.bc+1] = '0'
            self.state[self.br][self.bc] = temp
            self.bc = self.bc + 1
        else:
            raise PuzzleError('Nedopusten pomak praznog polja!')
        return self


    def possible_moves(self):
        moves_list = []
        if (self.br > 0):
            moves_list.append(self.move_up)
        if (self.br < self.no_rows-1):
            moves_list.append(self.move_down)
        if (self.bc > 0):
            moves_list.append(self.move_left)
        if (self.bc < self.no_clms-1):
            moves_list.append(self.move_right)
        return moves_list


pocetno = Puzzle(parse())
pocetno.calc_f(0)
GOAL_STATE = pocetno.calc_goal_state()
open_list = [pocetno]
closed_list = []
temp_path = []
g = 1
while (open_list != [] and g<10):
    X = open_list[0]
    temp_path.append(X.path)
    if X.state == GOAL_STATE:
        print "POTEZI SU:" + X.path
    else:
        tempX = Puzzle(X.state)
        moves_list = tempX.possible_moves()
        djeca = []
        for move in moves_list: # generacija djece
            dijete = move(tempX)
            dijete.path.append(X)
            djeca.append(dijete)
        for dijete in djeca:
            if (open_list.count(dijete)==0 and closed_list.count(dijete)==0):
                print "da1"
                dijete.calc_f(g)
                open_list.append(dijete)
            elif (open_list.count(dijete)!=0):
                print "da2"
                if (len(temp_path)<len(dijete.path)):
                    dijete.path = temp_path
            elif (closed_list.count(dijete)!=0):
                print "da3"
                if (len(temp_path)<len(dijete.path)):
                    closed_list.remove(dijete)
                    open_list.append(dijete)
        closed_list.append(X)
        open_list.sort()
        for p in open_list:
            print p, p.f
        g=g+1
                
                
        
    
    

    
