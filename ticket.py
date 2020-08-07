import random
import numpy as np

# Flatten a 2-d list
flatten = lambda lst: [elem for row in lst for elem in row]

class TicketBlock(object):
    """ Set the block number which will be printed on each passenger's ticket"""

    def __init__(self, rows, passengers):
        self.rows = rows
        self.passengers = flatten(passengers)

    def set_block(self, name):
        if name == 'random':
            self.random()
        elif name == 'b2f':
            self.b2f()
        elif name == 'f2b':
            self.f2b()
        elif name == 'wma':
            self.wma()
        elif name == 'wma_b2f':
            self.wma_b2f()
        elif name == 'stf_perf':
            self.steffen_perfect()
        elif name == 'stf_mod':
            self.steffen_modified()
        else:
            raise Exception(f'{name} is not defined in ticket.py')

    def random(self):
        """
        Random
        Divides into same number of blocks as passengers
        """
        block = list(range(len(self.passengers)))
        random.shuffle(block)
        for i,passenger in enumerate(self.passengers):
            passenger.block = block[i]

    def f2b(self):
        """
        Front to back
        Divides into same number of blocks as passengers
        """
        for passenger in self.passengers:
            passenger.block = passenger.id

    def b2f(self):
        """
        Back to front
        Divides into same number of blocks as passengers
        """
        for passenger in self.passengers:
            passenger.block = -passenger.id

    def f2b(self):
        for passenger in self.passengers:
            passenger.block = passenger.id

    def wma(self):
        """
        Set blockes to window-middle-aise
        Divides into 3 blockes
        """
        for passenger in self.passengers:
            if passenger.seat[1] in [0,6]:
                passenger.block = 1
            elif passenger.seat[1] in [1,5]:
                passenger.block = 2
            else:
                passenger.block = 3

    def wma_b2f(self):
        """
        Set blockes to window-middle-aise and back to front
        Divides into 9 blockes
        """
        for passenger in self.passengers:
            if self.rows*2/3 < passenger.seat[0]:
                if passenger.seat[1] in [0,6]:
                        passenger.block = (1,-passenger.id)
                elif passenger.seat[1] in [1,5]:
                    passenger.block = (2,-passenger.id)
                else:
                    passenger.block = (3,-passenger.id)
            elif self.rows/3 < passenger.seat[0] <= 2*self.rows/3:
                if passenger.seat[1] in [0,6]:
                        passenger.block = (4,-passenger.id)
                elif passenger.seat[1] in [1,5]:
                    passenger.block = (5,-passenger.id)
                else:
                    passenger.block = (6,-passenger.id)
            else:
                if passenger.seat[1] in [0,6]:
                        passenger.block = (7,-passenger.id)
                elif passenger.seat[1] in [1,5]:
                    passenger.block = (8,-passenger.id)
                else:
                    passenger.block = (9,-passenger.id)

    def steffen_perfect(self):
        row = self.rows
        for passenger in self.passengers:
            if passenger.seat[1] == 0:
                passenger.block = (1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

            elif passenger.seat[1] == 6:
                passenger.block = row/2 +(1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

            elif passenger.seat[1] == 1:
                passenger.block = 2*row + (1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

            elif passenger.seat[1] == 5:
                passenger.block = 5*row/2 +(1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

            elif passenger.seat[1] == 2:
                passenger.block = 4*row + (1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

            else:
                passenger.block = 9*row/2 +(1-(row-passenger.seat[0])%2)*row + (row-passenger.seat[0])/2

    def steffen_modified(self):
        for passenger in self.passengers:
            if passenger.seat[1] in [0,1,2]:
                if (self.rows - passenger.seat[0])%2:
                    passenger.block = (1, -passenger.id)
                else:
                    passenger.block = (3, -passenger.id)
            else:
                if (self.rows - passenger.seat[0])%2:
                    passenger.block = (2, -passenger.id)
                else:
                    passenger.block = (4, -passenger.id)
