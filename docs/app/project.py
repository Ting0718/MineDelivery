import MalmoPython
import json
import logging
import os
import random
import sys
import time
import numpy
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from priority_dict import priorityDictionary as PQ

order = 0


def GetMissionXML(house, ordernum):
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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
            <DrawCuboid x1="0"  y1="4" z1="0"  x2="11" y2="4" z2="11" type="stone" />
            <DrawCuboid x1="6"  y1="4" z1="0"  x2="6" y2="4" z2="0" type="diamond_block" />

            <!-- First House -->
            <DrawCuboid x1="6"  y1="5" z1="6"  x2="8" y2="7" z2="8" type="brick_block" />
            <!--<DrawCuboid x1="2"  y1="4" z1="5"  x2="2" y2="5" z2="6" type="air" />-->
            <DrawCuboid x1="7"  y1="5" z1="5"  x2="7" y2="6" z2="5" face="NORTH" type="dark_oak_door" />''' + getItemDrawing(
        house) + '''

            <!-- Second House -->
            <DrawCuboid x1="9"  y1="5" z1="2"  x2="11" y2="7" z2="4" type="brick_block" />
            <!--<DrawCuboid x1="2"  y1="4" z1="5"  x2="2" y2="5" z2="6" type="air" />-->
            <DrawCuboid x1="8"  y1="5" z1="3"  x2="8" y2="6" z2="3" face="WEST" type="dark_oak_door" />''' + getItemDrawing(
        house) + '''

            <!-- Third House -->
            <DrawCuboid x1="1"  y1="5" z1="2"  x2="3" y2="7" z2="4" type="brick_block" />
            <!--<DrawCuboid x1="2"  y1="4" z1="5"  x2="2" y2="5" z2="6" type="air" />-->
            <DrawCuboid x1="4"  y1="5" z1="3"  x2="4" y2="6" z2="3" face="EAST" type="dark_oak_door" />''' + getItemDrawing(
        house) + '''

          </DrawingDecorator>
          <ServerQuitFromTimeUp timeLimitMs="100000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>

      <AgentSection mode="Survival">
        <Name>Cristina</Name>
        <AgentStart>''' + changeAgentPosition(ordernum) + '''
          <!--<Placement x="0.5" y="5.0" z="0.5" pitch="35" yaw="0"/>-->
        </AgentStart>
        <AgentHandlers>
          <ObservationFromGrid>
              <Grid name="floorAll">
                <min x="0" y="0" z="0"/>
                <max x="11" y="0" z="11"/>
              </Grid>
          </ObservationFromGrid>
          <DiscreteMovementCommands/>
          <ObservationFromFullStats/>
          <!--<RewardForTouchingBlockType>-->
            <!--<Block reward="100.0" type="lapis_block" behaviour="onceOnly"/>-->
          <!--</RewardForTouchingBlockType>-->
          <!--<RewardForSendingCommand reward="-1" />-->
          <AgentQuitFromTouchingBlockType>
              <Block type="diamond_block" />
          </AgentQuitFromTouchingBlockType>
        </AgentHandlers>
      </AgentSection>

    </Mission>'''


def getItemDrawing(house):
    drawing = ""
    if house == "house1":
        drawing = '<DrawCuboid x1="6"  y1="8" z1="6"  x2="8" y2="9" z2="8" type="diamond_ore" />'
    if house == "house2":
        drawing = '<DrawCuboid x1="9"  y1="8" z1="2"  x2="11" y2="9" z2="4" type="diamond_ore" />'
    if house == "house3":
        drawing = '<DrawCuboid x1="1"  y1="8" z1="2"  x2="3" y2="9" z2="4" type="diamond_ore" />'

    return drawing


def changeAgentPosition(ordernum):
    drawing = ""
    if ordernum == 3:
        drawing = '<Placement x="6.5" y="5.0" z="1.5" pitch="35" yaw="0"/>'
    else:
        drawing = '<Placement x="6.5" y="5.0" z="0.5" pitch="35" yaw="0"/>'
    return drawing


def load_grid(world_state):
    """
    Used the agent observation API to get a 21 X 21 grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
    """
    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            # print("error")
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'floorAll', 0)
            break
    return grid


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
    num_repeats = 10

for i in range(num_repeats):
    print("entering")
    # size = int(6 + 0.5*i)
    # print("Size of maze:", size)
    # mission_file = './world.xml'
    # with open(mission_file, 'r') as f:
    #     print("Loading mission from %s" % mission_file)
    #     mission_xml = f.read()
    #     my_mission = MalmoPython.MissionSpec(mission_xml, True)
    if order == 0:
        my_mission = MalmoPython.MissionSpec(GetMissionXML(house=None, ordernum=order), True)
    elif order == 1:
        my_mission = MalmoPython.MissionSpec(GetMissionXML(house="house1", ordernum=order), True)
    elif order == 2:
        my_mission = MalmoPython.MissionSpec(GetMissionXML(house="house2", ordernum=order), True)
    else:
        my_mission = MalmoPython.MissionSpec(GetMissionXML(house="house3", ordernum=order), True)

    my_mission_record = MalmoPython.MissionRecordSpec()
    my_mission.requestVideo(800, 500)
    my_mission.setViewpoint(1)

    # Attempt to start a mission:
    max_retries = 3
    my_clients = MalmoPython.ClientPool()
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))  # add Minecraft machines here as available

    for retry in range(max_retries):
        try:
            agent_host.startMission(my_mission, my_clients, my_mission_record, 0, "%s-%d" % ('Moshe', i))
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission", (i + 1), ":", e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission", (i + 1), "to start ", )
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)

    print("Mission", (i + 1), "running.")
    print(world_state)
    print("Number of orders: " + str(order))
    print()

    while world_state.is_mission_running:
        # agent_host.sendCommand("move 1")
        if order == 3:
            # time.sleep(1)
            grid = load_grid(world_state)
            print('........', grid)
            break
        else:
            break
    order += 1

    # print()
    # print("Mission", (i + 1), "ended")
