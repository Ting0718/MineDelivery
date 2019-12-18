import queue
import MalmoPython
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
import tkinter as tk

Best_Testing = False
Tracing = False

class House(object):
    def __init__(self, id, state, location):
        self.id = id
        self.state = state
        self.orderTime = []
        self.location = location
    
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
        self.Locations = [(1,0),(3,2),(1,2),(6,4),(6,7),(6,6),(7,5)]
        # self.Locations = [(1,0),(2,0),(0,2),(0,3),(8,6),(8,7),(6,6),(6,5)]
        self.Col = 4
        self.Row = 4
        self.agent_face = [1,1]
        self.agent_host = agent_host
        # self.canvas = canvas
        # self.root = root
        self.Agent_Location = [(0,0),(0,0)]
        self.initialize()
    
    def initialize(self):
        self.House = []
        self.EventQueue = queue.PriorityQueue()
        self.Clock = 0.0
        # self.epsilon = 0.2
        self.total_waiting = 0
        self.Agent_Action = [[],[]]
        

        # print("&&&&&&&&&&&&&&&&&&")
        # print("Agent 1:\n")
        #print(self.Agent_Location[0])
        path1 = self.get_path(self.Agent_Location[0], (0,0))
        extract_action_list = self.extract_action_list_from_path(path1)

        for f in extract_action_list:
            f(0)
            time.sleep(0)
            #print(self.Agent_Location[0])

        # print("Agent 2:\n")
        # print(self.Agent_Location[1])
        path2 = self.get_path(self.Agent_Location[1], (0,0))
        extract_action_list = self.extract_action_list_from_path(path2)
        
        for f in extract_action_list:
            f(1)
            time.sleep(0)
            #print(self.Agent_Location[1])

        assert self.Agent_Location == [(0,0),(0,0)]

        #Set the order time and houses
        for i in range(len(self.Locations)):
            self.House.append(House(i, False, self.Locations[i]))

        self.set_order(3, 30, 7, self.House[0])
        self.set_order(2, 30, 4, self.House[1])
        self.set_order(3, 30, 7, self.House[2])
        self.set_order(12, 30, 8, self.House[3])
        self.set_order(9, 30, 6, self.House[4])
        self.set_order(8, 30, 8, self.House[5])
        self.set_order(13, 30, 5, self.House[6])
        # self.set_order(0, 30, 7, self.House[0])
        # self.set_order(2, 30, 4, self.House[1])
        # self.set_order(3, 30, 7, self.House[2])
        # self.set_order(12, 30, 8, self.House[3])

        # self.set_order(0, 30, 7, self.House[4])
        # self.set_order(2, 30, 4, self.House[5])
        # self.set_order(3, 30, 7, self.House[6])
        # self.set_order(12, 30, 8, self.House[7])

    
    def set_order(self, start,end, interval, house):
        time = start
        while time <= end:
            self.EventQueue.put((time, house))
            time += interval


    def execute_actions(self, agent_host, action):
        # agent_host.sendCommand(action)
        # time.sleep(0)
        # world_state = agent_host.getWorldState()
        # for error in world_state.errors:
        #     print("Error:", error.text)
        return

    def face_to(self,agent,face):
        # if self.agent_face[agent]>face:
        #     for i in range(self.agent_face[agent]-face):
        #         self.execute_actions(self.agent_host[agent],"turn -0.8")
        #     time.sleep(0.8)
        #     self.agent_face[agent] = face
        # elif self.agent_face[agent]<face:
        #     for i in range(face-self.agent_face[agent]):
        #         self.execute_actions(self.agent_host[agent],"turn 0.8")
        #     time.sleep(0.8)
        #     self.agent_face[agent] = face
        return

    def move_north(self,agent):
        # self.face_to(agent,1)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movenorth 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0],self.Agent_Location[0][1]-1),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0],self.Agent_Location[1][1]-1)]
    

    def move_south(self,agent):
        # self.face_to(agent,3)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movesouth 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0],self.Agent_Location[0][1]+1),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0],self.Agent_Location[1][1]+1)]

    def move_east(self, agent):
        # self.face_to(agent,2)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0]+1,self.Agent_Location[0][1]),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0]+1,self.Agent_Location[1][1])]
                
    def move_west(self, agent):
        # self.face_to(agent,4)
        # for i in range(7):
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        #     time.sleep(0)
        if agent == 0:
            self.Agent_Location = [(self.Agent_Location[0][0]-1,self.Agent_Location[0][1]),self.Agent_Location[1]]
        else:
            self.Agent_Location  = [self.Agent_Location[0], (self.Agent_Location[1][0]-1,self.Agent_Location[1][1])]

    def deliever_food(self, agent):
        # if agent == 0:
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     self.execute_actions(self.agent_host[agent],'movenorth 1')
        #     time.sleep(0)
        #     loc = self.Agent_Location[agent]
        #     self.execute_actions(self.agent_host[0],"chat /fill "+str(loc[0]*7+2)+" 8 "+str(loc[1]*7+2)+" "+str(loc[0]*7+4)+" 8 "+str(loc[1]*7+3)+" minecraft:air")
        #     self.execute_actions(self.agent_host[agent],'movesouth 1')
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        # else:
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     self.execute_actions(self.agent_host[agent],'moveeast 1')
        #     time.sleep(0)
        #     loc = self.Agent_Location[agent]
        #     self.execute_actions(self.agent_host[0],"chat /fill "+str(loc[0]*7+2)+" 8 "+str(loc[1]*7+2)+" "+str(loc[0]*7+4)+" 8 "+str(loc[1]*7+3)+" minecraft:air")
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        #     self.execute_actions(self.agent_host[agent],'movewest 1')
        return 

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

    
    def act(self, agent):
        if self.Agent_Action[agent][0] == None:
            self.Agent_Action[agent].pop(0)
            if Tracing:
                print("Stay")
        else:
            self.Agent_Action[agent][0](agent)
            self.Agent_Action[agent].pop(0)
            if Tracing:
                print("agent",agent, "now is on",self.Agent_Location[agent])


        for i in self.House:
            if i.location == self.Agent_Location[agent] and i.state == True:
                if Tracing:
                    print("************Agent", agent, "Change the house", i.id)
                i.state = False
                self.deliever_food(agent)
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


    def get_possible_actions(self,agent):
        return [i.location for i in self.House]
        

    def get_curr_state(self):
        return self.Agent_Location.copy() + [i for i in self.House] 


    def choose_action(self, curr_state, possible_actions, eps,agent):
        if curr_state not in self.q_table[agent]:
            self.q_table[agent][curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[agent][curr_state]:
                self.q_table[agent][curr_state][action] = 0

        if len(possible_actions) == 0:
            return None

        actionProb = random.uniform(0.0, 1.0)
        # using the random move
        if actionProb <= eps:
            # actionIndex = random.randint(0, len(possible_actions) - 1)
            return possible_actions[random.randint(0, len(possible_actions) - 1)]
        # using greedy action
        else:
            maxQValue = min(self.q_table[agent][curr_state].values()) - 1
            actionList = []
            for (action, qValue) in self.q_table[agent][curr_state].items():
                if qValue > maxQValue:
                    actionList.clear()
                    maxQValue = qValue
                    actionList.append(action)

                elif qValue == maxQValue:
                    actionList.append(action)
            return actionList[random.randint(0, len(actionList) - 1)]

    def transferCurrState(self, state):
        # transfer the state into (num)...
        copy_state = []
        for i in state:
            if type(i) == House:
                if i.state == True:
                    copy_state.append(i.location)
            else:
                copy_state.append(i)

        return tuple(copy_state)

    def best_policy(self):
        returnAction = {"0":[],"1":[]}

        s0 = self.transferCurrState(self.get_curr_state())
        possible_actions1= self.get_possible_actions(0)
        possible_actions2= self.get_possible_actions(1)
        agent1_a0 = self.choose_action(s0, possible_actions1, -1, 0)
        agent2_a0 = self.choose_action(s0, possible_actions2, -1, 1)

        self.set_toDoAction(agent1_a0,0)
        self.set_toDoAction(agent2_a0,1)

        returnAction["0"].append(agent1_a0)
        returnAction["1"].append(agent2_a0)

        done_update = False
        while not done_update:

            count = 0
            if self.EventQueue.qsize() != 0:
                for i in self.EventQueue.queue:
                    if i[0] == self.Clock:
                        count += 1
                for i in range(count):
                    event_time, house = self.EventQueue.get()
                    house.state = True  
                    house.orderTime.append(event_time)
                    loc = house.location 
                    self.execute_actions(self.agent_host[0],"chat /fill "+str(loc[0]*7+2)+" 8 "+str(loc[1]*7+2)+" "+str(loc[0]*7+4)+" 8 "+str(loc[1]*7+3)+" minecraft:gold_block")

            if Tracing:
                print("----------------------------------------------------")
                print("Now",self.Clock)
                print("Houses:")
                for i in self.House:
                    print("|",i.location,i.state)

            for agent in [0,1]:
                current_r = self.act(agent)

                if self.Agent_Action[agent] == []:
                    if (self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False for i in self.House]):
                        if agent == 0:
                            returnAction["1"].pop(-1)
                        return returnAction
                    else:
                        s = self.transferCurrState(self.get_curr_state())
                        possible_actions = self.get_possible_actions(agent)
                        next_a = self.choose_action(s, possible_actions, -1,agent)
                        self.set_toDoAction(next_a,agent)
                        returnAction[str(agent)].append(next_a)
            self.Clock += 1
                    
        return returnAction

    def update_q_table(self, tau, S, A, R, T,agent):
        
        # curr_s = S.popleft()
        # curr_a = A.popleft()
        # curr_r = R.popleft()

        # G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        # if tau + self.n < T:
        #     G += self.gamma ** self.n * self.q_table[agent][S[-1]][A[-1]]

        # old_q = self.q_table[agent][curr_s][curr_a]
        # self.q_table[agent][curr_s][curr_a] = old_q + self.alpha * (G - old_q)
        
        curr_s = S.popleft()
        curr_a = A.popleft()
        R.popleft()
        if len(S) != 0:
            nextMaxReward = max(self.q_table[agent][S[0]].values())
        else:
            nextMaxReward = 0
        if len(S) != 0:
            self.q_table[agent][curr_s][curr_a] = self.q_table[agent][curr_s][curr_a] + self.alpha * (R[0] + self.gamma * nextMaxReward) 
        else:
            self.q_table[agent][curr_s][curr_a] = self.q_table[agent][curr_s][curr_a] + self.alpha * (self.gamma * nextMaxReward) 

    # def update_q_table(self, tau, S, A, R, T,agent):
        
    #     curr_s = S.popleft()
    #     curr_a = A.popleft()
    #     R.popleft()
    #     nextMaxReward = max(self.q_table[agent][S[0]].values())
    #     self.q_table[agent][curr_s][curr_a] = self.q_table[agent][curr_s][curr_a] + self.alpha * (R[0] + self.gamma * nextMaxReward - self.q_table[agent][curr_s][curr_a]) 

    def run(self):
        S = [deque(), deque()]
        A = [deque(), deque()]
        R = [deque(), deque()]

        present_reward = 0
        done_update = False
        while not done_update:

            s0 = self.transferCurrState(self.get_curr_state())
            possible_actions1= self.get_possible_actions(0)
            possible_actions2= self.get_possible_actions(1)
            agent1_a0 = self.choose_action(s0, possible_actions1, self.epsilon, 0)
            agent2_a0 = self.choose_action(s0, possible_actions2, self.epsilon, 1)

            self.set_toDoAction(agent1_a0,0)
            self.set_toDoAction(agent2_a0,1)

            S[0].append(s0)
            S[1].append(s0)
            A[0].append(agent1_a0)
            A[1].append(agent2_a0)
            R[0].append(0)
            R[1].append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):

                time.sleep(0.1)

                # eventQueue update
                count = 0
                if self.EventQueue.qsize() != 0:
                    for i in self.EventQueue.queue:
                        if i[0] == self.Clock:
                            count += 1
                    for i in range(count):
                        event_time, house = self.EventQueue.get()
                        house.state = True  
                        house.orderTime.append(event_time)
                        loc = house.location 
                        self.execute_actions(self.agent_host[0],"chat /fill "+str(loc[0]*7+2)+" 8 "+str(loc[1]*7+2)+" "+str(loc[0]*7+4)+" 8 "+str(loc[1]*7+3)+" minecraft:gold_block")

                 #-----------------------
                if Tracing:

                    print("----------------------------------------------------")
                    print("Now",self.Clock)
                    print("Houses:")
                    for i in self.House:
                        print("|",i.location,i.state)
                #-----------------------

                if t < T:
                #和之前是一样的逻辑结构，只不过现在有两个agent
                    for agent in [0,1]:
                        current_r = self.act(agent)

                        if self.Agent_Action[agent] == []:#只有当到达了某一个房子才需要计算 reward， update q-table， choose action
                            R[agent].append(current_r)
                            
                            if (self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False for i in self.House]):
                                if Tracing:
                                    print("**********************")
                                    print("End")
                                    print("**********************")
                                T = t + 1
                                #S[agent].append('Term State')
                                present_reward = current_r
                                # print("Reward:", present_reward)
                            else:
                                s = self.transferCurrState(self.get_curr_state())
                                S[agent].append(s)
                                possible_actions = self.get_possible_actions(agent)
                                next_a = self.choose_action(s, possible_actions, self.epsilon,agent)
                                self.set_toDoAction(next_a,agent)
                                A[agent].append(next_a)
            
                            # 最后在update我们的q_table
                            tau = t - self.n + 1
                            if tau >= 0:
                                self.update_q_table(tau, S[agent], A[agent], R[agent], T, agent)
                            if tau == T - 1:
                                while len(S[agent]) > 1:
                                    tau = tau + 1
                                    self.update_q_table(tau, S[agent], A[agent], R[agent], T, agent)
                                done_update = True
                                return
                    self.Clock += 1

    

    def drawQ( self, curr_x=None, curr_y=None ):
        if self.canvas is None or self.root is None:
            return
        self.canvas.delete("all")
        action_inset = 0.1
        action_radius = 0.1
        curr_radius = 0.2
        action_positions = [ ( 0.5, 1-action_inset ), ( 0.5, action_inset ), ( 1-action_inset, 0.5 ), ( action_inset, 0.5 ) ]
        for x in range(world_x):
            for y in range(world_y):
                self.canvas.create_rectangle( (world_x-1-x)*scale, (world_y-1-y)*scale, (world_x-1-x+1)*scale, (world_y-1-y+1)*scale, outline="#fff", fill="#000")
                for i in self.House:
                    if i.state == True:
                        i_x = i.location % 4
                        i_y = i.location // 4
                        # print(i.location, i_x, i_y)
                        self.canvas.create_rectangle((world_x - 1 - i_x) * scale, (world_y - 1 - i_y) * scale,
                                                     (world_x - 1 - i_x + 1) * scale, (world_y - 1 - i_y + 1) * scale,
                                                     outline="#fff", fill="#ff0")

        root.update()



