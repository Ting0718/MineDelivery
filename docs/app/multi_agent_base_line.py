import queue
import json
import logging
from collections import defaultdict, deque
import sys
import os
import random
import sys
import time
import json
import math
import errno
from collections import defaultdict, deque
from timeit import default_timer as timer
from priority_dict import priorityDictionary as PQ

Best_Testing = False
Tracing = True

class House(object):
    def __init__(self, id, state, location):
        self.id = id
        self.state = state
        self.orderTime = []
        self.location = location
        self.hasAgentAssigned = False
    
    def __lt__(self, house):
        return False

    def __gt__(self, house):
        return False

    
class world(object):

    def __init__(self, alpha=0.3, gamma=0.8, n=1, agent_host=[]):
        self.epsilon = 0.35
        self.q_table = [{},{}]
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.Locations = [(1,0),(2,0),(0,2),(0,3),(8,6),(8,7),(6,6),(6,5)]
        # self.Locations = [(1, 0), (0, 2), (3, 2), (2, 3)]
        self.agent_face = [1,1]
        self.agent_host = agent_host
        # self.canvas = canvas	plan to send
        # self.root = root
        self.Agent_Location = [(0,0),(0,0)]
        self.row = 4
        self.col = 4
        self.initialize()
    
    def initialize(self):
        self.House = []
        self.EventQueue = queue.PriorityQueue()
        self.Clock = 0.0
        self.epsilon = 0.35
        self.total_waiting = 0
        self.Agent_Location = [(0,0),(0,0)]
        self.Agent_Action = [[],[]]

        #Set the order time and houses
        for i in range(len(self.Locations)):
            self.House.append(House(i, False, self.Locations[i]))

        # self.set_order(3, 30, 7, self.House[0])
        # self.set_order(2, 30, 4, self.House[1])
        # self.set_order(3, 30, 7, self.House[2])
        # self.set_order(12, 30, 8, self.House[3])
        # self.set_order(9, 30, 6, self.House[4])
        # self.set_order(8, 30, 8, self.House[5])
        # self.set_order(13, 30, 5, self.House[6])
        # self.set_order(2, 4, 2, self.House[0])
        # self.set_order(2, 4, 2, self.House[1])

        self.set_order(0, 30, 7, self.House[0])
        self.set_order(2, 30, 4, self.House[1])
        self.set_order(3, 30, 7, self.House[2])
        self.set_order(12, 30, 8, self.House[3])

        self.set_order(0, 30, 7, self.House[4])
        self.set_order(2, 30, 4, self.House[5])
        self.set_order(3, 30, 7, self.House[6])
        self.set_order(12, 30, 8, self.House[7])

    
    def set_order(self, start,end, interval, house):
        time = start
        while time <= end:
            self.EventQueue.put((time, house))
            time += interval

    def move_north(self,agent):
        # ui需要
        # self.face_to(agent,1)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movenorth 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0],self.Agent_Location[0][1]-1),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0],self.Agent_Location[1][1]-1)]
    

    def move_south(self,agent):
        # UI需要
        # self.face_to(agent,3)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movesouth 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0],self.Agent_Location[0][1]+1),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0],self.Agent_Location[1][1]+1)]

    def move_east(self, agent):
        # UI需要
        # self.face_to(agent,2)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0]+1,self.Agent_Location[0][1]),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0]+1,self.Agent_Location[1][1])]
                
    def move_west(self, agent):
        # UI需要
        # self.face_to(agent,4)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0]-1,self.Agent_Location[0][1]),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0]-1,self.Agent_Location[1][1])]

    def get_path(self, source, dest):
        action = []
        x_axis = dest[0]-source[0]
        y_axis = dest[1]-source[1]

        if x_axis>0:
            for i in range(x_axis):
                action.append('E')
        elif x_axis<0:
            for i in range(-x_axis):
                action.append('W')

        if y_axis>0:
            for i in range(y_axis):
                action.append('S')
        elif y_axis<0:
            for i in range(-y_axis):
                action.append('N')

        return action
        

    def extract_action_list_from_path(self, path_list):
        
        action_trans = {'N':self.move_north,'S':self.move_south,'E':self.move_east,'W':self.move_west}
        alist = []
        for i in path_list:
            alist.append(action_trans[i])
        return alist

    
    def doTheAction(self, agent):
        action = self.Agent_Action[agent].pop(0)
        if action != None:
            action = action(agent)
        if Tracing:
            print("agent",agent, "now is on",self.Agent_Location[agent])


        for i in self.House:
            if i.location == self.Agent_Location[agent] and i.state == True:
                if Tracing:
                    print("************Agent", agent, "Change the house", i.id, "at time", self.Clock)
                i.state = False
                i.hasAgentAssigned = False
                # self.deliever_food(agent)
                total = 0
                for order in i.orderTime:
                    total += self.Clock - order
                i.orderTime = []
                self.total_waiting += (total)
                return 1000 - (total)
        return  0

    def set_toDoAction(self,dest,agent):
        if Tracing:
            print("\t\t\t\tplan to send",agent, "to", dest)
        if dest == self.Agent_Location[agent]:
            self.Agent_Action[agent] = [None]
            if Tracing:
                print("\t\t\t\tWait")
            return

        path = self.get_path(self.Agent_Location[agent], dest)
        extract_action_list = self.extract_action_list_from_path(path)   
        if Tracing:
            print("\t\t\t\t",path,sep="")
            print("\t\t\t\t^^^^^^^^^^^")

        self.Agent_Action[agent] = extract_action_list
        return         

    def findDistance(self, agentLoc, targetLoc):
        return abs(agentLoc[0] -  targetLoc[0]) + abs(agentLoc[1] - targetLoc[1]) ** 2 
    
    def chooseHouseToMove(self, agent):
        if agent == 0: # choose the nearest location
            shortest_distance = 82
            selectHouse = None
            for house in self.House:
                if house.state == True and not house.hasAgentAssigned and self.findDistance(self.Agent_Location[agent], house.location) < shortest_distance:
                    shortest_distance = self.findDistance(self.Agent_Location[agent], house.location)
                    selectHouse = house

            if selectHouse == None:
                return self.Agent_Location[agent]
            selectHouse.hasAgentAssigned = True
            return selectHouse.location

        else: # choose the nearest order time

            biggestTime = self.Clock + 1
            selectHouse = None

            for house in self.House:
                if house.state == True and not house.hasAgentAssigned and house.orderTime[0] < biggestTime:
                    shortest_distance = self.findDistance(self.Agent_Location[agent], house.location)
                    selectHouse = house

            if selectHouse == None:
                return self.Agent_Location[agent]
            selectHouse.hasAgentAssigned = True
            return selectHouse.location

    def run(self):
        while (self.EventQueue.qsize() != 0 or [i.state for i in self.House] != [False for i in self.House]):
            count = 0
            if self.EventQueue.qsize() != 0:
                for i in self.EventQueue.queue:
                    if i[0] == self.Clock:
                        count += 1
                for i in range(count):
                    event_time, house = self.EventQueue.get()
                    house.state = True  
                    house.orderTime.append(event_time)
            
            for agent in [0, 1]:
                chooseHouse = None
                if self.Agent_Action[agent] == []: # 注意： 我们思考时间也算一秒，比如当agent 1第四秒在(1,0)并且有个房子也在这个时候更新了，我们会选取这个房子但是不会do action，所以思考也算一秒
                    chooseHouse = self.chooseHouseToMove(agent)

                    if chooseHouse != None:
                        self.set_toDoAction(chooseHouse, agent) # will do the action and update the action list of the agent
                
                else:
                    self.doTheAction(agent)
            
                # if self.Clock == 2:
                #     print("agent", agent, "is assign to", chooseHouse)
            self.Clock += 1

            # if (self.Clock >= 3):
            #     break
            
            # print("here")

        for agent in [0,1]:
            print("agent", agent, "is at", self.Agent_Location[agent])

        print("the total waiting time is", self.total_waiting)
    
a = world()
a.initialize()
a.run()



