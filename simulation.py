import random
import os
import sys
import time
import numpy as np
from tqdm import tqdm
from pprint import pprint
from ticket import TicketBlock

AIR_LAYOUT = {
    '737': (0,0,0,1,0,0,0),
    '747': (0,0,1,0,0,0,0,1,0,0),
    'a380': (0,0,0,1,0,0,0,0,0,1,0,0,0),
}

class Agent(object):

    def __init__(self, id, seat, baggage, plane):
        self.seat = seat # row, col
        self.id = id
        self.pos = [-1, -1]
        self.moveCnt = -1
        self.curMove = ''
        self.baggage = baggage
        self.plane = plane
        self.block = None # Block number printed on his ticket
        self.group = False
        self.first = False # if first member of group
        self.group_members = [] # other members of the group

    def __str__(self):
        if self.group:
            return f'P: [{self.id}, {self.block},  {self.seat}] - {self.baggage} | {self.group_members}'
        else:
            return f'P: [{self.id}, {self.block},  {self.seat}] - {self.baggage}'

    def __repr__(self):
        return self.__str__()

    def setGroup(self,grp):
        self.group = grp

    def chooseMove(self):

        if self.seat == self.pos:
            self.curMove = 'sit'
            return

        if self.seat[0] > self.pos[0]:
            self.curMove = 'up'
            return

        if self.seat[0] == self.pos[0]:
            if self.baggage > 0:
                self.curMove = 'baggage'
                return
            if self.seat[1] > self.pos[1]:
                self.curMove = 'right'
                return
            else:
                self.curMove = 'left'
                return
        print("error! Unknows step")

    def move(self):
        if self.curMove == '':
            self.chooseMove()
        if self.curMove == 'sit':
            self.sit()
        if self.curMove == 'up':
            self.moveUp()
        if self.curMove == 'baggage':
            self.setBaggage()
        if self.curMove == 'right':
            self.moveRight()
        if self.curMove == 'left':
            self.moveLeft()
        if self.curMove == 'standLeft':
            self.standLeft()
        if self.curMove == 'standRight':
            self.standRight()


    def moveRight(self):
        clear = True
        for seat in range(self.pos[1]+1, self.seat[1]):
            if not self.plane.empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.squares[self.pos[0]][seat]:
                    if agent.seat[1] < self.seat[1] and not agent in self.plane.nextSquares[self.pos[0]][self.pos[1]]:
                        agent.curMove = 'standLeft'
        if not clear:
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            myTurn = True
            for agent in self.plane.squares[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue
                if agent.seat[1] > self.seat[1] and agent.curMove == self.curMove:
                    myTurn = False
            if not myTurn:
                self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] += 1
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.curMove = ''
            return

    def moveLeft(self):
        clear = True
        for seat in range(self.seat[1], self.pos[1]):
            if not self.plane.empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.squares[self.pos[0]][seat]:
                    if agent.seat[1] > self.seat[1] and not agent in self.plane.nextSquares[self.pos[0]][self.pos[1]]:
                        agent.curMove = 'standRight'
        if not clear:
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            myTurn = True
            for agent in self.plane.squares[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue
                if agent.seat[1] < self.seat[1] and agent.curMove == self.curMove:
                    myTurn = False
            if not myTurn:
                self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] -= 1
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.curMove = ''
            return

    def moveUp(self):
        if self.plane.empty(self.pos[0]+1, self.pos[1]) and len(self.plane.squares[self.pos[0]][self.pos[1]]) == 1:
            self.pos[0] += 1
            self.curMove = ''
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def setBaggage(self):
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        self.baggage -= 1
        if self.baggage == 0:
            self.curMove = ''
        return

    def standLeft(self):
        if self.plane.empty(self.pos[0], self.pos[1]-1) or self.plane.layout[self.pos[1]-1] == 1:
            self.pos[1] -= 1
        if self.plane.layout[self.pos[1]] == 1:
            self.curMove = 'right'
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def standRight(self):
        if self.plane.empty(self.pos[0], self.pos[1]+1) or self.plane.layout[self.pos[1]+1] == 1:
            self.pos[1] += 1
        if self.plane.layout[self.pos[1]] == 1:
            self.curMove = 'left'
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def sit(self):
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return


