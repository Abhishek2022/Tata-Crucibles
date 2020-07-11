# Flatten a 2-d list
flatten = lambda lst: [elem for row in lst for elem in row]

class TicketBlock(object):
    """ Set the block number which will be printed on each passenger's ticket"""

    def __init__(self, rows, passengers):
        self.rows = rows
        self.passengers = passengers

    def set_block(name):
        if name == 'wma':
            self.wma()
        elif name == 'wma_b2f':
            self.wma_b2f()

    def wma(self):
        """
        Set blockes to window-middle-aise
        Divides into 3 blockes
        """
        for passenger in flatten(self.passengers):
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
        for passenger in flatten(self.passengers):
            if self.rows*2/3 < passenger.seat[0]:
                if passenger.seat[1] in [0,6]:
                        passenger.block = 1
                elif passenger.seat[1] in [1,5]:
                    passenger.block = 2
                else:
                    passenger.block = 3
            elif self.rows/3 < passenger.seat[0] <= 2*self.rows/3:
                if passenger.seat[1] in [0,6]:
                        passenger.block = 4
                elif passenger.seat[1] in [1,5]:
                    passenger.block = 5
                else:
                    passenger.block = 6
            else:
                if passenger.seat[1] in [0,6]:
                        passenger.block = 7
                elif passenger.seat[1] in [1,5]:
                    passenger.block = 8
                else:
                    passenger.block = 9