def get_total_map(x,y):
    return 'DrawCuboid x1="0"  y1="4" z1="0"  x2="'+str(x*7-1)+'" y2="4" z2="'+str(y*7-1)+'" type="stone" '


def get_house_xml(x,y):
    return '\n\t\t<DrawCuboid x1="'+str(x*7+2)+'"  y1="5" z1="'+str(y*7+2)+'"  x2="'+str(x*7+4)+'" y2="7" z2="'+str(y*7+3)+'" type="brick_block" />\n' \
            '<DrawCuboid x1="'+str(x*7+3)+'"  y1="5" z1="'+str(y*7+4)+'"  x2="'+str(x*7+3)+'" y2="6" z2="'+str(y*7+4)+'" face="SOUTH" type="dark_oak_door" />\n'


def get_houses(locations):
    xml = ''
    for i in locations:
        xml += get_house_xml(i[0],i[1])
    return xml


def safeStartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            # Attempt start:
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, role, expId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error: ", str(e))
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")


def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow a two minute timeout.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    if time.time() - start_time >= time_out:
        print("Timed out while waiting for mission to start - bailing.")
        exit(1)
    print()
    print("Mission has started.")



# -- set up two agent hosts --
agent_host = MalmoPython.AgentHost()
agent_host1 = MalmoPython.AgentHost()

