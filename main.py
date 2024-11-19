import os
import requests
import csv
import glob
import pathlib
from custom_gui import visualization_server
from worlds1.world_builder import create_world

if __name__ == "__main__":
    # check if script is launched locally or using Docker
    is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'
    # if script is launched using Docker, environment variables are extracted from command line input
    if is_docker:
        print("\nRunning from Docker...")
        participant_id = os.getenv('PARTICIPANT_ID', '1')
        environment = os.getenv('ENVIRONMENT_TYPE', 'trial')
    # if script is launched locally, environment variables can be entered as input to the command line
    if not is_docker:
        print("\nRunning locally...")
        print("\nEnter the participant ID:")
        participant_id = input()
        print("\nEnter one of the environments 'trial' or 'experiment':")
        environment = input()
    # build and run the trial/tutorial world
    if environment == "trial":
        print("\nStarting " + environment + " for participant with ID " + participant_id + "...")
        # determine the media folder to use images from
        media_folder = pathlib.Path().resolve()
        # initialize the visualizer
        vis_thread = visualization_server.run_matrx_visualizer(verbose = False, media_folder = media_folder)
        # create and run the MATRX world
        builder = create_world(participant_id = 'na', study_version = 'trial', name = 'Brutus', condition = 'tutorial', task = 'na', counterbalance_condition = 'na')
        builder.startup(media_folder = media_folder)
        world = builder.get_world()
        builder.api_info['matrx_paused'] = False
        world.run(builder.api_info)
    # build and run the experiment world
    if environment == "experiment":
        # check if script is launched from Docker or locally and extract explanation and counterbalancing condition variable accordingly
        if is_docker:
            condition = os.getenv('CONDITION', 'baseline')
        if not is_docker:
            print("\nEnter one of the conditions 'baseline', 'shap', or 'util':")
            condition = input()
        if condition == 'shap' or condition == 'util' or condition == 'baseline':
            if is_docker:
                counterbalance_condition = os.getenv('COUNTERBALANCE_CONDITION', '1')
            if not is_docker:
                print("\nEnter one of the 8 counterbalancing conditions:")
                counterbalance_condition = input()
            # determine robot and task order depending on counteralancing condition
            if counterbalance_condition == '1' or counterbalance_condition == '2':
                robot_order = ['Brutus', 'Titus']
                task_order = [1, 2]
            if counterbalance_condition == '3' or counterbalance_condition == '4':
                robot_order = ['Titus', 'Brutus']
                task_order = [1, 2]
            if counterbalance_condition == '5' or counterbalance_condition == '6':
                robot_order = ['Brutus', 'Titus']
                task_order = [2, 1]
            if counterbalance_condition == '7' or counterbalance_condition == '8':
                robot_order = ['Titus', 'Brutus']
                task_order = [2, 1]
            print("\nStarting " + environment + " with explanation " + condition + " and counterbalancing condition " + counterbalance_condition + " for participant with ID " + participant_id + "...")
            # determine media folder to use images from
            media_folder = pathlib.Path().resolve()
            # initialize the visualizer
            vis_thread = visualization_server.run_matrx_visualizer(verbose = False, media_folder = media_folder)
            # loop through the combination of task and robot to build and run the two tasks in succession
            for i, robot in enumerate(robot_order, start = 0):
                # build and run the MATRX world
                builder = create_world(participant_id = participant_id, study_version = environment, name = robot, condition = condition, task = task_order[i], counterbalance_condition = counterbalance_condition)
                builder.startup(media_folder = media_folder)
                world = builder.get_world()
                builder.api_info['matrx_paused'] = True
                world.run(builder.api_info)
                # get current working directory and logs directory
                current_directory = os.getcwd()
                logs_directory = max(glob.glob(os.path.join(current_directory, '*/counterbalance_' + counterbalance_condition + '/' + participant_id + '/')), key = os.path.getmtime)
                logs_directory = max(glob.glob(os.path.join(logs_directory, '*/')), key = os.path.getmtime)
                # get action and messages log files
                action_file = glob.glob(os.path.join(logs_directory, 'world_1/action*'))[0]
                message_file = glob.glob(os.path.join(logs_directory, 'world_1/message*'))[0]
                # extract important data from log files
                action_header = []
                action_contents = []
                message_header = []
                message_contents = []
                unique_robot_moves = []
                previous_row = None
                # open and read action file and extract the number of unique robot moves
                with open(action_file) as csvfile:
                    reader = csv.reader(csvfile, delimiter = ';', quotechar= "'")
                    for row in reader:
                        if action_header == []:
                            action_header = row
                            continue
                        if row[1:3] not in unique_robot_moves:
                            unique_robot_moves.append(row[1:3])
                        rows = {action_header[i]: row[i] for i in range(len(action_header))}
                        action_contents.append(rows)
                # open and read message file, extract human behavior and save every decision making situation in a seperate csv file
                with open(message_file) as csvfile:
                    reader = csv.reader(csvfile, delimiter = ';', quotechar = "'")
                    for row in reader:
                        if message_header == []:
                            message_header = row
                            continue
                        # save every decision making situation, the predicted moral sensitivity, and human behavior in that situation
                        if row[6:17] != previous_row and row[15] != "":
                            with open(current_directory + '/data/complete_data_decisions.csv', mode = 'a+') as csv_file:
                                csv_writer = csv.writer(csv_file, delimiter = ';', quotechar='"', quoting = csv.QUOTE_MINIMAL)
                                if row[16] == 'CRR_ND_self' or row[16] == 'FRR_MD_self' or row[16] == 'CRR_ND_robot' or row[16] == 'CRR_MD_robot':
                                    csv_writer.writerow([participant_id, condition, counterbalance_condition, task_order[i], row[0], robot, row[16], 'no intervention', row[15]])
                                if row[16] == 'FR_ND_self' or row[16] == 'CR_MD_self':
                                    csv_writer.writerow([participant_id, condition, counterbalance_condition, task_order[i], row[0], robot, row[16], 'allocate to self', row[15]])
                                if row[16] == 'FR_MD_robot' or row[16] == 'FR_ND_robot':
                                    csv_writer.writerow([participant_id, condition, counterbalance_condition, task_order[i], row[0], robot, row[16], 'allocate to robot', row[15]])
                        previous_row = row[6:17]
                        rows = {message_header[i]: row[i] for i in range(len(message_header))}
                        message_contents.append(rows)
                # extract important data from the action and message log files that should be saved in a single output file
                no_ticks = action_contents[-1]['tick_nr']
                completeness = action_contents[-1]['completeness']
                no_messages_human = message_contents[-1]['total_number_messages_human']
                no_messages_robot = message_contents[-1]['total_number_messages_robot']
                firefighter_decisions = message_contents[-1]['firefighter_decisions']
                firefighter_danger = message_contents[-1]['firefighter_danger']
                firefighter_danger_rate = message_contents[-1]['firefighter_danger_rate']
                total_allocations = message_contents[-1]['total_allocations']
                human_allocations = message_contents[-1]['total_allocations_human']
                robot_allocations = message_contents[-1]['total_allocations_robot']
                total_interventions = message_contents[-1]['total_interventions']
                disagreement_rate = message_contents[-1]['disagreement_rate']
                correct_behavior_rate = message_contents[-1]['correct_behavior_rate']
                incorrect_behavior_rate = message_contents[-1]['incorrect_behavior_rate']
                incorrect_intervention_rate = message_contents[-1]['incorrect_intervention_rate']
                correct_intervention_rate = message_contents[-1]['correct_intervention_rate']
                CRR_ND_self = message_contents[-1]['CRR_ND_self']
                FR_ND_self = message_contents[-1]['FR_ND_self']
                FRR_MD_self = message_contents[-1]['FRR_MD_self']
                CR_MD_self = message_contents[-1]['CR_MD_self']
                CRR_MD_robot = message_contents[-1]['CRR_MD_robot']
                FR_MD_robot = message_contents[-1]['FR_MD_robot']
                CRR_ND_robot = message_contents[-1]['CRR_ND_robot']
                FR_ND_robot = message_contents[-1]['FR_ND_robot']
                print("Saving output...")
                # save important information to output files
                with open(os.path.join(logs_directory, 'world_1/output.csv'), mode = 'w') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter = ';', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    csv_writer.writerow(['completeness', 'ticks', 'moves', 'robot_messages', 'human_messages', 'total_allocations', 'human_allocations', 'robot_allocations', 'total_interventions', 
                                         'disagreement_rate', 'correct_behavior_rate', 'incorrect_behavior_rate', 'correct_intervention_rate', 'incorrect_intervention_rate', 'firefighter_decisions', 
                                         'firefighter_danger', 'firefighter_danger_rate', 'CRR_ND_self', 'FR_ND_self', 'FRR_MD_self', 'CR_MD_self', 'CRR_MD_robot', 'FR_MD_robot', 'CRR_ND_robot', 'FR_ND_robot'])

                    csv_writer.writerow([completeness, no_ticks, len(unique_robot_moves), no_messages_robot, no_messages_human, total_allocations, human_allocations, robot_allocations, total_interventions,
                                         disagreement_rate, correct_behavior_rate, incorrect_behavior_rate, correct_intervention_rate, incorrect_intervention_rate, firefighter_decisions,
                                         firefighter_danger, firefighter_danger_rate, CRR_ND_self, FR_ND_self, FRR_MD_self, CR_MD_self, CRR_MD_robot, FR_MD_robot, CRR_ND_robot, FR_ND_robot])
                with open(current_directory + '/data/complete_data_performance.csv', mode = 'a+') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter = ';', quotechar='"', quoting = csv.QUOTE_MINIMAL)
                    csv_writer.writerow([participant_id, condition, counterbalance_condition, task_order[i], row[0], robot, completeness, no_ticks, len(unique_robot_moves), no_messages_robot, no_messages_human, 
                                         total_allocations, human_allocations, robot_allocations, total_interventions, disagreement_rate, correct_behavior_rate, incorrect_behavior_rate, correct_intervention_rate, 
                                         incorrect_intervention_rate, firefighter_decisions, firefighter_danger, firefighter_danger_rate, CRR_ND_self, FR_ND_self, FRR_MD_self, CR_MD_self, CRR_MD_robot, FR_MD_robot, CRR_ND_robot, FR_ND_robot])
        else:
            print("\nWrong condition name entered")
    # shutdown visualizer and stop world
    print("DONE!")
    r = requests.get("http://localhost:" + str(visualization_server.port) + "/shutdown_visualizer")
    vis_thread.join()
    builder.stop()