class Plane(object):

    def __init__(self, rows, layout):
        # layout: (0,0,1,0,0,0,1,0,0)
        # 1 - isle, 0 - seat
        self.rows = rows
        self.layout = layout
        self.passengers = []
        self.squares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]
        self.nextSquares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]

    def nextStep(self):
        self.squares = self.nextSquares
        self.nextSquares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]

    def allSeated(self):
        for agent in self.passengers:
            if agent.curMove != 'sit':
                return False
        return True

    def empty(self, row, col):
        return len(self.squares[row][col]) == 0 and len(self.nextSquares[row][col]) == 0

# Flatten a 2-d list
flatten = lambda lst: [elem for row in lst for elem in row]

def find(lst, id):
    for pas in flatten(lst):
        if id == pas.id:
            return pas
    raise Exception(f'No passenger with id {id}')

def find_flat(lst,id):
    for pas in lst:
        if id == pas.id:
            return pas
    raise Exception(f'No passenger with id {id}')

def rearrange_groups(queue):
    """
    Rearrange the list such that groups appear together
    List should be 1-d
    """
    q_copy = queue[:]
    for i,pas in enumerate(q_copy):
        if pas.first:
            for j,member_id in enumerate(pas.group_members):
                new_pas = find_flat(q_copy, member_id)
                q_copy.remove(new_pas)
                orig_ind = q_copy.index(find_flat(q_copy, pas.id))
                q_copy.insert(orig_ind+j+1, new_pas)
    return q_copy

def create_pass(rows, plane, sc, groups): # create passengers
    passengers = []
    for row in range(rows):
        curRow = []
        for j,col in enumerate(sc):
            baggage = int(round(random.gauss(bag['mu'], bag['sigma']),0))
            id = row*len(sc) + j
            curRow.append(Agent(id, [row, col], baggage, plane))
        passengers.append(curRow)

    # Group passengers
    all = list(range(rows*len(sc)))
    all_grps = []
    for k,v in groups.items():
        num_groups = int(v*len(all))
        for i in range(num_groups):
            initial = np.random.choice(all)
            group = []
            ind = all.index(initial)
            bi = 1
            for j in range(k):
                if ind+j >= len(all):
                    group.append(all[ind-bi])
                    bi+=1
                else:
                    group.append(all[ind+j]) # Add passengers to this group

            all = [p for p in all if p not in group] # remove group passengers from list of all passengers
            all_grps.append(group)

            for j,group_mem in enumerate(sorted(group)): # add groups to agents
                pas = find(passengers,group_mem)
                pas.group = True
                if j == 0:
                    pas.first = True
                pas.group_members = sorted(group.copy())
                pas.group_members.remove(group_mem)

    return passengers

