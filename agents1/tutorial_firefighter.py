import sys, random, enum, ast, time
from matrx import grid_world
from brains1.custom_agent_brain import custom_agent_brain
from utils1.util_functions import *
from actions1.custom_actions import *
from matrx import utils
from matrx.grid_world import GridWorld
from matrx.agents.agent_utils.state import State
from matrx.agents.agent_utils.navigator import Navigator
from matrx.agents.agent_utils.state_tracker import StateTracker
from matrx.actions.door_actions import OpenDoorAction
from matrx.actions.object_actions import GrabObject, DropObject, RemoveObject
from matrx.actions.move_actions import MoveNorth
from matrx.messages.message import Message
from matrx.messages.message_manager import MessageManager
from actions1.custom_actions import CarryObject, Drop

class Phase(enum.Enum):
    # define possible phases
    WAIT_FOR_CALL = 1,
    PLAN_PATH_TO_ROOM = 2,
    FOLLOW_PATH_TO_ROOM = 3,
    PLAN_ROOM_SEARCH_PATH = 4,
    FOLLOW_ROOM_SEARCH_PATH = 5,
    PLAN_PATH_TO_VICTIM = 6,
    FOLLOW_PATH_TO_VICTIM = 7,
    TAKE_VICTIM = 8,
    PLAN_PATH_TO_DROPPOINT = 9,
    FOLLOW_PATH_TO_DROPPOINT = 10,
    DROP_VICTIM = 11,
    PLAN_EXIT = 12,
    FOLLOW_EXIT_PATH = 13


