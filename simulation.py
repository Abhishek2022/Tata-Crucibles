import random
import os
import sys
import time
from pprint import pprint

g_737 = (0,0,0,1,0,0,0)
g_747 = (0,0,1,0,0,0,0,1,0,0)
g_a380 = (0,0,0,1,0,0,0,0,0,1,0,0,0)


class Agent(object):

    def __init__(self, seat, baggage, plane):
        self.seat = seat #row, col
        self.pos = [-1, -1]
        self.moveCnt = -1
        self.curMove = ''
        self.baggage = baggage
        self.plane = plane

    def __str__(self):
        return f'{self.seat} | {self.pos} | {self.baggage}'

    def __repr__(self):
        return f'{self.seat} | {self.pos} | {self.baggage}'

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
        self.passangers = []
        self.squares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]
        self.nextSquares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]

    def nextStep(self):
        self.squares = self.nextSquares
        self.nextSquares = [[[] for _ in range(len(self.layout))] for _ in range(self.rows)]

    def allSeated(self):
        for agent in self.passangers:
            if agent.curMove != 'sit':
                return False
        return True

    def empty(self, row, col):
        return len(self.squares[row][col]) == 0 and len(self.nextSquares[row][col]) == 0


def run(rows, layout, method, bag, printPlane):
    plane = Plane(rows, layout)
    passangers = []
    seatCols = []
    aisleCols = []
    for i,seat in enumerate(layout):
        if seat == 0:
            seatCols.append(i)
        else:
            aisleCols.append(i)

    for row in range(rows):
        curRow = []
        for col in seatCols:
            baggage = int(round(random.gauss(bag['mu'], bag['sigma']),0))
            curRow.append(Agent([row, col], baggage, plane))
        passangers.append(curRow)

    # form queue
    queue = []
    if method[0] == 'row-front':
        step = method[1]
        for i in range(0,rows,step):
            batch = [p for row in passangers[i:i+step] for p in row if p]
            random.shuffle(batch)
            queue.extend(batch)
    elif method[0] == 'row-back':
        step = method[1]
        for i in range(0,rows,step):
            batch = [p for row in passangers[rows-i-step:rows-i] for p in row if p]
            random.shuffle(batch)
            if batch:
                queue += batch

    elif method[0] == 'random':
        for row in passangers:
            queue += row
        random.shuffle(queue)

    else:
        raise Exception(f'No method name {method}')

    # run things
    rounds = 0
    while True:
        if len(queue) == 0 and plane.allSeated():
            return rounds

        # update agents
        for agent in plane.passangers:
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
                plane.passangers.append(nxtPass)
        plane.nextStep()
        # print plane
        if printPlane:
            os.system('clear')

            print(f'method: {method[0]} | batch: {method[1]}')
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
            time.sleep(0.04)

        rounds += 1


if len(sys.argv) != 5:
    print('usage: ./boardSim [numRuns] [numRows] [layout] [printPlane]')
    print('numRuns - Number of runs to take the average of')
    print('numRows - Number of rows in the airplane')
    print('layout - one of "737", "747", "a380"')
    print('printPlane - 1 if you want the plane to be printed, 0 otherwise')
    sys.exit(0)

runs = int(sys.argv[1])
rows = int(sys.argv[2])
if sys.argv[3] == '737':
    plane = g_737
elif sys.argv[3] == '747':
    plane = g_747
elif sys.argv[3] == 'a380':
    plane = g_a380
else:
    raise Exception(f'Unknown layout - {sys.argv[3]}')

printPlane = True if sys.argv[4] == '1' else False

batch = rows//5
methods = [ # methods - pass along with a batch parameter defined above
    'row-back',
    'random',
    'row-front',
]

bag = { # actual baggage time is rounded to nearest integer
    'mu': 18,
    'sigma': 6,
}

avgs = [0 for i in range(len(methods))]
for i in range(runs):
    for i,method in enumerate(methods):
        avgs[i] += run(rows, plane, (method,batch), bag, printPlane)

for i,av in enumerate(avgs):
    print(f'{methods[i][0]} - {round(av/runs,2)}')
