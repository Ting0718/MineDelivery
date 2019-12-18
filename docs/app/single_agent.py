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

actionL = ['right', 'down', 'down', 'up', 'down', 'up']
count = -1


# -- set up the python-side drawing -- #
# scale = 40
# world_x = 4
# world_y = 4
# root = tk.Tk()
# root.wm_title("Q-table")
# canvas = tk.Canvas(root, width=world_x*scale, height=world_y*scale, borderwidth=0, highlightthickness=0, bg="black")
# canvas.grid()
# root.update()


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


class Agent(object):
    def __init__(self):
        self.currentLocation = (0, 0)


class world(object):

    def __init__(self, alpha=0.3, gamma=0.8, n=1, agent_host=[]):
        self.epsilon = 0.2
        self.q_table = {}
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.EventQueue = queue.PriorityQueue()
        self.House = []
        self.Clock = 0.0
        self.Locations = [(1, 0), (2, 2), (5, 6), (1, 2), (3, 3)]
        self.Col = 4
        self.Row = 4
        self.Agent_Location = (0, 0)
        self.agent_host = agent_host
        self.agent_face = 1
        # self.canvas = canvas
        # self.root = root
        self.initialize()

    def execute_actions(self, agent_host, action):
        return
        time.sleep(0.01)
        agent_host.sendCommand(action)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)

    def face_to(self, face):
        if self.agent_face > face:
            for i in range(self.agent_face - face):
                self.execute_actions(agent_host, "turn -0.0000000000000000000001")
                time.sleep(1)
            self.agent_face = face
        elif self.agent_face < face:
            for i in range(face - self.agent_face):
                self.execute_actions(agent_host, "turn 0.3")
                time.sleep(1)

            self.agent_face = face

    def move_north(self, agent_host):
        # self.face_to(1)
        for i in range(5):
            self.execute_actions(agent_host, 'movenorth 1')

    def move_south(self, agent_host):
        # self.face_to(3)
        for i in range(5):
            self.execute_actions(agent_host, 'movesouth 1')

    def move_east(self, agent_host):
        # self.face_to(2)
        for i in range(5):
            self.execute_actions(agent_host, 'moveeast 1')

    def move_west(self, agent_host):
        # self.face_to(4)
        for i in range(5):
            self.execute_actions(agent_host, 'movewest 1')

    def deliever_food(self, agent_host):
        self.execute_actions(agent_host, 'moveeast 1')
        self.execute_actions(agent_host, 'moveeast 1')
        time.sleep(2)
        loc = self.Agent_Location
        self.execute_actions(self.agent_host[0],
                             "chat /fill " + str(loc[0] * 5 + 1) + " 8 " + str(loc[1] * 5 + 1) + " " + str(
                                 loc[0] * 5 + 3) + " 8 " + str(loc[1] * 5 + 2) + " minecraft:air")
        self.execute_actions(agent_host, 'movewest 1')
        self.execute_actions(agent_host, 'movewest 1')

    def get_path(self, source, dest):
        action = []
        # print("**************")
        # print(source, dest)
        x_axis = dest[0] - source[0]
        y_axis = dest[1] - source[1]

        if x_axis > 0:
            for i in range(x_axis):
                action.append('E')
        elif x_axis < 0:
            for i in range(-x_axis):
                action.append('W')

        if y_axis > 0:
            for i in range(y_axis):
                action.append('S')
        elif y_axis < 0:
            for i in range(-y_axis):
                action.append('N')

        return action

    def extract_action_list_from_path(self, path_list):

        action_trans = {'N': self.move_north, 'S': self.move_south, 'E': self.move_east, 'W': self.move_west}
        alist = []
        for i in path_list:
            alist.append(action_trans[i])
        return alist

    def initialize(self):
        # move = {'movenorth 1': 4, 'movesouth': -4, 'moveeast': -1, 'movewest': 1}
        self.House = []
        self.EventQueue = queue.PriorityQueue()
        self.Clock = 0.0
        self.epsilon = 0.2
        self.agent_face = 1
        self.total_waiting = 0

        # print(self.Agent_Location)
        path = self.get_path(self.Agent_Location, (0, 0))
        extract_action_list = self.extract_action_list_from_path(path)

        for f in extract_action_list:
            f(agent_host)
        self.Agent_Location = (0, 0)
        # print(self.Agent_Location)

        for i in range(len(self.Locations)):
            self.House.append(House(i, False, self.Locations[i]))
        # self.EventQueue.put((5, self.House[0]))
        # self.EventQueue.put((2, self.House[1]))
        # self.EventQueue.put((4, self.House[2]))
        # self.EventQueue.put((7, self.House[3]))
        # self.EventQueue.put((12, self.House[4]))

        # self.EventQueue.put((12, self.House[0]))
        # self.EventQueue.put((6, self.House[1]))
        # self.EventQueue.put((10, self.House[2]))
        # self.EventQueue.put((15, self.House[3]))
        # self.EventQueue.put((17, self.House[4]))
        #
        # self.EventQueue.put((19, self.House[0]))
        # self.EventQueue.put((10, self.House[1]))
        # self.EventQueue.put((16, self.House[2]))
        # self.EventQueue.put((23, self.House[3]))
        # self.EventQueue.put((22, self.House[4]))

        self.set_order(3, 30, 7, self.House[0])
        self.set_order(2, 30, 10, self.House[1])
        self.set_order(5, 30, 9, self.House[2])
        self.set_order(12, 30, 8, self.House[3])
        self.set_order(7, 30, 6, self.House[4])
        # print(self.EventQueue.queue)

    def set_order(self, start, end, interval, house):
        time = start
        while time <= end:
            self.EventQueue.put((time, house))
            time += interval

    def act(self, dir, agent_host):
        if dir == self.agent_face:
            self.Clock += 1
        else:
            path = self.get_path(self.Agent_Location, dir)
            extract_action_list = self.extract_action_list_from_path(path)

            for f in extract_action_list:
                f(agent_host)

            self.Agent_Location = dir
            self.Clock += (len(path))

        print("------------------")
        print(self.Clock)
        print("Agent", "to", self.Agent_Location)

        for i in self.House:
            if i.location == self.Agent_Location and i.state == True:
                print("Change the house", i.id)
                i.state = False
                self.deliever_food(agent_host)
                total = 0
                # print(i.orderTime)
                for order in i.orderTime:
                    total += self.Clock - order
                i.orderTime = []
                self.total_waiting += (total)
                return 1000 - (total)
        return 0

    def get_possible_actions(self):
        possibleAction = []
        for i in self.House:
            possibleAction.append(i.location)
        return possibleAction

    def get_curr_state(self):
        return [i for i in self.House] + [self.Agent_Location]

    def choose_action(self, curr_state, possible_actions, eps):
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0

        if len(possible_actions) == 0:
            return None

        actionProb = random.uniform(0.0, 1.0)
        # using the random move
        if actionProb <= eps:
            # actionIndex = random.randint(0, len(possible_actions) - 1)
            return possible_actions[random.randint(0, len(possible_actions) - 1)]
        # using greedy action
        else:
            maxQValue = min(self.q_table[curr_state].values()) - 1
            actionList = []
            for (action, qValue) in self.q_table[curr_state].items():
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

    # def get_actions(self, Agent_Location):
    #     direct = []
    #
    #     if Agent_Location + self.Row not in self.Locations and self.Agent_Location + self.Row < self.Row * self.Col:
    #         direct.append('down')
    #     if Agent_Location - self.Row not in self.Locations and self.Agent_Location - self.Row >= 0:
    #         direct.append('up')
    #     if Agent_Location + 1 not in self.Locations and (self.Agent_Location + 1) % self.Row != 0:
    #         direct.append('right')
    #     if Agent_Location - 1 not in self.Locations and (self.Agent_Location) % self.Row != 0:
    #         direct.append('left')
    #
    #     return direct

    def best_policy(self):
        # return [action]
        # self.epsilon = -1
        global Best_Testing
        Best_Testing = True
        returnAction = []
        s0 = self.transferCurrState(self.get_curr_state())
        possible_actions = self.get_possible_actions()
        a0 = self.choose_action(s0, possible_actions, self.epsilon)
        returnAction.append(a0)

        done_update = False
        while not done_update:
            self.Clock += 1

            if self.EventQueue.qsize() != 0 and self.Clock >= self.EventQueue.queue[0][0]:
                event_time, house = self.EventQueue.get()
                house.state = True
                house.orderTime.append(event_time)
                loc = house.location
                self.execute_actions(self.agent_host[0],
                                     "chat /fill " + str(loc[0] * 5 + 1) + " 8 " + str(loc[1] * 5 + 1) + " " + str(
                                         loc[0] * 5 + 3) + " 8 " + str(loc[1] * 5 + 2) + " minecraft:gold_block")

            self.act(returnAction[-1], agent_host)

            if self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False for i in self.House]:
                break

            else:
                s = self.transferCurrState(self.get_curr_state())
                possible_actions = self.get_possible_actions()
                next_a = self.choose_action(s, possible_actions, self.epsilon)
                returnAction.append(next_a)

        return returnAction

    def update_q_table(self, tau, S, A, R, T):
        
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
            nextMaxReward = max(self.q_table[S[0]].values())
        else:
            nextMaxReward = 0
        if len(S) != 0:
            self.q_table[curr_s][curr_a] = self.q_table[curr_s][curr_a] + self.alpha * (R[0] + self.gamma * nextMaxReward - self.q_table[curr_s][curr_a]) 
        else:
            self.q_table[curr_s][curr_a] = self.q_table[curr_s][curr_a] + self.alpha * (self.gamma * nextMaxReward - self.q_table[curr_s][curr_a]) 

    def run(self, agent_host):
        S, A, R = deque(), deque(), deque()

        present_reward = 0
        done_update = False
        while not done_update:
            # print("------------------")
            # print(self.Clock)
            # print("Agent",self.Agent_Location)
            # for i in self.House:
            #     print(i.id, i.state)
            # s0 = self.get_curr_state()
            s0 = self.transferCurrState(self.get_curr_state())

            # used to be ['left', right]... and now is only location which is the index.
            possible_actions = self.get_possible_actions()
            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            # S.append(s0)
            S.append(s0)
            A.append(a0)
            R.append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.1)
                # self.Clock += 1

                # eventQueue update
                # count = 0
                # if self.EventQueue.qsize() != 0:
                #     print('***********')
                #
                #     for i in self.EventQueue.queue:
                #         print(i[0], self.Clock)
                #         if i[0] == self.Clock:
                #             print("sameeeeee")
                #             count += 1
                #     print(count)
                #     print(self.EventQueue)
                #     for i in range(count):
                #         event_time, house = self.EventQueue.get()
                #         house.state = True
                #         # house.orderTime.append(event_time)
                #         house.orderTime = event_time
                #         loc = house.location
                #         self.execute_actions(self.agent_host[0], "chat /fill " + str(loc[0] * 5 + 1) + " 8 " + str(
                #             loc[1] * 5 + 1) + " " + str(loc[0] * 5 + 3) + " 8 " + str(
                #             loc[1] * 5 + 2) + " minecraft:gold_block")

                if self.EventQueue.qsize() != 0:
                    for i in self.EventQueue.queue:
                        # print('---------------')
                        # print(i)
                        if i[0] <= self.Clock:
                            event_time, house = self.EventQueue.get()
                            house.state = True
                            print("Change house", house.id)
                            # house.orderTime = event_time
                            house.orderTime.append(event_time)
                            loc = house.location
                            self.execute_actions(self.agent_host[0], "chat /fill " + str(loc[0] * 5 + 1) + " 8 " + str(
                                loc[1] * 5 + 1) + " " + str(loc[0] * 5 + 3) + " 8 " + str(
                                loc[1] * 5 + 2) + " minecraft:gold_block")
                if t < T:
                    print("in the action")
                    current_r = self.act(A[-1], agent_host)
                    R.append(current_r)

                    if (self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False, False, False, False,
                                                                                           False]) or t == 20:
                        print("End")
                        T = t + 1
                        #S.append('Term State')
                        present_reward = current_r
                        # print("Reward:", present_reward)

                    else:
                        # print(self.EventQueue.qsize(), [i.state for i in self.House])
                        # s = self.get_curr_state()
                        s = self.transferCurrState(self.get_curr_state())
                        S.append(s)
                        possible_actions = self.get_possible_actions()
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
                        A.append(next_a)

                # 最后在update我们的q_table
                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)
                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

    # def drawQ(self, curr_x=None, curr_y=None):
    #     if self.canvas is None or self.root is None:
    #         return
    #     self.canvas.delete("all")
    #     action_inset = 0.1
    #     action_radius = 0.1
    #     curr_radius = 0.2
    #     action_positions = [(0.5, 1 - action_inset), (0.5, action_inset), (1 - action_inset, 0.5), (action_inset, 0.5)]
    #     for x in range(world_x):
    #         for y in range(world_y):
    #             self.canvas.create_rectangle((world_x - 1 - x) * scale, (world_y - 1 - y) * scale,
    #                                          (world_x - 1 - x + 1) * scale, (world_y - 1 - y + 1) * scale,
    #                                          outline="#fff", fill="#000")
    #             for i in self.House:
    #                 if i.state == True:
    #                     i_x = i.location % 4
    #                     i_y = i.location // 4
    #                     # print(i.location, i_x, i_y)
    #                     self.canvas.create_rectangle((world_x - 1 - i_x) * scale, (world_y - 1 - i_y) * scale,
    #                                                  (world_x - 1 - i_x + 1) * scale, (world_y - 1 - i_y + 1) * scale,
    #                                                  outline="#fff", fill="#ff0")
    #
    #     root.update()