a = world(agent_host = [agent_host,agent_host1])


try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

if agent_host.receivedArgument("test"):
    num_repeats = 1
else:
    num_repeats = 426

mission_xml = '''
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <About>
    <Summary>MineDelivery</Summary>
  </About>

  <ServerSection>
    <ServerInitialConditions>
        <Time><StartTime>1000</StartTime></Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator generatorString="3;7,2*3,2,1:2;1;village"/>
      <DrawingDecorator>
        <!-- coordinates for cuboid are inclusive -->

        <'''+get_total_map(9,9)+'''/>

'''+get_houses([(1,0),(3,2),(1,2),(6,4),(6,7),(6,6),(7,5)])+'''

      </DrawingDecorator>
      <ServerQuitFromTimeUp timeLimitMs="1000000000"/>
      <ServerQuitWhenAnyAgentFinishes/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Cristina</Name>
    <AgentStart>
      <Placement x="0.5" y="5" z="6.5" pitch="30" yaw="180"/>
    </AgentStart>
    <AgentHandlers>
      <!-- <AgentQuitFromTouchingBlockType>
          <Block type="cobblestone"/>
      </AgentQuitFromTouchingBlockType> -->
      <ObservationFromGrid>
          <Grid name="floorAll">
            <min x="0" y="5" z="0"/>
            <max x="15" y="5" z="15"/>
          </Grid>
      </ObservationFromGrid>
      <ContinuousMovementCommands/>
      <DiscreteMovementCommands/>
      <ObservationFromFullStats/>
      <!--<RewardForTouchingBlockType>-->
        <!--<Block reward="100.0" type="lapis_block" behaviour="onceOnly"/>-->
      <!--</RewardForTouchingBlockType>-->
      <!--<RewardForSendingCommand reward="-1" />-->
      <!-- <AgentQuitFromTouchingBlockType>
          <Block type="lapis_block" />
      </AgentQuitFromTouchingBlockType> -->
    </AgentHandlers>
  </AgentSection>
  
  <AgentSection mode="Survival">
    <Name>Cristina1</Name>
    <AgentStart>
      <Placement x="1.5" y="5" z="5.5" pitch="30" yaw="180"/>
    </AgentStart>
    <AgentHandlers>
      <!-- <AgentQuitFromTouchingBlockType>
          <Block type="cobblestone"/>
      </AgentQuitFromTouchingBlockType> -->
      <ObservationFromGrid>
          <Grid name="floorAll">
            <min x="0" y="5" z="0"/>
            <max x="15" y="5" z="15"/>
          </Grid>
      </ObservationFromGrid>
      <ContinuousMovementCommands/>
      <DiscreteMovementCommands/>
      <ObservationFromFullStats/>
      <!--<RewardForTouchingBlockType>-->
        <!--<Block reward="100.0" type="lapis_block" behaviour="onceOnly"/>-->
      <!--</RewardForTouchingBlockType>-->
      <!--<RewardForSendingCommand reward="-1" />-->
      <!-- <AgentQuitFromTouchingBlockType>
          <Block type="lapis_block" />
      </AgentQuitFromTouchingBlockType> -->
    </AgentHandlers>
  </AgentSection>

</Mission>
'''


