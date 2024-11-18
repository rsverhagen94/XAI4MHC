import os
import numpy as np
from matrx import WorldBuilder
from matrx.agents import SenseCapability
from matrx.grid_world import GridWorld, AgentBody
from matrx.objects import EnvObject
from matrx.goals import WorldGoal
from agents1.firefighter import firefighter
from agents1.robot import robot
from agents1.tutorial_firefighter import tutorial_firefighter
from agents1.tutorial_robot import tutorial_robot
from brains1.custom_human_brain import custom_human_brain
from loggers.action_logger import action_logger
from datetime import datetime
from loggers.message_logger import message_logger

def add_drop_off_zones(builder, study_version):
    """ function to add drop off zones to the MATRX world """
    # add different drop off zone depending on study version
    if study_version == "experiment":
        builder.add_area((25, 9), width = 1, height = 8, name = "Drop off 1", visualize_opacity = 0, visualize_colour = "#e5ddd5", drop_zone_nr = 1, is_drop_zone = True, is_goal_block = False, is_collectable = False) 
    if study_version == "trial":
        builder.add_area((12, 5), width = 1, height = 3, name = "Drop off 1", visualize_opacity = 0, visualize_colour = "#e5ddd5", drop_zone_nr = 1, is_drop_zone = True, is_goal_block = False, is_collectable = False)
            
