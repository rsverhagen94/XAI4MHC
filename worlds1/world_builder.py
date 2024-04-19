import os, random, sys, itertools
import numpy as np
from matrx import WorldBuilder
from matrx.actions import MoveNorth, OpenDoorAction, CloseDoorAction, GrabObject
from matrx.actions.move_actions import MoveEast, MoveSouth, MoveWest
from matrx.agents import AgentBrain, HumanAgentBrain, SenseCapability
from matrx.grid_world import GridWorld, AgentBody
from actions1.custom_actions import RemoveObjectTogether, DropObject, Idle, CarryObject, Drop, CarryObjectTogether, DropObjectTogether
from matrx.actions.object_actions import RemoveObject
from matrx.objects import EnvObject
from matrx.world_builder import RandomProperty
from matrx.goals import WorldGoal
from agents1.firefighter import firefighter
from agents1.robot import robot
from actions1.custom_actions import RemoveObjectTogether
from brains1.custom_human_brain import custom_human_brain
from loggers.action_logger import action_logger
from datetime import datetime
from loggers.message_logger import message_logger

random_seed = 1
key_action_map = {
        'ArrowUp': MoveNorth.__name__,
        'ArrowRight': MoveEast.__name__,
        'ArrowDown': MoveSouth.__name__,
        'ArrowLeft': MoveWest.__name__,
        'q': CarryObject.__name__,
        'w': Drop.__name__,
        'd': RemoveObjectTogether.__name__,
        'a': CarryObjectTogether.__name__,
        's': DropObjectTogether.__name__,
        'e': RemoveObject.__name__,
    }

def add_drop_off_zones(builder, exp_version):
    if exp_version == "experiment":
        builder.add_area((25, 9), width = 1, height = 8, name = "Drop off 1", visualize_opacity = 0, visualize_colour = "#e5ddd5", 
                         drop_zone_nr = 1, is_drop_zone = True, is_goal_block = False, is_collectable = False) 
    if exp_version == "trial":
        builder.add_area((17, 7), width = 1, height = 4, name = "Drop off 1", visualize_opacity = 0.5, visualize_colour = "#1F262A", 
                         drop_zone_nr = 1, is_drop_zone = True, is_goal_block = False, is_collectable = False) 
            