class tutorial_firefighter(custom_agent_brain):
    def __init__(self, name, condition, resistance, total_fires, victims, task, counterbalance_condition):
        super().__init__(name, condition, resistance, total_fires, victims, task, counterbalance_condition)
        # initialize important variables
        self._phase = Phase.WAIT_FOR_CALL
        self._resistance = resistance
        self._time_left = resistance
        self._total_fires = total_fires
        self._extinguished_fires = []
        self._send_messages = []
        self._rescued = []
        self._modulos = []
        self._goal_victim = None
        self._decided = None
        self._location = '?'

    def initialize(self):
        # initialize state tracker and navigator
        self._state_tracker = StateTracker(agent_id=self.agent_id)
        self._navigator = Navigator(agent_id=self.agent_id,action_set=self.action_set, algorithm=Navigator.A_STAR_ALGORITHM)

    def filter_agent_observations(self, state):
        # calculate the number of seconds passed
        self._second = state['World']['tick_duration'] * state['World']['nr_ticks']
        # if 6 seconds passed, resistance to collapse decreases with 1 minute
        if int(self._second) % 6 == 0 and int(self._second) not in self._modulos:
            self._modulos.append(int(self._second))
            self._resistance -= 1
        return state

    def decide_on_agent_action(self, state):
        # keep track of own agent name
        agent_name = state[self.agent_id]['obj_id']
        # keep track of extinguished fires
        if self.received_messages_content and 'Extinguishing' in self.received_messages_content[-1] and self.received_messages_content[-1] not in self._extinguished_fires:
            self._extinguished_fires.append(self.received_messages_content[-1])
        # keep track of temperature with respect to the number of extinguished fires
        if len(self._extinguished_fires) / self._total_fires < 0.65:
            self._temperature = '>'
            self._temperature_cat = 'higher'
        if len(self._extinguished_fires) / self._total_fires == 1:
            self._temperature = '<'
            self._temperature_cat = 'lower'
        if len(self._extinguished_fires) / self._total_fires >= 0.65 and len(self._extinguished_fires) / self._total_fires < 1:
            self._temperature = '<≈'
            self._temperature_cat = 'close'

        # infinite loop until task is completed
        while True:
            # while remaining idle and waiting for a call to action  
            if Phase.WAIT_FOR_CALL == self._phase:
                # keep track of who decided on the call to action
                if self.received_messages_content and 'Sending in' in self.received_messages_content[-1] and 'Not sending in' not in self.received_messages_content[-1] and 'because' in self.received_messages_content[-1]:
                    self._decided = 'robot'
                if self.received_messages_content and 'Sending in' in self.received_messages_content[-1] and 'Not sending in' not in self.received_messages_content[-1] and 'because' not in self.received_messages_content[-1]:
                    self._decided = 'human'
                # extract the coordinates to navigate to when send in to rescue
                if self.received_messages_content and 'Coordinates' in self.received_messages_content[-1] and self._goal_victim not in self._rescued and agent_name == 'fire_fighter_1':
                    msg = self.received_messages_content[-1]
                    self._drop_location = tuple((int(msg.split()[-3]), int(msg.split()[-1])))
                    self._goal_location = tuple((int(msg.split()[2]), int(msg.split()[4])))
                    self._phase = Phase.PLAN_PATH_TO_VICTIM
                    return Idle.__name__, {'action_duration': 0}
                # plan path to room when send in to locate the fire source
                if self.received_messages_content and 'Target' in self.received_messages_content[-1] and self._location == '?' and agent_name != 'fire_fighter_1':
                    self._msg = self.received_messages_content[-1]
                    self._phase = Phase.PLAN_PATH_TO_ROOM
                    return Idle.__name__, {'action_duration': 0}
                # otherwise remain idle
                else:
                    return None, {}
                
            if Phase.PLAN_PATH_TO_ROOM == self._phase:
                # extract the office to navigate to when send in to locate the fire source
                self._navigator.reset_full()
                if agent_name and agent_name == 'fire_fighter_2':
                    self._area_location = tuple((int(self._msg.split()[3]), int(self._msg.split()[5])))
                    self._area = 'office ' + self._msg.split()[7]
                    self._navigator.add_waypoints([self._area_location])
                self._phase = Phase.FOLLOW_PATH_TO_ROOM

            if Phase.FOLLOW_PATH_TO_ROOM == self._phase:
                # navigate to office to search for the fire source
                self._send_message('Moving to ' + self._area + ' to search for the fire source.', agent_name.replace('_', ' ').capitalize())
                self._state_tracker.update(state)
                action = self._navigator.get_move_action(self._state_tracker)
                if action != None:
                    return action, {}
                self._phase = Phase.PLAN_ROOM_SEARCH_PATH

            if Phase.PLAN_ROOM_SEARCH_PATH == self._phase:
                # keep track of the tiles in the office
                room_tiles = [info['location'] for info in state.values()
                    if 'class_inheritance' in info 
                    and 'AreaTile' in info['class_inheritance']
                    and 'room_name' in info
                    and info['room_name'] == self._area]
                # continue with task if conditions are safe enough
                if self._temperature != '>' or self._temperature == '>' and self._decided == 'robot':
                    self._room_tiles = room_tiles               
                    self._navigator.reset_full()
                    self._navigator.add_waypoints(room_tiles)
                    self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH
                # otherwise abort task
                else:
                    self._send_message('<b>ABORTING TASK!</b> The combination of temperature and amount of smoke is too dangerous for me to continue searching for the fire source in ' + self._area + '.', agent_name.replace('_', ' ').capitalize())
                    self.agent_properties["img_name"] = "/images/human-danger2.gif"
                    self.agent_properties["visualize_size"] = 2.0
                    self._phase = Phase.PLAN_EXIT
                    return Idle.__name__, {'action_duration': 0}

            if Phase.FOLLOW_ROOM_SEARCH_PATH == self._phase:
                # traverse the office to search for the fire source
                self._state_tracker.update(state)
                action = self._navigator.get_move_action(self._state_tracker)
                if action != None:                   
                    for info in state.values():
                        # if fire source is found pin it on the map and update display that it is found
                        if 'class_inheritance' in info and 'fire_object' in info['class_inheritance'] and 'source' in info['obj_id'] and self._location != 'found':
                            self._send_message('<b>Fire source</b> located in ' + self._area + ' and pinned on the map.', agent_name.replace('_', ' ').capitalize())
                            self._location = 'found'
                            action_kwargs = add_object([info['location']], "/images/source-final.svg", 2, 1, 'fire source in ' + self._area)
                            self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH
                            return AddObject.__name__, action_kwargs
                        #if normal fire is found pin it on the map
                        if 'class_inheritance' in info and 'fire_object' in info['class_inheritance'] and 'fire' in info['obj_id'] and self._location != 'found':
                            self._send_message('Fire located in ' + self._area + ' and pinned on the map.', agent_name.replace('_', ' ').capitalize())
                            self._location = 'found'
                            action_kwargs = add_object([info['location']], "/images/fire2.svg", 2, 1, 'fire in ' + self._area)
                            self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH
                            return AddObject.__name__, action_kwargs
                    return action, {}
                self._phase = Phase.PLAN_EXIT

            if Phase.PLAN_EXIT == self._phase:
                # navigate to exit of the building
                self._navigator.reset_full()
                if agent_name and agent_name == 'fire_fighter_2':
                    loc = (0, 5)
                if agent_name and agent_name == 'fire_fighter_1':
                    loc = (0, 7)
                self._navigator.add_waypoints([loc])
                self._phase = Phase.FOLLOW_EXIT_PATH

            if Phase.FOLLOW_EXIT_PATH == self._phase:
                # exit the building and remain idle again
                self._state_tracker.update(state)
                action = self._navigator.get_move_action(self._state_tracker)
                if action != None:
                    return action, {}
                self._phase = Phase.WAIT_FOR_CALL
                self.agent_properties["img_name"] = "/images/rescue-man-final3.svg"
                self.agent_properties["visualize_size"] = 1.0
                return IdleDisappear.__name__, {'action_duration': 0}

            if Phase.PLAN_PATH_TO_VICTIM == self._phase:
                # plan path to victim when send in to rescue
                self._navigator.reset_full()
                self._navigator.add_waypoints([self._goal_location])
                self._phase = Phase.FOLLOW_PATH_TO_VICTIM

            if Phase.FOLLOW_PATH_TO_VICTIM == self._phase:
                # follow path to victim when send in to rescue
                self._state_tracker.update(state)
                action = self._navigator.get_move_action(self._state_tracker)
                if action != None:
                    return action, {}
                self._phase = Phase.TAKE_VICTIM

            if Phase.TAKE_VICTIM == self._phase:
                # continue with task if conditions are safe enough and rescue critically injured victim
                if self._temperature != '>' or self._temperature == '>' and self._decided == 'robot':
                    self._phase = Phase.PLAN_PATH_TO_DROPPOINT
                    for info in state.values():
                        if 'class_inheritance' in info and 'victim_object' in info['class_inheritance']:
                            self._goal_victim = info['img_name'][8:-4]
                            self._send_message('Transporting ' + self._goal_victim + ' to the safe zone.', agent_name.replace('_', ' ').capitalize())
                            return CarryObject.__name__, {'object_id': info['obj_id'], 'action_duration': 0}
                # otherwise abort task
                else:
                    for info in state.values():
                        if 'class_inheritance' in info and 'victim_object' in info['class_inheritance']:
                            self._goal_victim = info['img_name'][8:-4]
                    self._send_message('<b>ABORTING TASK!</b> The combination of temperature and amount of smoke is too dangerous for me to continue rescuing ' + self._goal_victim + '.', agent_name.replace('_', ' ').capitalize())
                    self.agent_properties["img_name"] = "/images/human-danger2.gif"
                    self.agent_properties["visualize_size"] = 2.0
                    self._phase = Phase.PLAN_EXIT
                    return Idle.__name__, {'action_duration': 0}

            if Phase.PLAN_PATH_TO_DROPPOINT == self._phase:
                # plan path to drop zone
                self._navigator.reset_full()
                self._navigator.add_waypoints([self._drop_location])
                self._phase = Phase.FOLLOW_PATH_TO_DROPPOINT

            if Phase.FOLLOW_PATH_TO_DROPPOINT == self._phase:
                # follow path to drop zone
                self._state_tracker.update(state)
                action = self._navigator.get_move_action(self._state_tracker)
                if action != None:
                    return action, {}
                self._phase = Phase.DROP_VICTIM

            if Phase.DROP_VICTIM == self._phase:
                # drop victim at drop zone
                self._rescued.append(self._goal_victim)
                self._send_message('Delivered ' + self._goal_victim + ' at the safe zone.', agent_name.replace('_', ' ').capitalize())
                self._phase = Phase.PLAN_EXIT
                self._goal_victim = None
                return Drop.__name__, {'action_duration':0}

    def _send_message(self, message_content, sender):
        # helper function to send messages
        message = Message(content = message_content, from_id = sender)
        if message.content not in self.received_messages_content:
            self.send_message(message)
            self._send_messages.append(message.content)