def add_agents(builder, name, condition, study_version, resistance, total_fires, victims, task, counterbalance_condition):
    """ function to add artificial and human agents to the MATRX world """
    # determine sense capability for agents
    sense_capability = SenseCapability({AgentBody: np.inf, victim_object: 1, None: np.inf, iron_object: 2, fire_object: 1, smoke_object: np.inf})
    # add different agents to the world depending on study version
    if study_version == "experiment":
        # initialize robot, firefighters, and human brains
        robot_brain = robot(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        firefighter1_brain = firefighter(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        firefighter2_brain = firefighter(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        firefighter3_brain = firefighter(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        human_brain = custom_human_brain(max_carry_objects = 1, grab_range = 1, drop_range = 0, remove_range = 1, fov_occlusion = True)
        # add different agent icon depending on robot name
        if name == 'Titus':  
            builder.add_agent((24, 12), robot_brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, img_name = "/images/final-titus2.svg", visualize_when_busy = True, visualize_size = 1.1)
        if name == 'Brutus':  
            builder.add_agent((24, 12), robot_brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, img_name = "/images/robot-final4.svg", visualize_when_busy = True, visualize_size = 1.1)    
        # add firefighter and human agents to the world
        builder.add_agent((0, 12), firefighter1_brain, team = "Team 1", name = "fire fighter 1", sense_capability = sense_capability, is_traversable = True, img_name = "/images/rescue-man-final3.svg", visualize_when_busy = False, visualize_opacity = 0)
        builder.add_agent((0, 13), firefighter2_brain, team = "Team 1", name = "fire fighter 3", sense_capability = sense_capability, is_traversable = True, img_name = "/images/rescue-man-final3.svg", visualize_when_busy = False, visualize_opacity = 0)
        builder.add_agent((0, 11), firefighter3_brain, team = "Team 1", name = "fire fighter 2", sense_capability = sense_capability, is_traversable = True, img_name = "/images/rescue-man-final3.svg", visualize_when_busy = False, visualize_opacity = 0)    
        builder.add_human_agent((24, 13), human_brain, team = "Team 1", name =  "Human", visualize_opacity = 0, sense_capability = sense_capability, is_traversable = True, visualize_shape = 1, visualize_colour = "#e5ddd5", visualize_when_busy = False)
    else:
        # initialize robot, firefighters, and human brains
        robot_brain = tutorial_robot(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        firefighter1_brain = tutorial_firefighter(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        firefighter2_brain = tutorial_firefighter(name = name, condition = condition, resistance = resistance, total_fires = total_fires, victims = victims, task = task, counterbalance_condition = counterbalance_condition)
        human_brain = custom_human_brain(max_carry_objects = 1, grab_range = 1, drop_range = 0, remove_range = 1, fov_occlusion = True)
        # add different agent icon depending on robot name
        if name == 'Titus':  
            builder.add_agent((11, 6), robot_brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, img_name = "/images/final-titus2.svg", visualize_when_busy = True, visualize_size = 1.1)
        if name == 'Brutus':  
            builder.add_agent((11, 6), robot_brain, team = "Team 1", name = name, sense_capability = sense_capability, is_traversable = True, img_name = "/images/robot-final4.svg", visualize_when_busy = True, visualize_size = 1.1)
        # add firefighter and human agents to the world
        builder.add_agent((0, 5), firefighter1_brain, team = "Team 1", name = "fire fighter 1", sense_capability = sense_capability, is_traversable = True, img_name = "/images/rescue-man-final3.svg", visualize_when_busy = False, visualize_opacity = 0)
        builder.add_agent((0, 7), firefighter2_brain, team = "Team 1", name = "fire fighter 2", sense_capability = sense_capability, is_traversable = True, img_name = "/images/rescue-man-final3.svg", visualize_when_busy = False, visualize_opacity = 0)
        builder.add_human_agent((11, 7), human_brain, team = "Team 1", name =  "Human", visualize_opacity = 0, sense_capability = sense_capability, is_traversable = True, visualize_shape = 1, visualize_colour = "#e5ddd5", visualize_when_busy = False)

def create_world(participant_id, study_version, name, condition, task, counterbalance_condition):
    """ function to create the MATRX world """
    # create the smaller and simpler trial/tutorial world
    if study_version == "trial":
        # determine task characteristics
        resistance = 90
        total_fires = 3
        victims = 'known'
        goal = collection_goal(max_nr_ticks = 10000000000)
        # create the outline of the world
        builder = WorldBuilder(shape = [13, 13], tick_duration = 0.5, run_matrx_api = True, run_matrx_visualizer = False, verbose = False, simulation_goal = goal, visualization_bg_clr = "#e5ddd5")
        # fill the world with rooms/offices
        builder.add_room(top_left_location = (0, 0), width = 5, height = 4, name = 'office 01', door_locations = [(2, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 4)})
        builder.add_room(top_left_location = (6, 0), width = 5, height = 4, name = 'office 02', door_locations = [(8, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (8, 4)})
        builder.add_room(top_left_location = (0, 9), width = 5, height = 4, name = 'office 03', door_locations = [(2, 9)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 8)})
        builder.add_room(top_left_location = (6, 9), width = 5, height = 4, name = 'office 04', door_locations = [(8, 9)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (8, 8)})
        # add office signs 
        builder.add_object(location = [2, 0], is_traversable = True, is_movable = False, name = "area 01 sign", img_name = "/images/sign01.svg", visualize_depth = 110, visualize_size = 0.5)
        builder.add_object(location = [8, 0], is_traversable = True, is_movable = False, name = "area 02 sign", img_name = "/images/sign02.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2, 12], is_traversable = True, is_movable = False, name = "area 03 sign", img_name = "/images/sign03.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [8, 12], is_traversable = True, is_movable = False, name = "area 04 sign", img_name = "/images/sign04.svg", visualize_depth = 110, visualize_size = 0.55)
        # add roof icons to the offices
        for location in [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (3, 3), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0),
                        (6, 0), (6, 1), (6, 2), (6, 3), (7, 3), (9, 3), (10, 3), (10, 2), (10, 1), (10, 0), (9, 0), (8, 0), (7, 0),
                        (0, 9), (0, 10), (0, 11), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (4, 11), (4, 10), (4, 9), (3, 9), (1, 9),
                        (6, 9), (6, 10), (6, 11), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (10, 11), (10, 10), (10, 9), (9, 9), (7, 9)]:
            builder.add_object(location = location, name = 'roof', callable_class = EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall6.png")        
        # add drop zone icons where victims should be dropped on the be rescued
        builder.add_object(location = (12, 5), name = "drop zone victim 1", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        builder.add_object(location = (12, 6), name = "drop zone victim 2", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        builder.add_object(location = (12, 7), name = "drop zone victim 3", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
        # add victims to the world
        builder.add_object(location = (3, 11), name = 'critically injured woman in area 3', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
        builder.add_object(location = (2, 1), name = 'mildly injured elderly woman in area 1', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
        builder.add_object(location = (3, 1), name = 'mildly injured man in area 1', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
        # add fire, smoke, and iron to the world
        builder.add_object(location = (8, 2), name = 'fire 02', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
        builder.add_object(location = (3, 2), name = 'fire 01', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
        builder.add_object(location = (2, 9), name = 'iron', callable_class = iron_object, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
        builder.add_object(location = (8, 10), name = 'source 04', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
        builder.add_object(location = (8, 9), name = 'smog', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
        builder.add_object(location = (8, 7), name = 'smog', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 5)

    # create the official experiment world
    if study_version == "experiment":
        # determine the maximum amount of time for the task (1800 ticks with tick duration 0.5 seconds = 900 seconds / 15 minutes as maximum amount of task time)
        goal = collection_goal(max_nr_ticks = 1800)
        # create world outline and initiliaze builder
        builder = WorldBuilder(shape = [26, 25], tick_duration = 0.5, run_matrx_api = True, run_matrx_visualizer = False, verbose = False, simulation_goal = goal, visualization_bg_clr = '#e5ddd5')
        # determine directories for logging
        current_experiment_dir = datetime.now().strftime(condition + "_" + name + "_T" + str(task) + "_%d-%m_%Hh-%Mm-%Ss")
        logger_save_dir = os.path.join("experiment_logs/counterbalance_" + counterbalance_condition + "/" + str(id), current_experiment_dir)
        # add loggers to the world
        builder.add_logger(action_logger, log_strategy = 1, save_path = logger_save_dir, file_name_prefix = "actions_")
        builder.add_logger(message_logger, save_path = logger_save_dir, file_name_prefix = "messages_")
        # fill world with rooms/offices
        builder.add_room(top_left_location = (0, 0), width = 5, height = 4, name = 'office 01', door_locations = [(2, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 4)})
        builder.add_room(top_left_location = (7, 0), width = 5, height = 4, name = 'office 02', door_locations = [(9, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9, 4)})
        builder.add_room(top_left_location = (14, 0), width = 5, height = 4, name = 'office 03', door_locations = [(16, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16, 4)})
        builder.add_room(top_left_location = (21, 0), width = 5, height = 4, name = 'office 04', door_locations = [(23, 3)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (23, 4)})
        builder.add_room(top_left_location = (0, 7), width = 5, height = 4, name = 'office 05', door_locations = [(2, 7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 6)})
        builder.add_room(top_left_location = (7, 7), width = 5, height = 4, name = 'office 06', door_locations = [(9, 7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9, 6)})
        builder.add_room(top_left_location = (14, 7), width = 5, height = 4, name = 'office 07', door_locations = [(16, 7)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16, 6)})
        builder.add_room(top_left_location = (0, 14), width = 5, height = 4, name = 'office 08', door_locations = [(2, 17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 18)})
        builder.add_room(top_left_location = (7, 14), width = 5, height = 4, name = 'office 09', door_locations = [(9, 17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9, 18)})
        builder.add_room(top_left_location = (14, 14), width = 5, height = 4, name = 'office 10', door_locations = [(16, 17)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16, 18)})
        builder.add_room(top_left_location = (0, 21), width = 5, height = 4, name = 'office 11', door_locations = [(2, 21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (2, 20)})
        builder.add_room(top_left_location = (7, 21), width = 5, height = 4, name = 'office 12', door_locations = [(9, 21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (9, 20)})
        builder.add_room(top_left_location = (14, 21), width = 5, height = 4, name = 'office 13', door_locations = [(16, 21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (16, 20)})
        builder.add_room(top_left_location = (21, 21), width = 5, height = 4, name = 'office 14', door_locations = [(23, 21)], 
                         doors_open = True, door_visualization_opacity = 0, wall_visualize_colour = "#8a8a8a", with_area_tiles = True, 
                         area_visualize_colour = '#0008ff', area_visualize_opacity = 0.0, door_open_colour = '#e5ddd5', area_custom_properties = {'doormat': (23, 20)})
        # add office signs
        builder.add_object(location = [2, 0], is_traversable = True, is_movable = False, name = "area 01 sign", img_name = "/images/sign01.svg", visualize_depth = 110, visualize_size = 0.5)
        builder.add_object(location = [9, 0], is_traversable = True, is_movable = False, name = "area 02 sign", img_name = "/images/sign02.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16, 0], is_traversable = True, is_movable = False, name = "area 03 sign", img_name = "/images/sign03.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [23, 0], is_traversable = True, is_movable = False, name = "area 04 sign", img_name = "/images/sign04.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2, 10], is_traversable = True, is_movable = False, name = "area 05 sign", img_name = "/images/sign05.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [9, 10], is_traversable = True, is_movable = False, name = "area 06 sign", img_name = "/images/sign06.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16, 10], is_traversable = True, is_movable = False, name = "area 07 sign", img_name = "/images/sign07.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2, 14], is_traversable = True, is_movable = False, name = "area 08 sign", img_name = "/images/sign08.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [9, 14], is_traversable = True, is_movable = False, name = "area 09 sign", img_name = "/images/sign09.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16, 14], is_traversable = True, is_movable = False, name = "area 10 sign", img_name = "/images/sign10.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [2, 24], is_traversable = True, is_movable = False, name = "area 11 sign", img_name = "/images/sign11.svg", visualize_depth = 110, visualize_size = 0.45)
        builder.add_object(location = [9, 24], is_traversable = True, is_movable = False, name = "area 12 sign", img_name = "/images/sign12.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [16, 24], is_traversable = True, is_movable = False, name = "area 13 sign", img_name = "/images/sign13.svg", visualize_depth = 110, visualize_size = 0.55)
        builder.add_object(location = [23, 24], is_traversable = True, is_movable = False, name = "area 14 sign", img_name = "/images/sign14.svg", visualize_depth = 110, visualize_size = 0.55)
        # add a roof/walls to the offices
        for location in [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (3, 3), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0),
                        (7, 0), (7, 1), (7, 2), (7, 3), (8, 3), (10, 3), (11, 3), (11, 2), (11, 1), (11, 0), (10, 0), (9, 0), (8, 0),
                        (14, 0), (14, 1), (14, 2), (14, 3), (15, 3), (17, 3), (18, 3), (18, 2), (18, 1), (18, 0), (17, 0), (16, 0), (15, 0),
                        (24, 3), (22, 3), (21, 3), (21, 2), (21, 1), (21, 0), (22, 0), (23, 0), (24, 0),
                        (0, 7), (0, 8), (0, 9), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (4, 9), (4, 8), (4, 7), (3, 7), (1, 7),
                        (7, 7), (7, 8), (7, 9), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (11, 9), (11, 8), (11, 7), (10, 7), (8, 7),
                        (14, 7), (14, 8), (14, 9), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (18, 9), (18, 8), (18, 7), (17, 7), (15, 7),
                        (0, 14), (1, 14), (2, 14), (3, 14), (0, 14), (0, 15), (0, 16), (0, 17), (1, 17), (3, 17), (4, 17), (4, 16), (4, 15), (4, 14),
                        (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (7, 15), (7, 16), (7, 17), (8, 17), (10, 17), (11, 17), (11, 16), (11, 15),
                        (14, 14), (15, 14), (16, 14), (17, 14), (18, 14), (14, 15), (14, 16), (14, 17), (15, 17), (18, 15), (18, 16), (18, 17), (17, 17),
                        (0, 23), (0, 22), (0, 21), (1, 21), (3, 21), (4, 21), (4, 22), (4, 23),
                        (7, 21), (7, 22), (10, 21), (11, 21), (11, 22), (11, 23), (8, 21), (7, 23),
                        (14, 21), (14, 22), (14, 23), (15, 21), (17, 21), (18, 21), (18, 22), (18, 23),
                        (21, 21), (21, 22), (21, 23), (22, 21), (24, 21)]:
            builder.add_object(location = location, name = 'roof', callable_class = EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall6.png")
        for location in [(24, 24), (23, 24), (22, 24), (21, 24), (18, 24), (17, 24), (16, 24), (15, 24), (14, 24), (11, 24), (10, 24), (9, 24), (8, 24), (7, 24), (4, 24), (3, 24), (2, 24), (1, 24), (0, 24)]:
            builder.add_object(location = location, name = 'roof', callable_class = EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_bottom.png")
        for location in [(25, 24)]:
            builder.add_object(location = location, name = 'roof', callable_class = EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_bottom_right.png")
        for location in [(25, 3), (25, 2), (25, 1), (25, 0), (25, 21), (25, 22), (25, 23)]:
            builder.add_object(location = location, name = 'roof', callable_class = EnvObject, is_traversable = True, is_movable = False, visualize_shape = 'img', img_name = "/images/wall_right.png")
        # create the first of the two tasks
        if task == 1:
            # determine task characteristics
            resistance = 151
            total_fires = 8
            victims = 'known'
            # add drop zone icons where victims should be dropped on the be rescued
            builder.add_object(location = (25, 7), name = "drop zone victim 1", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 8), name = "drop zone victim 2", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 9), name = "drop zone victim 3", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 10), name = "drop zone victim 4", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman3.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 11), name = "drop zone victim 5", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 12), name = "drop zone victim 6", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man2.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 13), name = "drop zone victim 7", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 14), name = "drop zone victim 8", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 15), name = "drop zone victim 9", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman2.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 16), name = "drop zone victim 10", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            builder.add_object(location = (25, 17), name = "drop zone victim 11", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman2.svg", drop_zone_nr = 0, visualize_opacity = 0.5)
            # add victims to the world
            builder.add_object(location = (3, 2), name = 'critically injured elderly woman in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object(location = (3, 16), name = 'critically injured man in area 08', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured man.svg")
            builder.add_object(location = (3, 23), name = 'critically injured woman in area 11', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            builder.add_object(location = (17, 1), name = 'mildly injured elderly man in area 03', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man2.svg")
            builder.add_object(location = (16, 1), name = 'mildly injured woman in area 03', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman2.svg")
            builder.add_object(location = (24, 1), name = 'mildly injured elderly woman in area 04', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            builder.add_object(location = (3, 9), name = 'mildly injured man in area 05', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured man.svg")
            builder.add_object(location = (2, 9), name = 'mildly injured woman in area 05', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman3.svg")
            builder.add_object(location = (10, 15), name = 'mildly injured elderly man in area 09', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object(location = (9, 15), name = 'mildly injured woman in area 09', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object(location = (17, 23), name = 'mildly injured elderly woman in area 13', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman2.svg")
            # add fire and smoke to the world
            builder.add_object(location = (16, 8), name = 'source 07', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (16, 7), name = 'smog at 07', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object(location = (16, 5), name = 'smog at 07', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 5)
            builder.add_object(location = (9, 22), name = 'fire 12', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (9, 21), name = 'smog at 12', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object(location = (9, 19), name = 'smog at 12', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 5)     
            builder.add_object(location = (17, 2), name = 'fire 03', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (24, 2), name = 'fire 04', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (9, 8), name = 'fire 07', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (3, 8), name = 'fire 05', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (17, 22), name = 'fire 13', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (10, 16), name = 'fire 09', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)          
        # create the seconds task
        if task == 2:
            # determine task characteristics
            resistance = 151
            total_fires = 6
            victims = 'unknown'
            # add drop zone icons where victims should be dropped on the be rescued
            builder.add_object(location = (25, 5), name = "drop zone victim 1", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man3.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 6), name = "drop zone victim 2", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman3.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 7), name = "drop zone victim 3", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 9), name = "drop zone victim 4", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 10), name = "drop zone victim 5", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 11), name = "drop zone victim 6", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 13), name = "drop zone victim 7", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg", drop_zone_nr = 0, visualize_opacity = 0)            
            builder.add_object(location = (25, 14), name = "drop zone victim 8", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 15), name = "drop zone victim 9", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured man3.svg", drop_zone_nr = 0, visualize_opacity = 0)   
            builder.add_object(location = (25, 16), name = "drop zone victim 10", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured woman2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 17), name = "drop zone victim 11", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            builder.add_object(location = (25, 18), name = "drop zone victim 12", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg", drop_zone_nr = 0, visualize_opacity = 0)  
            builder.add_object(location = (25, 19), name = "drop zone victim 13", callable_class = dropzone_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman2.svg", drop_zone_nr = 0, visualize_opacity = 0)
            # add victims to the world
            builder.add_object(location = (3, 16), name = 'critically injured elderly man in area 08', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured elderly man.svg")
            builder.add_object(location = (1, 15), name = 'critically injured woman in area 08', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured woman.svg")
            builder.add_object(location = (15, 15), name = 'critically injured elderly woman in area 10', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/critically injured elderly woman.svg")
            builder.add_object(location = (2, 2), name = 'mildly injured man in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured man3.svg")
            builder.add_object(location = (3, 1), name = 'mildly injured man in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured man2.svg")
            builder.add_object(location = (2, 1), name = 'mildly injured elderly man in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man2.svg")
            builder.add_object(location = (1, 1), name = 'mildly injured woman in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman2.svg")
            builder.add_object(location = (1, 2), name = 'mildly injured elderly woman in area 01', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman2.svg")
            builder.add_object(location = (17, 1), name = 'mildly injured elderly man in area 03', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man.svg")
            builder.add_object(location = (16, 1), name = 'mildly injured woman in area 03', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman.svg")
            builder.add_object(location = (9, 15), name = 'mildly injured woman in area 09', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured woman3.svg")
            builder.add_object(location = (8, 15), name = 'mildly injured elderly man in area 09', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly man3.svg")
            builder.add_object(location = (10, 15), name = 'mildly injured elderly woman in area 09', callable_class = victim_object, visualize_shape = 'img', img_name = "/images/mildly injured elderly woman.svg")
            # add fire, smoke, and iron to the world
            builder.add_object(location = (2, 22), name = 'fire 11', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (2, 21), name = 'smog at 11', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object(location = (2, 19), name = 'smog at 11', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 5)
            builder.add_object(location = (23, 22), name = 'source 14', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/source-final.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (23, 21), name = 'smog at 14', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 1.75)
            builder.add_object(location = (23, 19), name = 'smog at 14', callable_class = smoke_object, visualize_shape = 'img', img_name = "/images/smoke.svg", visualize_size = 5)
            builder.add_object(location = (17, 2), name = 'fire 03', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
            builder.add_object(location = (2, 8), name = 'fire 05', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 2, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (23, 3), name = 'iron', callable_class = iron_object, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True) 
            builder.add_object(location = (10, 16), name = 'fire 09', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'normal', is_traversable = True, is_movable = True)
            builder.add_object(location = (9, 7), name = 'iron', callable_class = iron_object, visualize_shape = 'img', img_name = "/images/girder.svg", visualize_size = 1, weight = 100, is_traversable = False, is_movable = True)
            builder.add_object(location = (3, 2), name = 'fire 01', callable_class = fire_object, visualize_shape = 'img', img_name = "/images/fire2.svg", visualize_size = 1.25, smoke = 'fast', is_traversable = True, is_movable = True)
    # complete the world
    add_drop_off_zones(builder, study_version)
    add_agents(builder, name, condition, study_version, resistance, total_fires, victims, task, counterbalance_condition)
    return builder

class victim_object(EnvObject):
    """ class for adding victim objects to the MATRX world """
    def __init__(self, location, name, visualize_shape, img_name):
        super().__init__(location, name, is_traversable = True, is_movable = True,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = 0.9, class_callable = victim_object,
                         is_drop_zone = False, is_goal_block = False, is_collectable = True)

class fire_object(EnvObject):
    """ class for adding fire objects to the MATRX world """
    def __init__(self, location, name, smoke, visualize_shape, img_name, visualize_size, is_traversable, is_movable):
        super().__init__(location, name, smoke = smoke, is_traversable = is_traversable, is_movable = is_movable,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = fire_object,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)
        
class iron_object(EnvObject):
    """ class for adding iron objects to the MATRX world """
    def __init__(self, location, name, weight, visualize_shape, img_name, visualize_size, is_traversable, is_movable):
        super().__init__(location, name, weight = weight, is_traversable = is_traversable, is_movable = is_movable,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = iron_object,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)

class smoke_object(EnvObject):
    """ class for adding smoke objects to the MATRX world """
    def __init__(self, location, name, visualize_shape, img_name, visualize_size):
        super().__init__(location, name, is_traversable = True, is_movable = False,
                         visualize_shape = visualize_shape, img_name = img_name,
                         visualize_size = visualize_size, class_callable = smoke_object,
                         is_drop_zone = False, is_goal_block = False, is_collectable = False)

class dropzone_object(EnvObject):
    """ class for adding dropzone objects to the MATRX world """
    def __init__(self, location, drop_zone_nr, name, visualize_shape, img_name, visualize_opacity):
        super().__init__(location, name, is_traversable = True, is_movable = False,
                         visualize_shape = visualize_shape, img_name = img_name, visualize_opacity = visualize_opacity, 
                         visualize_size = 0.9, class_callable = dropzone_object,
                         visualize_depth = 110, drop_zone_nr = drop_zone_nr,
                         is_drop_zone = False, is_goal_block = True, is_collectable = False)

class collection_goal(WorldGoal):
    """ class that determines the goal og the world and when it should terminate """
    def __init__(self, max_nr_ticks):
        super().__init__()
        # determine max. number of ticks
        self.max_nr_ticks = max_nr_ticks
        # dictionary of all drop locations that contains as key the rank of the to be collected object and as value the location
        # of where it should be dropped, the shape and colour of the block, and the tick number the correct block was delivered. 
        # The rank and tick number is there so we can check if objects are dropped in the right order.
        self.__drop_off = {}
        self.__drop_off_zone = {}
        # track the progess/completeness
        self.__progress = 0    

    def goal_reached(self, grid_world):
        if grid_world.current_nr_ticks >= self.max_nr_ticks:
            return True
        return self.victims_rescued(grid_world)

    def victims_rescued(self, grid_world):
        # find all drop off locations
        if self.__drop_off == {}:
            self.__find_drop_off_locations(grid_world)
        # go through each drop zone and check if the victims are there
        is_satisfied, progress = self.__check_completion(grid_world)
        return is_satisfied

    def progress(self, grid_world):
        # find all drop off locations
        if self.__drop_off == {}:
            self.__find_drop_off_locations(grid_world)
        # go through each drop zone and check if the victims are there
        is_satisfied, progress = self.__check_completion(grid_world)
        # progress in completeness percentage
        self.__progress = progress / sum([len(goal_victims)\
            for goal_victims in self.__drop_off.values()])
        return self.__progress

    def __find_drop_off_locations(self, grid_world):
        # dictionary with as key the zone number and as values a list of the dropzone goal victim objects
        goal_victims = {} 
        # go through all objects and check if object is part of a drop zone
        all_objects = grid_world.environment_objects
        for object_id, object in all_objects.items(): 
            if "drop_zone_nr" in object.properties.keys():
                zone_nr = object.properties["drop_zone_nr"]
                if object.properties["is_goal_block"]:
                    if zone_nr in goal_victims.keys():
                        goal_victims[zone_nr].append(object)
                    else:
                        goal_victims[zone_nr] = [object]
        # go through all drop zones and check the number of rescued victims
        self.__drop_off_zone = {}
        self.__drop_off = {}
        for zone_nr in goal_victims.keys():
            self.__drop_off_zone[zone_nr] = {}
            self.__drop_off[zone_nr] = {}
            # obtain the zone's goal victims
            victims = goal_victims[zone_nr].copy()
            max_rank = len(victims)
            # find the 'bottom' location
            bottom_location = (-np.inf, -np.inf)
            for victim in victims:
                if victim.location[1] > bottom_location[1]:
                    bottom_location = victim.location
            # loop through victims lists and add them to their appropriate ranks
            for rank in range(max_rank):
                location = (bottom_location[0], bottom_location[1] - rank)
                # find the victim at that location and save details
                for victim in victims:
                    if victim.location == location:
                        self.__drop_off_zone[zone_nr][rank] = [location, victim.properties['img_name'][8:-4], None]
                        for zone in self.__drop_off_zone.keys():
                            self.__drop_off[zone] = {}
                            ranking = list(self.__drop_off_zone[zone].values())
                            ranking.reverse()
                            for r in range(len(self.__drop_off_zone[zone].keys())):
                                self.__drop_off[zone][r] = ranking[r]

    def __check_completion(self, grid_world):
        # get the current tick number
        current_tick = grid_world.current_nr_ticks
        # loop through all zones, check the victims and set the tick if satisfied
        for zone_nr, goal_victims in self.__drop_off.items():
            # go through all ranks of this drop off zone
            for rank, victim_data in goal_victims.items():
                location = victim_data[0] 
                shape = victim_data[1]
                tick = victim_data[2]
                # retrieve all objects, the object ids at the location and obtain all victims from it
                all_objects = grid_world.environment_objects
                object_ids = grid_world.get_objects_in_range(location, object_type = EnvObject, sense_range = 0)
                victims = [all_objects[object_id] for object_id in object_ids
                          if object_id in all_objects.keys() and "is_collectable" in all_objects[object_id].properties.keys()]
                victims = [victim for victim in victims if victim.properties["is_collectable"]]
                # check if there is a victim, and if so if it is the right one and the tick is not yet set, then set the current tick.
                if len(victims) > 0 and victims[0].properties['img_name'][8:-4] == shape and tick is None:
                    self.__drop_off[zone_nr][rank][2] = current_tick
                # if there is no victims, reset its tick to None
                elif len(victims) == 0:
                    if self.__drop_off[zone_nr][rank][2] != None:
                        self.__drop_off[zone_nr][rank][2] = None
        # now check if all victims are rescued
        is_satisfied = True
        progress = 0
        for zone_nr, goal_victims in self.__drop_off.items():
            zone_satisfied = True
            ticks = [goal_victims[r][2] for r in range(len(goal_victims))]
            for tick in ticks:
                if tick is not None:
                    progress += 1
            if None in ticks:
                zone_satisfied = False
            # update our satisfied boolean
            is_satisfied = is_satisfied and zone_satisfied
        return is_satisfied, progress