def get_total_map(x, y):
    return 'DrawCuboid x1="0"  y1="4" z1="0"  x2="' + str(x * 5 - 1) + '" y2="4" z2="' + str(
        y * 5 - 1) + '" type="stone" '


def get_house_xml(x, y):
    return '\n\t\t<DrawCuboid x1="' + str(x * 5 + 1) + '"  y1="5" z1="' + str(y * 5 + 1) + '"  x2="' + str(
        x * 5 + 3) + '" y2="7" z2="' + str(y * 5 + 2) + '" type="brick_block" />\n' \
                                                        '<DrawCuboid x1="' + str(x * 5 + 2) + '"  y1="5" z1="' + str(
        y * 5 + 3) + '"  x2="' + str(x * 5 + 2) + '" y2="6" z2="' + str(
        y * 5 + 3) + '" face="SOUTH" type="dark_oak_door" />\n'


def get_houses(locations):
    xml = ''
    for i in locations:
        xml += get_house_xml(i[0], i[1])
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


# a = world()
agent_host = MalmoPython.AgentHost()
agent_host_obervser = MalmoPython.AgentHost()
a = world(agent_host=[agent_host])
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
    num_repeats = 1000

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

        <''' + get_total_map(8, 8) + '''/>
        <DrawCuboid x1="20"  y1="5" z1="40"  x2="21" y2="7" z2="41" type="brick_block" />