my_mission = MalmoPython.MissionSpec(mission_xml, True)
# my_mission_record = MalmoPython.MissionRecordSpec()
agent_mission_record = MalmoPython.MissionRecordSpec()
agent1_mission_record = MalmoPython.MissionRecordSpec()
my_mission.requestVideo(800, 500)
my_mission.setViewpoint(1)
my_mission.allowAllChatCommands()
my_mission.allowAllContinuousMovementCommands()

# Attempt to start a mission:

# Making a ClientPool
client_pool = MalmoPython.ClientPool()
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10001))

max_retries = 3

for retry in range(max_retries):
    try:
        # agent_host.startMission(my_mission, my_mission_record)
        safeStartMission(agent_host, my_mission, client_pool, agent_mission_record, 0, 'Test')
        safeStartMission(agent_host1, my_mission, client_pool, agent1_mission_record, 1, 'Test')
        # safeWaitForStart([agent_host, agent_host1])
        # agent_host.startMission(my_mission, client_pool, my_mission_record, 0, 'Test')
        # agent_host1.startMission(my_mission, client_pool, my_mission_record, 1, 'Test')
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission", ":", e)
            exit(1)
        else:
            time.sleep(0.1)

print("Waiting for the mission to start", end=' ')
print()


file = open("output.txt","w")

for i in range(num_repeats):
    if i > 100:
        a.epsilon = 0.2
    if i % 5 == 0 and i != 0:
        print("---- this is the best policy")
        a.initialize()
        po = a.best_policy()
        size = 0
        for self_q_table in a.q_table:
            for q_table_size in self_q_table.keys():
                size += len(self_q_table[q_table_size].values())
        print("the size of the q table is", size)
        print("Agent 1      :",po["0"])
        print("Agent 2      :",po["1"])
        print(a.total_waiting)
        file.write(str(a.total_waiting)+"\n")
        

       

    #print("this is the q table", str(a.q_table))

    print("Waiting for the mission to start ", end=' ')
    time.sleep(3)
    agent_state, agent1_state = agent_host.getWorldState(), agent_host1.getWorldState()
    while not (agent_state.has_mission_begun and agent1_state.has_mission_begun):
        print(".", end="")
        time.sleep(0.1)
        agent_state, agent1_state = agent_host.getWorldState(), agent_host1.getWorldState()

        for error in agent_state.errors:
            print("Error:", error.text)
    print()
    print("Mission", (i + 1), "running.")
    print()
    
    a.initialize()
    a.run()

file.close()