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
scale = 40
world_x = 4
world_y = 4
root = tk.Tk()
root.wm_title("Q-table")
canvas = tk.Canvas(root, width=world_x*scale, height=world_y*scale, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()
root.update()


class House(object):
    def __init__(self, id, state, location):
        self.id = id
        self.state = state
        self.orderTime = 0
        self.location = location


class Agent(object):
    def __init__(self):
        self.currentLocation = (0, 0)


class world(object):

    def __init__(self, alpha=0.3, gamma=0.8, n=1):
        self.epsilon = 0.2
        self.q_table = {}
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.EventQueue = queue.PriorityQueue()
        self.House = []
        self.Clock = 0.0
        self.Locations = [7, 12, 14]
        self.Col = 4
        self.Row = 4
        self.Agent_Location = 0
        self.canvas = canvas
        self.root = root
        self.initialize()

    def dijkstra_shortest_path(self, grid_obs, source, dest):
        if source == dest or source == 0:
            return []

        # ------------------------------------
        #
        #   Fill and submit this code
        #
        visited = []
        pq = PQ()
        distance = []
        predecessors = dict()

        for i in range(len(grid_obs)):
            visited.append(False)
            if i == source:
                predecessors[i] = None
                distance.append(0)
            else:
                predecessors[i] = -1
                distance.append(math.inf)

        pq[source] = 0

        while len(pq) != 0:

            index = pq.smallest()
            del pq[index]

            if index == dest:
                path = []
                temp = index
                while (temp != None):
                    path.append(temp)
                    temp = predecessors[temp]
                path.reverse()

            if (visited[index] == False):
                visited[index] = True

                neighbors = []
                # print(grid_obs[(index - 1).location])
                if index - 1 >= 0 and index % self.Row != 0 and grid_obs[index - 1] != "House":
                    neighbors.append(index - 1)

                if index + 1 < len(grid_obs) and (index + 1) % self.Row != 0 and grid_obs[index + 1] != "House":
                    neighbors.append(index + 1)

                if index + self.Row < len(grid_obs) and grid_obs[index + self.Row] != "House":
                    neighbors.append(index + self.Row)

                if index - self.Row >= 0 and grid_obs[index - self.Row] != "House":
                    neighbors.append(index - self.Row)

                # neighbors = [index-1, index+1, index+self.Row, index-self.Row]

                for n in neighbors:
                    if n >= 0 and n < len(grid_obs) and grid_obs[n] != "House":

                        if distance[n] > distance[index] + 1:
                            distance[n] = distance[index] + 1
                            predecessors[n] = index
                            pq[n] = distance[n]

        return path
        # -------------------------------------

    def extract_action_list_from_path(self, path_list):
        """
        Converts a block idx path to action list.

        Args
            path_list:  <list>  list of block idx from source block to dest block.

        Returns
            action_list: <list> list of string discrete action commands (e.g. ['movesouth 1', 'movewest 1', ...]
        """
        action_trans = {-self.Row: 'movesouth 1', self.Row: 'movenorth 1', -1: 'moveeast 1', 1: 'movewest 1'}
        alist = []
        for i in range(len(path_list) - 1):
            curr_block, next_block = path_list[i:(i + 2)]
            alist.append(action_trans[next_block - curr_block])
            alist.append(action_trans[next_block - curr_block])

        return alist

    def initialize(self):
        move = {'movenorth 1': 4, 'movesouth': -4, 'moveeast': -1, 'movewest': 1}

        global Best_Testing
        Best_Testing = False
        self.EventQueue = queue.PriorityQueue()
        self.House = []
        self.Clock = 0.0
        self.epsilon = 0.2
        origin = self.Agent_Location
        self.Agent_Location = 0

        # print("+++++++++++++++++++++++++++")
        # print("Origin",origin, "to", 0)

        grid = ['E' for i in range(self.Row * self.Col)]
        for i in self.Locations:
        # for i in self.House:
            # print(i.location)
            grid[i] = 'House'
            # grid[i.location] = 'House'
        # print('--------')
        # print(grid)

        path = self.dijkstra_shortest_path(grid, origin, 0)
        # print("Path: ",path)
        extract_action_list = self.extract_action_list_from_path(path)

        for i in extract_action_list:
            time.sleep(0.1)
            self.execute_actions(agent_host, i)

        self.Agent_Location = 0
        time.sleep(1)

        assert self.Agent_Location == 0

        # print(self.Agent_Location)

        for i in range(3):
            self.House.append(House(i, False, self.Locations[i]))
        self.EventQueue.put((5, self.House[0]))
        self.EventQueue.put((2, self.House[1]))
        self.EventQueue.put((4, self.House[2]))
        # print(self.EventQueue.queue)

    def get_curr_state(self):
        return [i for i in self.House] + [self.Agent_Location]

    def execute_actions(self, agent_host, action):
        time.sleep(0.1)
        agent_host.sendCommand(action)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)

    def act(self, dir, agent_host):
        # print("location is: " + loc)
        global Best_Testing
        cmd = ''
        if dir == 'up':
            loc = self.Agent_Location - self.Row
            cmd = 'movesouth 1'
        if dir == 'down':
            loc = self.Agent_Location + self.Row
            cmd = 'movenorth 1'
        if dir == 'left':
            loc = self.Agent_Location - 1
            cmd = 'moveeast 1'
        if dir == 'right':
            loc = self.Agent_Location + 1
            cmd = 'movewest 1'

        self.Agent_Location = loc
        if not Best_Testing:
            self.execute_actions(agent_host, cmd)
            self.execute_actions(agent_host, cmd)

        # print("------------------")
        # print(self.Clock)
        # print("Agent",cmd, "to", self.Agent_Location)
        # for i in self.House:
        #     print(i.id, i.state)

        for i in self.House:
            if i.location in self.get_adj(loc) and i.state == True:
                # print("Change the house", i.id)
                i.state = False
                return 1000 - (self.Clock - i.orderTime)
        return 0

    def get_adj(self, loc):

        adj = []

        if loc + self.Row < self.Row * self.Col:
            adj.append(loc + self.Row)
        if loc - self.Row >= 0:
            adj.append(loc - self.Row)
        if (loc + 1) % self.Row != 0:
            adj.append(loc + 1)
        if (loc) % self.Row != 0:
            adj.append(loc - 1)

        return adj

    def get_possible_actions(self):
        direct = []

        if self.Agent_Location + self.Row not in self.Locations and self.Agent_Location + self.Row < self.Row * self.Col:
            direct.append('down')
        if self.Agent_Location - self.Row not in self.Locations and self.Agent_Location - self.Row >= 0:
            direct.append('up')
        if self.Agent_Location + 1 not in self.Locations and (self.Agent_Location + 1) % self.Row != 0:
            direct.append('right')
        if self.Agent_Location - 1 not in self.Locations and (self.Agent_Location) % self.Row != 0:
            direct.append('left')

        return direct

    def choose_action(self, curr_state, possible_actions, eps):
        # if curr_state not in self.q_table:
        #     self.q_table[curr_state] = {}
        # for action in possible_actions:
        #     if action not in self.q_table[curr_state]:
        #         self.q_table[curr_state][action] = 0

        # global count, actionL
        # count+=1
        # return action[count]
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

        return frozenset(copy_state)

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

            if self.EventQueue.qsize() != 0 and self.Clock == self.EventQueue.queue[0][0]:
                event_time, house = self.EventQueue.get()
                house.state = True

            self.act(returnAction[-1], agent_host)

            if self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False, False, False]:
                break

            else:
                s = self.transferCurrState(self.get_curr_state())
                possible_actions = self.get_possible_actions()
                next_a = self.choose_action(s, possible_actions, self.epsilon)
                returnAction.append(next_a)

        return returnAction

    def update_q_table(self, tau, S, A, R, T):
        # curr_s = self.transferCurrState(S.popleft())
        self.drawQ()
        curr_s = S.popleft()
        curr_a = A.popleft()
        curr_r = R.popleft()

        nextMaxReward = 0

        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

        # if tau + self.n < T:
        #     # nextMaxReward = max(self.q_table[self.transferCurrState(S[-1])].values())
        #     nextMaxReward = max(self.q_table[S[-1]].values())
        # self.q_table[curr_s][curr_a] = curr_r + self.alpha * nextMaxReward # update the q table value

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
            possible_actions = self.get_possible_actions()
            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            # S.append(s0)
            S.append(s0)
            A.append(a0)
            R.append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.1)
                self.Clock += 1
                if self.EventQueue.qsize() != 0 and self.Clock == self.EventQueue.queue[0][0]:
                    event_time, house = self.EventQueue.get()
                    house.state = True
                    house.orderTime = self.Clock
                if t < T:
                    current_r = self.act(A[-1], agent_host)
                    R.append(current_r)

                    if self.EventQueue.qsize() == 0 and [i.state for i in self.House] == [False, False, False]:
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                        # print("Reward:", present_reward)

                    else:
                        # s = self.get_curr_state()
                        s = self.transferCurrState(self.get_curr_state())
                        S.append(s)
                        possible_actions = self.get_possible_actions()
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
                        A.append(next_a)
                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)
                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

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
        # min_value = -20
        # max_value = 20
        # for x in range(world_x):
        #     for y in range(world_y):
        #         s = "%d:%d" % (x,y)
        #         self.canvas.create_rectangle( (world_x-1-x)*scale, (world_y-1-y)*scale, (world_x-1-x+1)*scale, (world_y-1-y+1)*scale, outline="#fff", fill="#000")
        #         for action in range(4):
        #             if not s in self.q_table:
        #                 continue
        #             value = self.q_table[s][action]
        #             color = int( 255 * ( value - min_value ) / ( max_value - min_value )) # map value to 0-255
        #             color = max( min( color, 255 ), 0 ) # ensure within [0,255]
        #             color_string = '#%02x%02x%02x' % (255-color, color, 0)
        #             self.canvas.create_oval( (world_x - 1 - x + action_positions[action][0] - action_radius ) *scale,
        #                                      (world_y - 1 - y + action_positions[action][1] - action_radius ) *scale,
        #                                      (world_x - 1 - x + action_positions[action][0] + action_radius ) *scale,
        #                                      (world_y - 1 - y + action_positions[action][1] + action_radius ) *scale,
        #                                      outline=color_string, fill=color_string )
        # if curr_x is not None and curr_y is not None:
        #     self.canvas.create_oval( (world_x - 1 - curr_x + 0.5 - curr_radius ) * scale,
        #                              (world_y - 1 - curr_y + 0.5 - curr_radius ) * scale,
        #                              (world_x - 1 - curr_x + 0.5 + curr_radius ) * scale,
        #                              (world_y - 1 - curr_y + 0.5 + curr_radius ) * scale,
        #                              outline="#fff", fill="#fff" )
        # self.root.update()