''' + get_houses([(1, 0), (2, 2), (5, 6), (1, 2), (3, 3)]) + '''

      </DrawingDecorator>
      <ServerQuitFromTimeUp timeLimitMs="1000000000"/>
      <ServerQuitWhenAnyAgentFinishes/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Cristina</Name>
    <AgentStart>
      <Placement x="0.5" y="5" z="4.5" pitch="30" yaw="180"/>
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
    <Name>Manager</Name>
    <AgentStart>
      <Placement x="20.5" y="8" z="40.5" pitch="30" yaw="180"/>
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
my_mission_record = MalmoPython.MissionRecordSpec()
agent_host_obervser_record = MalmoPython.MissionRecordSpec()
my_mission.requestVideo(800, 500)
my_mission.setViewpoint(1)
my_mission.allowAllChatCommands()
my_mission.allowAllContinuousMovementCommands()

# Making a ClientPool
client_pool = MalmoPython.ClientPool()
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10001))

max_retries = 3

for retry in range(max_retries):
    try:
        # agent_host.startMission(my_mission, my_mission_record)
        safeStartMission(agent_host, my_mission, client_pool, my_mission_record, 0, 'Test')
        safeStartMission(agent_host_obervser, my_mission, client_pool, agent_host_obervser_record, 1, 'Test')
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission", ":", e)
            exit(1)
        else:
            time.sleep(0.1)

print("Waiting for the mission to start", end=' ')
print()

file = open("output_single.txt","w")

for i in range(num_repeats):
    if i % 5 == 0 and i != 0:
        print("---- this is the best policy")
        a.initialize()
        po = a.best_policy()
        # a.Agent_Location = (0, 0)
        # print("Total waiting time: " + str(a.total_waiting))
        file.write(str(a.total_waiting) + "\n")
        # if len(po) <= 8:
        #     print("this is the solution:" + str(po))

    # print("this is the q table", str(a.q_table))

    print("Waiting for the mission", (i + 1), "to start ", )
    agent_state, observer_state = agent_host.getWorldState(), agent_host_obervser.getWorldState()
    # world_state = agent_host.getWorldState()
    while not (agent_state.has_mission_begun and observer_state.has_mission_begun):
        time.sleep(0.1)
        # world_state = agent_host.getWorldState()
        agent_state, observer_state = agent_host.getWorldState(), agent_host_obervser.getWorldState()
        for error in agent_state.errors:
            print("Error:", error.text)

    print()
    print("Mission", (i + 1), "running.")

    # grid = load_grid(world_state)
    # print('........', grid)

    # Initialize
    a.initialize()

    a.run(agent_host)
file.close()