def run(rows, layout, block_method, bag, groups, batch_size=None, printPlane=False):
    plane = Plane(rows, layout) # Set up plane according to layout
    seatCols = []
    aisleCols = []
    for i,seat in enumerate(layout):
        if seat == 0:
            seatCols.append(i)
        else:
            aisleCols.append(i)

    passengers = create_pass(rows, plane, seatCols, groups) # create the passengers along with their groups

    ticket = TicketBlock(rows,passengers)
    ticket.set_block(block_method) # Divide into blocks according to chosen scheme

    # form queue
    queue = sorted(flatten(passengers), key=lambda x: x.block)

    if batch_size is not None: # Break passengers into batches only if batch_size is set
        for i in range(0,rows*len(seatCols),batch_size*len(seatCols)):
            slice = queue[i:i+batch_size*len(seatCols)]
            random.shuffle(slice)
            queue[i:i+batch_size*len(seatCols)] = slice # slices are immutable

    queue = rearrange_groups(queue) # Enable grouping passengers

    # run things
    rounds = 0
    while True:
        if len(queue) == 0 and plane.allSeated():
            return rounds

        # update agents
        for agent in plane.passengers:
            agent.move()
        # check queue
        if len(queue) > 0:
            bestAisle = None
            bestDist = -1
            for aisle in aisleCols:
                dist = abs(aisle-queue[0].seat[1])
                if bestDist == -1 or dist < bestDist:
                    bestDist = dist
                    bestAisle = aisle
            if plane.empty(0, bestAisle):
                nxtPass = queue.pop(0)
                nxtPass.pos = [0, bestAisle]
                plane.nextSquares[0][bestAisle].append(nxtPass)
                plane.passengers.append(nxtPass)
        plane.nextStep()
        # print plane
        if printPlane:
            os.system('clear')
            print(f'method: {block_method} | batch: {batch_size}')
            for _ in range(len(layout) + 1):
                print("", end='')
            for _ in range(len(queue)):
                print('<', end='')
            print('\n')
            for i in range(rows):
                print(str(i+1).zfill(2), end=' ')
                for j in range(len(layout)):
                    if len(plane.squares[i][j]) != 0:
                        if len(plane.squares[i][j]) > 1:
                            print(len(plane.squares[i][j]), end='')
                        elif plane.squares[i][j][0].curMove == 'standRight' or plane.squares[i][j][0].curMove == 'right':
                            print('>', end='')
                        elif plane.squares[i][j][0].curMove == 'standLeft' or plane.squares[i][j][0].curMove == 'left':
                            print('<', end='')
                        elif plane.squares[i][j][0].curMove == 'up':
                            print('V', end='')
                        elif plane.squares[i][j][0].curMove == 'baggage':
                            print('B', end='')
                        elif plane.squares[i][j][0].curMove == 'sit':
                            print('S', end='')
                        else:
                            print('?', end='')
                    elif j in aisleCols:
                        print('|', end='')
                    else:
                        print('_', end='')
                print('')
            print('\nCurrent round: {}'.format(rounds))
            time.sleep(wait_time)
        rounds += 1

################## Driver code #####################

if len(sys.argv) != 4:
    print('usage: ./boardSim [numRuns] [numRows] [printPlane]')
    print('numRuns - Number of runs to take the average of')
    print('numRows - Number of rows in the airplane')
    #print('layout - one of "737", "747", "a380"')
    print('printPlane - 1 if you want the plane to be printed, 0 otherwise')
    sys.exit(0)

runs = int(sys.argv[1])
rows = int(sys.argv[2])
#plane = AIR_LAYOUT[sys.argv[3]]
plane = AIR_LAYOUT['737']

printPlane = True if sys.argv[3] == '1' else False

 ############## Parameters ###################

batch = rows//3 # 3 batches by default

block_methods = [ # Methods of dividing passengers into blocks
    'random',
    'b2f', # back to front
    'f2b', # Front to back
    'wma', # Window-middle-aisle (3 classes)
    'wma_b2f', # Window-middle-aisle back to front (9 classes)
]

# Taken from "Agent-Based Evaluation of the Airplane Boarding Strategies’ Efficiency and Sustainability"
bag = { # actual baggage time is rounded to nearest integer (mostly list in 3-7 for our use-case)
    'mu': 5,
    'sigma': 2/3,
}
wait_time = 0.04

groups = { # percentage of groups, must add up to < 1 (remaining are solo)
    2: 0.1,
    3: 0.1,
    4: 0.1,
}

############################################

avg = np.zeros(len(block_methods), dtype=np.float32)
for j,block_method in enumerate(block_methods):
    if not printPlane:
        print(block_method)
        for i in tqdm(range(runs)):
            avg[j] += run(rows, plane, block_method, bag, groups, batch_size=batch, printPlane=printPlane)/runs
    else:
        for i in range(runs):
            avg[j] += run(rows, plane, block_method, bag, groups, batch_size=batch, printPlane=printPlane)/runs

print('Average time')
for j,block_method in enumerate(block_methods):
    print(f'\t{block_method} | {round(float(avg[j]),3)}')