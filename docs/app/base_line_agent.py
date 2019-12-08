import queue

class House(object):
    def __init__(self, id, state, location):
        self.id = id
        self.state = state
        self.orderTime = 0
        self.waitTime = 0
        self.location = location

class Agent(object):
    def __init__(self):
        self.currentLocation = (0, 0)

class baseLineWorld(object):
    def __init__(self, alpha=0.3, gamma=0.8, n=1):
        self.n = n
        self.EventQueue = queue.PriorityQueue()
        self.House = []
        self.Clock = 0.0
        # self.Locations = [(1,0),(2,2),(5,6),(1,2),(3,3)]
        self.Locations = [(1,1), (3,1), (0,1)]
        self.Col = 4
        self.Row = 4
        self.Agent_Location = (0,0)
        self.initialize()

    def initialize(self):
        self.House = []
        self.EventQueue = queue.PriorityQueue()
        self.Clock = 0.0

        self.Agent_Location = (0,0)

        for i in range(len(self.Locations)):
            self.House.append(House(i, False, self.Locations[i]))
        self.EventQueue.put((2, self.House[0]))
        self.EventQueue.put((3, self.House[1]))
        self.EventQueue.put((5, self.House[2]))
    
    # will change the state of house if it is time to have order
    def updateHouseOrder(self):
        if self.EventQueue.qsize() != 0:
            for i in self.EventQueue.queue:
                if i[0] <= self.Clock:
                    eventTime, house = self.EventQueue.get()
                    house.state = True
                    house.orderTime = eventTime

    # will choose the most nearest house to move and update the time
    def chooseHouseToMove(self):
        # because our map is 4 * 4 and the max path length is 4+4 = 8
        self.shortest_path = 9
        chooseHouse = None

        for house in self.House:
            if house.state and (abs(self.Agent_Location[0] - house.location[0]) + abs(self.Agent_Location[1] - house.location[1])) <= self.shortest_path:
                chooseHouse = house
                self.shortest_path = abs(self.Agent_Location[0] - house.location[0]) + abs(self.Agent_Location[1] - house.location[1])

        return chooseHouse
    
    def moveToHouse(self, chooseHouse):
        chooseHouse.state = False
        self.Clock += abs(self.Agent_Location[0] - chooseHouse.location[0]) + abs(self.Agent_Location[1] - chooseHouse.location[1])
        chooseHouse.waitTime = self.Clock - chooseHouse.orderTime
        self.Agent_Location = chooseHouse.location
        self.chooseHouse = False

    def findOrderShortestTime(self):
        shortestTime = self.EventQueue.queue[0][0]

        for i in range(len(self.EventQueue.queue)):
            eventTime = self.EventQueue.queue[i][0]

            if eventTime < shortestTime:
                eventTime = shortestTime
        return shortestTime
    

    def run(self):    

        while (self.EventQueue.qsize() != 0 and [i.state for i in self.House] != [False, False, False, False, False]):
            self.updateHouseOrder()
            chooseHouse = self.chooseHouseToMove()

            # because there is a possible when the current clock doesn't have a correspoind order to run
            if chooseHouse == None:
                self.Clock = self.findOrderShortestTime()
            else:
                self.moveToHouse(chooseHouse)
            
        totalWaitTime = 0

        for house in self.House:
            totalWaitTime += house.waitTime

        return totalWaitTime

baseLine = baseLineWorld()
print("total waiting time is ", baseLine.run())
