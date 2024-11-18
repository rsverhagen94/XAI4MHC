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
from matrx.actions.object_actions import GrabObject, RemoveObject
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


class firefighter(custom_agent_brain):
    def __init__(self, name, condition, resistance, total_fires, victims, task, counterbalance_condition):
        super().__init__(name, condition, resistance, total_fires, victims, task, counterbalance_condition)
        # initialize important variables
        self._phase = Phase.WAIT_FOR_CALL
        self._resistance = resistance
        self._time_left = resistance
        self._task = task
        self._total_fires = total_fires
        self._extinguished_fires = []
        self._send_messages = []
        self._processed_messages = []
        self._smoke_plumes = []
        self._rescued = []
        self._modulos = []
        self._added = []
        self._goal_victim = None
        self._decided = None
        self._location = '?'

    def initialize(self):
        # initialize state tracker and navigator
        self._state_tracker = StateTracker(agent_id = self.agent_id)
        self._navigator = Navigator(agent_id = self.agent_id, action_set = self.action_set, algorithm = Navigator.A_STAR_ALGORITHM)

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
        # keep track of the number of smoke plumes
        for info in state.values():
            if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog' in info['obj_id'] and info['visualization']['size'] == 5:
                if info not in self._smoke_plumes:
                    self._smoke_plumes.append(info)
        # add big smoke plume at office 6 if fire is not extinguished with 35 minutes left during task 1
        if self._resistance == 35 and self.received_messages_content and 'Extinguishing fire in office 06.' not in self.received_messages_content and agent_name == 'fire_fighter_1' and self._task == 1:
            if (9,7) not in self._added:
                self._added.append((9,7))
                action_kwargs = add_object([(9,7)], "/images/smoke.svg", 1.75, 1, 'smog at 06', True, True)
                return AddObject.__name__, action_kwargs
            if (9,5) not in self._added:
                self._added.append((9,5))
                action_kwargs = add_object([(9,5)], "/images/smoke.svg", 5, 1, 'smog at 06', True, True)
                return AddObject.__name__, action_kwargs
        # add big smoke plume at office 5 if fire is not extinguished with 30 minutes left during task 2
        if self._resistance == 30 and self.received_messages_content and 'Extinguishing fire in office 05.' not in self.received_messages_content and agent_name == 'fire_fighter_1' and self._task == 2:
            if (2,7) not in self._added:
                self._added.append((2,7))
                action_kwargs = add_object([(2,7)], "/images/smoke.svg", 1.75, 1, 'smog at 05', True, True)
                return AddObject.__name__, action_kwargs
            if (2,5) not in self._added:
                self._added.append((2,5))
                action_kwargs = add_object([(2,5)], "/images/smoke.svg", 5, 1, 'smog at 05', True, True)
                return AddObject.__name__, action_kwargs
        # remove the big smoke plume at office 7 when extinguished during task 1
        if self._task == 1 and self.received_messages_content and 'Extinguishing fire in office 07.' in self.received_messages_content:
            if not state[{'obj_id': 'brutus', 'location': (16, 7)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_07' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # remove the big smoke plume at office 12 when extinguished during task 1
        if self._task == 1 and self.received_messages_content and 'Extinguishing fire in office 12.' in self.received_messages_content:
            if not state[{'obj_id': 'brutus', 'location': (9, 21)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_12' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # remove the big smoke plume at office 14 when extinguished during task 2
        if self._task == 2 and self.received_messages_content and 'Extinguishing fire in office 14.' in self.received_messages_content:
            if not state[{'obj_id': 'brutus', 'location': (23, 21)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_14' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # remove the big smoke plume at office 11 when extinguished during task 2
        if self._task == 2 and self.received_messages_content and 'Extinguishing fire in office 11.' in self.received_messages_content:
            if not state[{'obj_id': 'brutus', 'location': (2, 21)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_11' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # remove the big smoke plume at office 6 when extinguished during task 1
        if self._task == 1 and self.received_messages_content and 'Extinguishing fire in office 06.' in self.received_messages_content and self._resistance < 35:
            if not state[{'obj_id': 'brutus', 'location': (9, 7)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_06' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # remove the big smoke plume at office 5 when extinguished during task 2
        if self._task == 2 and self.received_messages_content and 'Extinguishing fire in office 05.' in self.received_messages_content and self._resistance < 30:
            if not state[{'obj_id': 'brutus', 'location': (2, 7)}]:
                for info in state.values():
                    if 'class_inheritance' in info and 'EnvObject' in info['class_inheritance'] and 'smog_at_05' in info['obj_id']:
                        return RemoveObject.__name__, {'object_id': info['obj_id'], 'remove_range': 100, 'action_duration': 0}
        # add iron debris blocking the exit of office 4 when the fire is extinguished during task 1        
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Extinguishing the fire in office 04' in self.received_messages_content[-1] and self._task == 1:
            if (23,4) not in self._added:
                self._added.append((23,4))
                action_kwargs = add_object([(23,4)], "/images/girder.svg", 1.25, 1, 'iron', False, True)
                return AddObject.__name__, action_kwargs
        # add iron debris blocking the exit of office 9 when the fire is extinguished during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Extinguishing the fire in office 09' in self.received_messages_content[-1] and self._task == 1:
            if (9,18) not in self._added:
                self._added.append((9,18))
                action_kwargs = add_object([(9,18)], "/images/girder.svg", 1.25, 1, 'iron', False, True)
                return AddObject.__name__, action_kwargs
        # add iron debris blocking the exit of office 5 when the fire is extinguished during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Extinguishing the fire in office 05' in self.received_messages_content[-1] and self._task == 1:
            if (2,6) not in self._added:
                self._added.append((2,6))
                action_kwargs = add_object([(2,6)], "/images/girder.svg", 1.25, 1, 'iron', False, True)
                return AddObject.__name__, action_kwargs
        # add iron debris blocking the exit of office 3 when the fire is extinguished during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Extinguishing the fire in office 13' in self.received_messages_content[-1] and self._task == 1:
            if (16,20) not in self._added:
                self._added.append((16,20))
                action_kwargs = add_object([(16,20)], "/images/girder.svg", 1.25, 1, 'iron', False, True)
                return AddObject.__name__, action_kwargs
        # add iron debris blocking the exit of office 9 when the fire is extinguished during task 2
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Extinguishing the fire in office 09' in self.received_messages_content[-1] and self._task == 2:
            if (9,18) not in self._added:
                self._added.append((9,18))
                action_kwargs = add_object([(9,18)], "/images/girder.svg", 1.25, 1, 'iron', False, True)
                return AddObject.__name__, action_kwargs
        # expand fire in office 4 when evacuating the victim first during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Evacuating the victim in office 04 first' in self.received_messages_content[-1] and self._task == 1:
            if (23,2) not in self._added:
                self._added.append((23,2))
                action_kwargs = add_object([(23,2)], "/images/fire2.svg", 2, 1, 'spread fire', True, True)
                return AddObject.__name__, action_kwargs
            return RemoveObject.__name__, {'object_id': 'fire_in_office_04', 'remove_range': 100}
        if self.received_messages_content and self._task == 1:
            for msg in self.received_messages_content:
                if 'Evacuating the victim in office 04 first' in msg and msg not in self._processed_messages:
                    self._processed_messages.append(msg)
                    return RemoveObject.__name__, {'object_id': 'fire_04', 'remove_range': 100}
        # expand fire in office 9 when evacuating the victim first during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Evacuating the victims in office 09 first' in self.received_messages_content[-1] and self._task == 1:
            if (9,16) not in self._added:
                self._added.append((9,16))
                action_kwargs = add_object([(9,16)], "/images/fire2.svg", 2, 1, 'spread fire', True, True)
                return AddObject.__name__, action_kwargs
            return RemoveObject.__name__, {'object_id': 'fire_in_office_09', 'remove_range': 100}
        if self.received_messages_content and self._task == 1:
            for msg in self.received_messages_content:
                if 'Evacuating the victims in office 09 first' in msg and msg not in self._processed_messages:
                    self._processed_messages.append(msg)
                    return RemoveObject.__name__, {'object_id': 'fire_09', 'remove_range': 100}
        # expand fire in office 5 when evacuating the victims first during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Evacuating the victims in office 05 first' in self.received_messages_content[-1] and self._task == 1:
            if (2,8) not in self._added:
                self._added.append((2,8))
                action_kwargs = add_object([(2,8)], "/images/fire2.svg", 2, 1, 'spread fire', True, True)
                return AddObject.__name__, action_kwargs
            return RemoveObject.__name__, {'object_id': 'fire_in_office_05', 'remove_range': 100}
        if self.received_messages_content and self._task == 1:
            for msg in self.received_messages_content:
                if 'Evacuating the victims in office 05 first' in msg and msg not in self._processed_messages:
                    self._processed_messages.append(msg)
                    return RemoveObject.__name__, {'object_id': 'fire_05', 'remove_range': 100}
        # expand fire in office 13 when evacuating the victims first during task 1
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Evacuating the victim in office 13 first' in self.received_messages_content[-1] and self._task == 1:
            if (16,22) not in self._added:
                self._added.append((16,22))
                action_kwargs = add_object([(16,22)], "/images/fire2.svg", 2, 1, 'spread fire', True, True)
                return AddObject.__name__, action_kwargs
            return RemoveObject.__name__, {'object_id': 'fire_in_office_13', 'remove_range': 100}
        if self.received_messages_content and self._task == 1:
            for msg in self.received_messages_content:
                if 'Evacuating the victim in office 13 first' in msg and msg not in self._processed_messages:
                    self._processed_messages.append(msg)
                    return RemoveObject.__name__, {'object_id': 'fire_13', 'remove_range': 100}
        # expand fire in office 9 when evacuating the victims first during task 2
        if agent_name == 'fire_fighter_1' and self.received_messages_content and 'Evacuating the victim in office 09 first' in self.received_messages_content[-1] and self._task == 2:
            if (9,16) not in self._added:
                self._added.append((9,16))
                action_kwargs = add_object([(9,16)], "/images/fire2.svg", 2, 1, 'spread fire', True, True)
                return AddObject.__name__, action_kwargs
            return RemoveObject.__name__, {'object_id': 'fire_in_office_09', 'remove_range': 100}
        if self.received_messages_content and self._task == 2:
            for msg in self.received_messages_content:
                if 'Evacuating the victim in office 09 first' in msg and msg not in self._processed_messages:
                    self._processed_messages.append(msg)
                    return RemoveObject.__name__, {'object_id': 'fire_09', 'remove_range': 100}
        # keep track of which fires have been extinguished
        if self.received_messages_content and 'Extinguishing' in self.received_messages_content[-1] and self.received_messages_content[-1] not in self._extinguished_fires:
            self._extinguished_fires.append(self.received_messages_content[-1])
        # keep track of the temperature with respect to the number of extinguished fires and fire resistance to collapse
        if len(self._extinguished_fires) / self._total_fires != 1 and self._resistance <= 50:
            self._temperature = '>'
            self._temperature_cat = 'higher'
        if len(self._extinguished_fires) / self._total_fires == 1 and self._resistance > 25 and self._resistance <= 50:
            self._temperature = '>'
            self._temperature_cat = 'higher'
        if len(self._extinguished_fires) / self._total_fires != 1 and self._resistance > 50:
            self._temperature = '<≈'
            self._temperature_cat = 'close'
        if len(self._extinguished_fires) / self._total_fires == 1 and self._resistance > 50:
            self._temperature = '<≈'
            self._temperature_cat = 'close'
        if len(self._extinguished_fires) / self._total_fires > 0.8 and self._resistance <= 25:
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
                # extract the offices to navigate to when send in to locate the fire source for each fire fighter seperately
                self._navigator.reset_full()
                if agent_name and agent_name == 'fire_fighter_2':
                    self._area_location = tuple((int(self._msg.split()[3]), int(self._msg.split()[5])))
                    self._area = 'office ' + self._msg.split()[7]
                    self._navigator.add_waypoints([self._area_location])
                if agent_name and agent_name == 'fire_fighter_3':
                    self._area_location = tuple((int(self._msg.split()[-5]), int(self._msg.split()[-3])))
                    self._area = 'office ' + self._msg.split()[-1]
                    self._navigator.add_waypoints([self._area_location])
                self._phase = Phase.FOLLOW_PATH_TO_ROOM

            if Phase.FOLLOW_PATH_TO_ROOM == self._phase:
                # navigate to offices to search for the fire source
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
                # abort the task when the temperature is higher than the safety threshold and the number of big smoke plumes is more than two
                if self._temperature == '>' and len(self._smoke_plumes) > 2:
                    self._send_message('<b>ABORTING TASK!</b> The combination of temperature and amount of smoke is too dangerous for me to continue searching for the fire source in ' + self._area + '.', agent_name.replace('_', ' ').capitalize())
                    self.agent_properties["img_name"] = "/images/human-danger2.gif"
                    self.agent_properties["visualize_size"] = 2.0
                    self._phase = Phase.PLAN_EXIT
                    return Idle.__name__, {'action_duration': 0}
                # otherwise continue with locating the fire source
                if self._temperature == '>' and len(self._smoke_plumes) < 3 or self._temperature == '>' and self._decided == 'robot' or self._temperature == '<≈':
                    self._room_tiles = room_tiles               
                    self._navigator.reset_full()
                    self._navigator.add_waypoints(room_tiles)
                    self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH

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
                            action_kwargs = add_object([info['location']], "/images/source-final.svg", 2, 1, 'fire source in ' + self._area, True, True)
                            self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH
                            return AddObject.__name__, action_kwargs
                        #if normal fire is found pin it on the map
                        if 'class_inheritance' in info and 'fire_object' in info['class_inheritance'] and 'fire' in info['obj_id'] and self._location != 'found':
                            self._send_message('Fire located in ' + self._area + ' and pinned on the map.', agent_name.replace('_', ' ').capitalize())
                            self._location = 'found'
                            action_kwargs = add_object([info['location']], "/images/fire2.svg", 2, 1, 'fire in ' + self._area, True, True)
                            self._phase = Phase.FOLLOW_ROOM_SEARCH_PATH
                            return AddObject.__name__, action_kwargs
                    return action, {}
                self._phase = Phase.PLAN_EXIT

            if Phase.PLAN_EXIT == self._phase:
                # navigate to exit of the building
                self._navigator.reset_full()
                if agent_name and agent_name == 'fire_fighter_2':
                    loc = (0, 11)
                if agent_name and agent_name == 'fire_fighter_1':
                    loc = (0, 12)
                if agent_name and agent_name == 'fire_fighter_3':
                    loc = (0, 13)
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
                # abort task when temperature is higher than safety threshold and the number of big smoke plumes is more than two
                if self._temperature == '>' and len(self._smoke_plumes) > 2:
                    for info in state.values():
                        if 'class_inheritance' in info and 'victim_object' in info['class_inheritance']:
                            self._goal_victim = info['img_name'][8:-4]
                    self._send_message('<b>ABORTING TASK!</b> The combination of temperature and amount of smoke is too dangerous for me to continue rescuing ' + self._goal_victim + '.', agent_name.replace('_', ' ').capitalize())
                    self.agent_properties["img_name"] = "/images/human-danger2.gif"
                    self.agent_properties["visualize_size"] = 2.0
                    self._phase = Phase.PLAN_EXIT
                    return Idle.__name__, {'action_duration': 0}
                # otherwise execute rescue action
                if self._temperature == '>' and len(self._smoke_plumes) < 3 or self._temperature == '>' and self._decided == 'robot' or self._temperature == '<≈':
                    self._phase = Phase.PLAN_PATH_TO_DROPPOINT
                    for info in state.values():
                        if 'class_inheritance' in info and 'victim_object' in info['class_inheritance']:
                            self._goal_victim = info['img_name'][8:-4]
                            self._send_message('Transporting ' + self._goal_victim + ' to the safe zone.', agent_name.replace('_', ' ').capitalize())
                            return CarryObject.__name__, {'object_id': info['obj_id'], 'action_duration': 0}

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