def add_agents(builder, name, condition, exp_version, resistance, no_fires, victims, task, counterbalance_condition):
    sense_capability = SenseCapability({AgentBody: np.inf, 
                                        CollectableBlock: 1, 
                                        None: np.inf, 
                                        IronObject: 1, 
                                        FireObject: 1, 
                                        SmokeObject: np.inf})
    
    if exp_version == "experiment":
        brain = robot(name = name, condition = condition, resistance = resistance, no_fires = no_fires, 
                      victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        brain2 = firefighter(name = name, condition = condition, resistance = resistance, no_fires = no_fires, 
                             victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        brain3 = firefighter(name = name, condition = condition, resistance = resistance, no_fires = no_fires, 
                             victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        brain4 = firefighter(name = name, condition = condition, resistance = resistance, no_fires = no_fires, 
                             victims = victims, task = task, counterbalance_condition = counterbalance_condition)

    if exp_version == "experiment":
        loc = (24, 12)
    else:
        loc = (16, 8)

    if name == 'Titus':  
        builder.add_agent(loc, brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, 
                          img_name = "/images/final-titus2.svg", visualize_when_busy = True, visualize_size = 1.1)
    if name == 'Brutus':  
        builder.add_agent(loc, brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, 
                          img_name = "/images/robot-final4.svg", visualize_when_busy = True, visualize_size = 1.1)
    builder.add_agent((0, 12), brain2, team = "Team 1", name = "fire fighter 1", sense_capability = sense_capability, is_traversable = True, 
                      img_name = "/images/rescue-man-final3.svg", visualize_when_busy = True, visualize_opacity = 0)
    builder.add_agent((0, 13), brain3, team = "Team 1", name = "fire fighter 3", sense_capability = sense_capability, is_traversable = True, 
                      img_name = "/images/rescue-man-final3.svg", visualize_when_busy = True, visualize_opacity = 0)
    builder.add_agent((0, 11), brain4, team = "Team 1", name = "fire fighter 2", sense_capability = sense_capability, is_traversable = True, 
                      img_name = "/images/rescue-man-final3.svg", visualize_when_busy = True, visualize_opacity = 0)

    # Add human agents
    brain = custom_human_brain(max_carry_objects = 1, grab_range = 1, drop_range = 0, remove_range = 1, fov_occlusion = True)
    if exp_version == "experiment":
        loc = (24, 13)
    else:
        loc = (16, 9)
    builder.add_human_agent(loc, brain, team = "Team 1", name =  "Human", visualize_opacity = 0, key_action_map = key_action_map, 
                            sense_capability = sense_capability, is_traversable = True, visualize_shape = 1, visualize_colour = '#e5ddd5', visualize_when_busy = False)

def create_builder(id, exp_version, name, condition, task, counterbalance_condition):
    # Set numpy's random generator
    np.random.seed(random_seed)

    if task == 1:
        time = 1080
    if task == 2:
        time = 1080
    if task == 3:
        time = 720
    if task == 4:
        time = 720

    if exp_version == "trial":
        goal = CollectionGoal(max_nr_ticks=10000000000)
        builder = WorldBuilder(shape = [19,19], tick_duration = 0.5, run_matrx_api = True, random_seed = random_seed, 
                               run_matrx_visualizer = False, verbose = False, simulation_goal =goal , visualization_bg_clr = '#9a9083')

    if exp_version == "trial":
        resistance = 90
        no_fires = 3
        victims = 'known'

        goal = CollectionGoal(max_nr_ticks=10000000000)
        builder = WorldBuilder(shape = [13,13], tick_duration = 0.5, run_matrx_api = True, random_seed = random_seed, 
                               run_matrx_visualizer = False, verbose = False, simulation_goal =goal , visualization_bg_clr = "#e5ddd5")
        builder.add_room(top_left_location = (0, 0), width = 5, height = 4, name = 'office 1', door_locations = [(2,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,4)})
        builder.add_room(top_left_location = (6,0), width = 5, height = 4, name = 'office 2', door_locations = [(8,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (8,4)})
        builder.add_room(top_left_location = (0,9), width = 5, height = 4, name = 'office 3', door_locations = [(2,9)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,8)})
        builder.add_room(top_left_location = (6,9), width = 5, height = 4, name = 'office 4', door_locations = [(8,9)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (8,8)})
        builder.add_object(location = [2,0], is_traversable = True, is_movable = False, name = "area 01 sign", img_name = "/images/sign01.svg", visualize_depth = 110, visualize_size = 0.5)
        builder.add_object(location = [8,0], is_traversable = True, is_movable = False, name = "area 02 sign", img_name = "/images/sign02.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2,12], is_traversable = True, is_movable = False, name = "area 03 sign", img_name = "/images/sign03.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [8,12], is_traversable = True, is_movable = False, name = "area 04 sign", img_name = "/images/sign04.svg", visualize_depth = 110, visualize_size = 0.55)
        for loc in [(0,0), (0,1), (0,2), (0,3), (1,3), (3,3), (4,3), (4,2), (4,1), (4,0), (3,0), (2,0), (1,0),
                    (6,0), (6,1), (6,2), (6,3), (7,3), (9,3), (10,3), (10,2), (10,1), (10,0), (9,0), (8,0), (7,0),
                    (0,9), (0,10), (0,11), (0,12), (1,12), (2,12), (3,12), (4,12), (4,11), (4,10), (4,9), (3,9), (1,9),
                    (6,9), (6,10), (6,11), (6,12), (7,12), (8,12), (9,12), (10,12), (10,11), (10,10), (10,9), (9,9), (7,9)]:
            builder.add_object(loc, 'roof', EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall6.png")        
        
        builder.add_object((3,11), 'critically injured woman in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
        builder.add_object((2,1), 'mildly injured elderly woman in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
        builder.add_object((3,1), 'mildly injured man in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
        builder.add_object((12,5), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        builder.add_object((12,6), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        builder.add_object((12,7), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        builder.add_object((8,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
        builder.add_object((2,9), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
        builder.add_object((3,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
        builder.add_object((8,10), 'source', FireObject, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
        builder.add_object(location = (8,9), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
        for i in [(8,8), (7,8), (6,8), (9,8), (9,7), (9,6), (8,7), (8,6), (7,7), (7,6), (6,7), (6,6), (10,8), (10,7), (10,6)]:
            builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)

    # Create the goal
    if exp_version == "experiment":
        goal = CollectionGoal(max_nr_ticks=time)
        builder = WorldBuilder(shape = [26,25], tick_duration = 0.5, run_matrx_api = True, run_matrx_visualizer = False, 
                               verbose = False, simulation_goal = goal, visualization_bg_clr = '#e5ddd5')
        current_exp_folder = datetime.now().strftime(condition + "_" + name + "_T" + str(task) + "_%d-%m_%Hh-%Mm-%Ss")
        logger_save_folder = os.path.join("experiment_logs/counterbalance_" + counterbalance_condition + "/" + str(id), current_exp_folder)
        builder.add_logger(action_logger, log_strategy = 1, save_path = logger_save_folder, file_name_prefix = "actions_")
        builder.add_logger(message_logger, save_path = logger_save_folder, file_name_prefix = "messages_")

        builder.add_room(top_left_location = (0, 0), width = 5, height = 4, name = 'office 1', door_locations = [(2,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,4)})
        builder.add_room(top_left_location = (7,0), width = 5, height = 4, name = 'office 2', door_locations = [(9,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9,4)})
        builder.add_room(top_left_location = (14,0), width = 5, height = 4, name = 'office 3', door_locations = [(16,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16,4)})
        builder.add_room(top_left_location = (21,0), width = 5, height = 4, name = 'office 4', door_locations = [(23,3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (23,4)})
        builder.add_room(top_left_location = (0,7), width = 5, height = 4, name = 'office 5', door_locations = [(2,7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,6)})
        builder.add_room(top_left_location = (7,7), width = 5, height = 4, name = 'office 6', door_locations = [(9,7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9,6)})
        builder.add_room(top_left_location = (14,7), width = 5, height = 4, name = 'office 7', door_locations = [(16,7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16,6)})
        builder.add_room(top_left_location = (0,14), width = 5, height = 4, name = 'office 8', door_locations = [(2,17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,18)})
        builder.add_room(top_left_location = (7,14), width = 5, height = 4, name = 'office 9', door_locations = [(9,17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9,18)})
        builder.add_room(top_left_location = (14,14), width = 5, height = 4, name = 'office 10', door_locations = [(16,17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16,18)})
        builder.add_room(top_left_location = (0,21), width = 5, height = 4, name = 'office 11', door_locations = [(2,21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2,20)})
        builder.add_room(top_left_location = (7,21), width = 5, height = 4, name = 'office 12', door_locations = [(9,21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9,20)})
        builder.add_room(top_left_location = (14,21), width = 5, height = 4, name = 'office 13', door_locations = [(16,21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16,20)})
        builder.add_room(top_left_location = (21,21), width = 5, height = 4, name = 'office 14', door_locations = [(23,21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (23,20)})

        builder.add_object(location = [2,0], is_traversable = True, is_movable = False, name = "area 01 sign", img_name = "/images/sign01.svg", visualize_depth = 110, visualize_size = 0.5)
        builder.add_object(location = [9,0], is_traversable = True, is_movable = False, name = "area 02 sign", img_name = "/images/sign02.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16,0], is_traversable = True, is_movable = False, name = "area 03 sign", img_name = "/images/sign03.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [23,0], is_traversable = True, is_movable = False, name = "area 04 sign", img_name = "/images/sign04.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2,10], is_traversable = True, is_movable = False, name = "area 05 sign", img_name = "/images/sign05.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [9,10], is_traversable = True, is_movable = False, name = "area 06 sign", img_name = "/images/sign06.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16,10], is_traversable = True, is_movable = False, name = "area 07 sign", img_name = "/images/sign07.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2,14], is_traversable = True, is_movable = False, name = "area 08 sign", img_name = "/images/sign08.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [9,14], is_traversable = True, is_movable = False, name = "area 09 sign", img_name = "/images/sign09.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16,14], is_traversable = True, is_movable = False, name = "area 10 sign", img_name = "/images/sign10.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2,24], is_traversable = True, is_movable = False, name = "area 11 sign", img_name = "/images/sign11.svg", visualize_depth = 110, visualize_size = 0.45)
        builder.add_object(location = [9,24], is_traversable = True, is_movable = False, name = "area 12 sign", img_name = "/images/sign12.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16,24], is_traversable = True, is_movable = False, name = "area 13 sign", img_name = "/images/sign13.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [23,24], is_traversable = True, is_movable = False, name = "area 14 sign", img_name = "/images/sign14.svg", visualize_depth = 110, visualize_size = 0.55)

        for loc in [(0,0), (0,1), (0,2), (0,3), (1,3), (3,3), (4,3), (4,2), (4,1), (4,0), (3,0), (2,0), (1,0),
                    (7,0), (7,1), (7,2), (7,3), (8,3), (10,3), (11,3), (11,2), (11,1), (11,0), (10,0), (9,0), (8,0),
                    (14,0), (14,1), (14,2), (14,3), (15,3), (17,3), (18,3), (18,2), (18,1), (18,0), (17,0), (16,0), (15,0),
                    (24,3), (22,3), (21,3), (21,2), (21,1), (21,0), (22,0), (23,0), (24,0),
                    (0,7), (0,8), (0,9), (0,10), (1,10), (2,10), (3,10), (4,10), (4,9), (4,8), (4,7), (3,7), (1,7),
                    (7,7), (7,8), (7,9), (7,10), (8,10), (9,10), (10,10), (11,10), (11,9), (11,8), (11,7), (10,7), (8,7),
                    (14,7), (14,8), (14,9), (14,10), (15,10), (16,10), (17,10), (18,10), (18,9), (18,8), (18,7), (17,7), (15,7),
                    (0,14), (1,14), (2,14), (3,14), (0,14), (0,15), (0,16), (0,17), (1,17), (3,17), (4,17), (4,16), (4,15), (4,14),
                    (7,14), (8,14), (9,14), (10,14), (11,14), (7,15), (7,16), (7,17), (8,17), (10,17), (11,17), (11,16), (11,15),
                    (14,14), (15,14), (16,14), (17,14), (18,14), (14,15), (14,16), (14,17), (15,17), (18,15), (18,16), (18,17), (17,17),
                    (0,23), (0,22), (0,21), (1,21), (3,21), (4,21), (4,22), (4,23),
                    (7,21), (7,22), (10,21), (11,21), (11,22), (11,23), (8,21), (7,23),
                    (14,21), (14,22), (14,23), (15,21), (17,21), (18,21), (18,22), (18,23),
                    (21,21), (21,22), (21,23), (22,21), (24,21)]:
            builder.add_object(loc, 'roof', EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall6.png")

        for loc in [(24,24), (23,24), (22,24), (21,24), (18,24), (17,24), (16,24), (15,24), (14,24), (11,24), (10,24), (9,24), (8,24), (7,24), (4,24), (3,24), (2,24), (1,24), (0,24)]:
            builder.add_object(loc, 'roof', EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_bottom.png")

        for loc in [(25,24)]:
            builder.add_object(loc, 'roof', EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_bottom_right.png")

        for loc in [(25,3), (25,2), (25,1), (25,0), (25,21), (25,22), (25,23)]:
            builder.add_object(loc, 'roof', EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_right.png")

        if task == 1:
            resistance = 91
            no_fires = 8
            victims = 'known'
            builder.add_object((3,9), 'critically injured woman in area 5', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            builder.add_object((3,1), 'mildly injured man in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg")
            builder.add_object((3,23), 'critically injured elderly man in area 11', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg")
            builder.add_object((3,16), 'critically injured man in area 8', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            builder.add_object((10,2), 'critically injured elderly woman in area 2', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object((10,15), 'mildly injured elderly man in area 9', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object((9,15), 'mildly injured man in area 9', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
            builder.add_object((24,1), 'mildly injured elderly woman in area 4', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            builder.add_object((17,1), 'mildly injured woman in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object((9,8), 'source', FireObject, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (9,7), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(9,6), (8,6), (7,6), (10,6), (10,5), (10,4), (9,5), (9,4), (8,5), (8,4), (7,5), (7,4), (11,6), (11,5), (11,4)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((9,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (9,21), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(9,19), (8,19), (7,19), (10,19), (10,18), (10,20), (9,18), (9,20), (8,18), (8,20), (7,18), (7,20), (11,19), (11,18), (11,20)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)       
            builder.add_object((17,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((16,16), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True) 
            builder.add_object((16,7), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((24,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((16,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((9,17), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((23,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((23,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((3,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            #builder.add_object((16,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((10,16), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)          
            #builder.add_object((3,2), 'critically injured woman in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            builder.add_object((25,8), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,9), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,11), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,12), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,13), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,14), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,15), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,16), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        
        if task == 2:
            resistance = 91
            no_fires = 10
            victims = 'unknown'
            builder.add_object((25,17), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,16), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,15), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,14), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,13), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,12), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,11), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,9), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,8), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((24,23), 'critically injured man in area 14', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            builder.add_object((10,16), 'critically injured woman in area 9', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            #builder.add_object((3,9), 'critically injured man in area 5', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            builder.add_object((3,16), 'critically injured elderly woman in area 10', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object((10,23), 'critically injured elderly man in area 12', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg")
            builder.add_object((17,1), 'mildly injured elderly man in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object((16,1), 'mildly injured man in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg")
            builder.add_object((15,1), 'mildly injured woman in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object((17,23), 'mildly injured elderly woman in area 13', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            builder.add_object((3,1), 'mildly injured man in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
            builder.add_object((2,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (2,7), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(2,6), (1,6), (0,6), (3,6), (3,5), (3,4), (2,5), (2,4), (1,5), (1,4), (0,5), (0,4), (4,6), (4,5), (4,4)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((9,8), 'source', FireObject, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (9,7), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(9,6), (8,6), (7,6), (10,6), (10,5), (10,4), (9,5), (9,4), (8,5), (8,4), (7,5), (7,4), (11,6), (11,5), (11,4)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((17,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((23,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((16,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((2,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((9,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((16,16), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((16,7), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((23,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((2,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((16,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((9,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((23,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            #builder.add_object((2,17), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((17,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((9,17), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            #builder.add_object((2,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,17), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((3,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.252, smoke = 'normal', is_traversable = True, is_movable = True)     

        if task == 3:
            resistance = 61
            victims = 'known'
            no_fires = 8
            builder.add_object((25,8), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,9), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,11), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,12), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,13), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,14), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((25,15), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object((9,22), 'source', FireObject, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (9,21), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(9,19), (8,19), (7,19), (10,19), (10,18), (10,20), (9,18), (9,20), (8,18), (8,20), (7,18), (7,20), (11,19), (11,18), (11,20)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((2,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (2,21), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(2,19), (1,19), (0,19), (3,19), (3,18), (3,20), (2,18), (2,20), (1,18), (1,20), (0,18), (0,20), (4,19), (4,18), (4,20)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((3,16), 'critically injured woman in area 8', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            builder.add_object((3,2), 'critically injured man in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            builder.add_object((10,16), 'critically injured elderly man in area 9', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg")
            builder.add_object((3,9), 'critically injured elderly woman in area 5', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object((24,23), 'mildly injured elderly man in area 14', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object((23,1), 'mildly injured elderly woman in area 4', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            builder.add_object((24,1), 'mildly injured man in area 4', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
            builder.add_object((10,1), 'mildly injured woman in area 2', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object((24,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((16,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((10,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((24,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((9,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object((16,16), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True) 
            #builder.add_object((16,3), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object((2,7), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            #builder.add_object((23,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)

        if task == 4:
            resistance = 61
            victims = 'unknown'
            no_fires = 10

            #builder.add_object((25,8), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            #builder.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            #.add_object((25,10), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            #builder.add_object((25,11), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,11), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,12), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,13), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,14), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((25,15), name = "Collect Block", callable_class = GhostBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object((3,2), 'critically injured elderly man in area 1', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg")
            #builder.add_object((3,9), 'critically injured woman in area 5', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            #builder.add_object((3,16), 'critically injured woman in area 8', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured woman2.svg")
            builder.add_object((3,15), 'critically injured man in area 8', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            #builder.add_object((10,2), 'critically injured elderly woman in area 2', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object((15,9), 'mildly injured woman in area 7', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object((17,9), 'mildly injured man in area 7', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
            builder.add_object((16,9), 'mildly injured elderly man in area 7', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object((10,9), 'mildly injured elderly woman in area 6', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            #builder.add_object((16,1), 'mildly injured man in area 3', callable_class = CollectableBlock, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg")
            builder.add_object((9,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((10,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((2,22), 'source', FireObject, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (2,21), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(2,19), (1,19), (0,19), (3,19), (3,18), (3,20), (2,18), (2,20), (1,18), (1,20), (0,18), (0,20), (4,19), (4,18), (4,20)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((2,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (2,7), name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.25)
            for i in [(2,6), (1,6), (0,6), (3,6), (3,5), (3,4), (2,5), (2,4), (1,5), (1,4), (0,5), (0,4), (4,6), (4,5), (4,4)]:
                builder.add_object(location = i, name = 'smog', callable_class = SmokeObject, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object((17,8), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((23,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,21), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,17), 'iron', IronObject, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object((16,22), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((9,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((16,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((23,2), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object((9,16), 'fire', FireObject, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)

    add_drop_off_zones(builder, exp_version)
    add_agents(builder, name, condition, exp_version, resistance, no_fires, victims, task, counterbalance_condition)

    return builder

class CollectableBlock(EnvObject):
    def __init__(self, location, name, visualize_shape, img_name):
        super().__init__(location, name, is_traversable = True, is_movable = True,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = 0.9, class_callable = CollectableBlock,
                         is_drop_zone = False, is_goal_block = False, is_collectable = True)

class FireObject(EnvObject):
    def __init__(self, location, name, smoke, visualize_shape, img_name, visualize_size, is_traversable, is_movable):
        super().__init__(location, name, smoke = smoke, is_traversable = is_traversable, is_movable = is_movable,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = FireObject,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)
        
class IronObject(EnvObject):
    def __init__(self, location, name, weight, visualize_shape, img_name, visualize_size, is_traversable, is_movable):
        super().__init__(location, name, weight = weight, is_traversable = is_traversable, is_movable = is_movable,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = IronObject,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)

class SmokeObject(EnvObject):
    def __init__(self, location, name, visualize_shape, img_name, visualize_size):
        super().__init__(location, name, is_traversable = True, is_movable = False,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = SmokeObject,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)

class GhostBlock(EnvObject):
    def __init__(self, location, drop_zone_nr, name, visualize_shape, img_name, visualize_opacity):
        super().__init__(location, name, is_traversable = True, is_movable = False,
                         visualize_shape = visualize_shape, img_name = img_name, visualize_opacity = visualize_opacity, 
                         visualize_size = 0.9, class_callable = GhostBlock,
                         visualize_depth = 110, drop_zone_nr = drop_zone_nr,
                         is_drop_zone = False, is_goal_block = True, is_collectable = False)


class CollectionGoal(WorldGoal):
    '''
    The goal for BW4T world (the simulator), so determines
    when the simulator should stop.
    '''
    def __init__(self, max_nr_ticks:int):
        '''
        @param max_nr_ticks the max number of ticks to be used for this task
        '''
        super().__init__()
        self.max_nr_ticks = max_nr_ticks

        # A dictionary of all drop locations. The keys is the drop zone number, the value another dict.
        # This dictionary contains as key the rank of the to be collected object and as value the location
        # of where it should be dropped, the shape and colour of the block, and the tick number the correct
        # block was delivered. The rank and tick number is there so we can check if objects are dropped in
        # the right order.
        self.__drop_off:dict = {}
        self.__drop_off_zone:dict = {}

        # We also track the progress
        self.__progress = 0
        self.__score = 0
    
    def score(self, grid_world: GridWorld):
        return self.__score

    def goal_reached(self, grid_world: GridWorld):
        if grid_world.current_nr_ticks >= self.max_nr_ticks:
            return True
        return self.isBlocksPlaced(grid_world)

    def isBlocksPlaced(self, grid_world:GridWorld):
        '''
        @return true if all blocks have been placed in right order
        '''

        if self.__drop_off =={}:  # find all drop off locations, its tile ID's and goal blocks
            self.__find_drop_off_locations(grid_world)

        # Go through each drop zone, and check if the blocks are there in the right order
        is_satisfied, progress = self.__check_completion(grid_world)

        # Progress in percentage
        self.__progress = progress / sum([len(goal_blocks)\
            for goal_blocks in self.__drop_off.values()])

        return is_satisfied

    def progress(self, grid_world:GridWorld):
        if self.__drop_off == {}:  # find all drop off locations, its tile ID's and goal blocks
            self.__find_drop_off_locations(grid_world)

        # Go through each drop zone, and check if the blocks are there in the right order
        is_satisfied, progress = self.__check_completion(grid_world)

        # Progress in percentage
        self.__progress = progress / sum([len(goal_blocks)\
            for goal_blocks in self.__drop_off.values()])
        return self.__progress

    def __find_drop_off_locations(self, grid_world):

        goal_blocks = {}  # dict with as key the zone nr and values list of ghostly goal blocks
        all_objs = grid_world.environment_objects
        for obj_id, obj in all_objs.items():  # go through all objects
            if "drop_zone_nr" in obj.properties.keys():  # check if the object is part of a drop zone
                zone_nr = obj.properties["drop_zone_nr"]  # obtain the zone number
                if obj.properties["is_goal_block"]:  # check if the object is a ghostly goal block
                    if zone_nr in goal_blocks.keys():  # create or add to the list
                        goal_blocks[zone_nr].append(obj)
                    else:
                        goal_blocks[zone_nr] = [obj]

        self.__drop_off_zone:dict = {}
        self.__drop_off:dict = {}
        for zone_nr in goal_blocks.keys():  # go through all drop of zones and fill the drop_off dict
            # Instantiate the zone's dict.
            self.__drop_off_zone[zone_nr] = {}
            self.__drop_off[zone_nr] = {}

            # Obtain the zone's goal blocks.
            blocks = goal_blocks[zone_nr].copy()

            # The number of blocks is the maximum the max number blocks to collect for this zone.
            max_rank = len(blocks)

            # Find the 'bottom' location
            bottom_loc = (-np.inf, -np.inf)
            for block in blocks:
                if block.location[1] > bottom_loc[1]:
                    bottom_loc = block.location

            # Now loop through blocks lists and add them to their appropriate ranks
            for rank in range(max_rank):
                loc = (bottom_loc[0], bottom_loc[1]-rank)

                # find the block at that location
                for block in blocks:
                    if block.location == loc:
                        # Add to self.drop_off
                        self.__drop_off_zone[zone_nr][rank] = [loc, block.properties['img_name'][8:-4], None]
                        for i in self.__drop_off_zone.keys():
                            self.__drop_off[i] = {}
                            vals = list(self.__drop_off_zone[i].values())
                            vals.reverse()
                            for j in range(len(self.__drop_off_zone[i].keys())):
                                self.__drop_off[i][j] = vals[j]

    def __check_completion(self, grid_world):
        # Get the current tick number
        curr_tick = grid_world.current_nr_ticks

        # loop through all zones, check the blocks and set the tick if satisfied
        for zone_nr, goal_blocks in self.__drop_off.items():
            # Go through all ranks of this drop off zone
            for rank, block_data in goal_blocks.items():
                loc = block_data[0]  # the location, needed to find blocks here
                shape = block_data[1]  # the desired colour
                tick = block_data[2]

                # Retrieve all objects, the object ids at the location and obtain all BW4T Blocks from it
                all_objs = grid_world.environment_objects
                obj_ids = grid_world.get_objects_in_range(loc, object_type=EnvObject, sense_range=0)
                blocks = [all_objs[obj_id] for obj_id in obj_ids
                          if obj_id in all_objs.keys() and "is_collectable" in all_objs[obj_id].properties.keys()]
                blocks = [b for b in blocks if b.properties["is_collectable"]]

                # Check if there is a block, and if so if it is the right one and the tick is not yet set, then set the
                # current tick.
                if len(blocks) > 0 and blocks[0].properties['img_name'][8:-4] == shape and \
                        tick is None:
                    self.__drop_off[zone_nr][rank][2] = curr_tick
                    if 'critical' in blocks[0].properties['img_name'][8:-4]:
                        self.__score += 6
                    if 'mild' in blocks[0].properties['img_name'][8:-4]:
                        self.__score += 3
                    
                # if there is no block, reset its tick to None

                elif len(blocks) == 0:
                    if self.__drop_off[zone_nr][rank][2] != None:
                        self.__drop_off[zone_nr][rank][2] = None
                        if rank in [0, 1, 2, 3]:
                            self.__score -= 6
                        if rank in [4, 5, 6, 7]:
                            self.__score -= 3

        # Now check if all blocks are collected in the right order
        is_satisfied = True
        progress = 0
        for zone_nr, goal_blocks in self.__drop_off.items():
            zone_satisfied = True
            ticks = [goal_blocks[r][2] for r in range(len(goal_blocks))]  # list of ticks in rank order

            # check if all ticks are increasing
            for tick in ticks:
                if tick is not None:
                    progress += 1
            if None in ticks:
                zone_satisfied = False
            # update our satisfied boolean
            is_satisfied = is_satisfied and zone_satisfied

        return is_satisfied, progress