def load_grid(world_state):
    """
    Used the agent observation API to get a 21 X 21 grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
    """
    while world_state.is_mission_running:
        # sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'floorAll', 0)
            break
    return grid


# a = world()

# for i in range(1000):
#     if i % 5 == 0 and i != 0:
#         print("---- this is the best policy")
#         po = a.best_policy()
#         print(len(po))

#         if len(po) <= 8:
#             print("this is the solution:" + str(po))
#         a.initialize()
#     # print("this is the q table", str(a.q_table))
#     a.run()
#     a.initialize()


a = world()
agent_host = MalmoPython.AgentHost()
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

mission_file = './world.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_mission.requestVideo(800, 500)
my_mission.setViewpoint(1)
# Attempt to start a mission:

# my_clients = MalmoPython.ClientPool()
# my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available


max_retries = 3
# my_clients = MalmoPython.ClientPool()
# my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission", (i + 1), ":", e)
            exit(1)
        else:
            time.sleep(0.1)

print("Waiting for the mission to start", end=' ')

for i in range(num_repeats):
    if i % 5 == 0 and i != 0:
        print("---- this is the best policy")
        a.initialize()
        po = a.best_policy()
        print(len(po), po)
        a.Agent_Location = 0

        # if len(po) <= 8:
        #     print("this is the solution:" + str(po))

    # print("this is the q table", str(a.q_table))

    print("Waiting for the mission", (i + 1), "to start ", )
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)

    print()
    print("Mission", (i + 1), "running.")

    # grid = load_grid(world_state)
    # print('........', grid)

    # Initialize
    a.initialize()
    a.run(agent_host)

    # indices = [i for i, x in enumerate(grid) if x == "dark_oak_door"]
    # print("the index of element " + str(indices))
