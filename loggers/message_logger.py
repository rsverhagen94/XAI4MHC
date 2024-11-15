from matrx.logger.logger import GridWorldLogger
from matrx.grid_world import GridWorld
import copy
import json
import numpy as np
import re

class message_logger(GridWorldLogger):
    """ Logs messages send and received by (all) agents and extracts important information from them such as the number of interventions """

    def __init__(self, save_path="", file_name_prefix="", file_extension=".csv", delimiter=";"):
        super().__init__(save_path=save_path, file_name=file_name_prefix, file_extension=file_extension,
                         delimiter=delimiter, log_strategy=1)
        self._threshold = None

    def log(self, grid_world, agent_data):
        # log important information extracted from messages such as disagreement rate
        log_data = {
            'threshold': '',
            'total_number_messages_human': 0,
            'total_number_messages_robot': 0,
            'firefighter_decisions': 0,
            'firefighter_danger': 0,
            'firefighter_danger_rate': 0,
            'total_allocations_human': 0,
            'total_allocations_robot': 0,
            'total_allocations': 0,
            'total_interventions': 0,
            'disagreement_rate': 0,
            'correct_behavior_rate': 0,
            'incorrect_behavior_rate': 0,
            'incorrect_intervention_rate': 0,
            'correct_intervention_rate': 0,
            'sensitivity': '',
            'decision': '',
            # correct rejection of reallocation of normal decision (< 4.2 moral sensitivity) to self (i.e., no intervention to self for normal decision)
            'CRR_ND_self': 0,
            # false reallocation of normal decision to self
            'FR_ND_self': 0,
            # false rejection of reallocation of moral decision (>= 4.2 moral sensitivity) to self
            'FRR_MD_self': 0,
            # false reallocation of normal decision to robot
            'FR_ND_robot': 0,
            # correct rejection of reallocation of normal decision to robot
            'CRR_ND_robot': 0,
            # correct reallocation of moral decision to self
            'CR_MD_self': 0,
            # correct rejection of reallocation of moral decision to robot
            'CRR_MD_robot': 0,
            # false reallocation of moral decision to robot
            'FR_MD_robot': 0}
        # initialize the variables to extract
        gwmm = grid_world.message_manager
        ticks = grid_world.current_nr_ticks - 1
        tot_messages_human = 0
        tot_messages_robot = 0
        firefighter_danger = 0
        firefighter_decisions = 0
        tot_allocations_human = 0
        tot_allocations_robot = 0
        CRR_ND_self = 0
        FR_ND_self = 0
        FRR_MD_self = 0
        CR_MD_self = 0
        CRR_MD_robot = 0
        FR_MD_robot = 0
        CRR_ND_robot = 0
        FR_ND_robot = 0
        sensitivity = ''
        decision = ''
        processed_messages = []
        # loop over all ticks
        for tick in range(0, ticks):
            if tick in gwmm.preprocessed_messages.keys():
                # loop over all processed messages
                for message in gwmm.preprocessed_messages[tick]:
                    # extract threshold/level of agent autonomy
                    if 'Counterbalancing' in message.content:
                        self._threshold = message.content.split()[6]
                    # only process non-hidden messages
                    if (tick, message.content) not in processed_messages and 'Time left: ' not in message.content and 'Smoke spreads: ' not in message.content and 'Coordinates vic' not in message.content and 'Target' not in message.content \
                        and 'Temperature: ' not in message.content and 'Location: ' not in message.content and 'Distance: ' not in message.content and 'Victims rescued: ' not in message.content and 'Counterbalancing' not in message.content and 'Current tick is' not in message.content:
                        processed_messages.append((tick, message.content))
                        # classify human behavior in relation to threshold, intervention, and moral sensitivity
                        if 'No intervention' in message.content and self._threshold == '5.0' and float(message.content.split()[6]) < 4.2:
                            CRR_ND_self += 1
                            decision = 'CRR_ND_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[6])
                        if 'No intervention' in message.content and self._threshold == '5.0' and float(message.content.split()[6]) >= 4.2 and float(message.content.split()[6]) <= 5:
                            FRR_MD_self += 1
                            decision = 'FRR_MD_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[6])
                        if 'No intervention' in message.content and self._threshold == '5.0' and float(message.content.split()[6]) > 5:
                            CRR_MD_robot += 1
                            decision = 'CRR_MD_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[6])
                        if 'No intervention' in message.content and self._threshold == '3.5' and float(message.content.split()[6]) < 3.5:
                            CRR_ND_self += 1
                            decision = 'CRR_ND_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[6])
                        if 'No intervention' in message.content and self._threshold == '3.5' and float(message.content.split()[6]) >= 3.5 and float(message.content.split()[6]) < 4.2:
                            CRR_ND_robot += 1
                            decision = 'CRR_ND_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[6])
                        if 'No intervention' in message.content and self._threshold == '3.5' and float(message.content.split()[6]) >= 4.2:
                            CRR_MD_robot += 1
                            decision = 'CRR_MD_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[6])
                        if 'Reallocating' in message.content and 'to you' in message.content and self._threshold == '5.0' and float(message.content.split()[9]) < 4.2:
                            FR_ND_self += 1
                            decision = 'FR_ND_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[9])
                        if 'Reallocating' in message.content and 'to you' in message.content and self._threshold == '5.0' and float(message.content.split()[9]) >= 4.2 and float(message.content.split()[9]) <= 5:
                            CR_MD_self += 1
                            decision = 'CR_MD_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[9])
                        if 'Reallocating' in message.content and 'to you' in message.content and self._threshold == '3.5' and float(message.content.split()[9]) <= 3.5:
                            FR_ND_self += 1
                            decision = 'FR_ND_self'
                            tot_allocations_robot += 1
                            sensitivity = float(message.content.split()[9])
                        if 'Reallocating' in message.content and 'to me' in message.content and self._threshold == '5.0' and float(message.content.split()[9]) > 5:
                            FR_MD_robot += 1
                            decision = 'FR_MD_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[9])
                        if 'Reallocating' in message.content and 'to me' in message.content and self._threshold == '3.5' and float(message.content.split()[9]) > 3.5 and float(message.content.split()[9]) < 4.2:
                            FR_ND_robot += 1
                            decision = 'FR_ND_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[9])
                        if 'Reallocating' in message.content and 'to me' in message.content and self._threshold == '3.5' and float(message.content.split()[9]) >= 4.2:
                            FR_MD_robot += 1
                            decision = 'FR_MD_robot'
                            tot_allocations_human += 1
                            sensitivity = float(message.content.split()[9])
                        # keep track of the number of human and robot messages sent
                        if 'human' in message.from_id:
                            tot_messages_human += 1
                        if 'Titus' in message.from_id and 'No intervention' not in message.content or 'Brutus' in message.from_id and 'No intervention' not in message.content:
                            tot_messages_robot += 1
                        # keep track of how often firefighters aborted tasks and were involved in decisions
                        if 'ABORTING TASK' in message.content:
                            firefighter_danger += 1
                        if 'Sending in' in message.content and 'Not sending in' not in message.content:
                            firefighter_decisions += 1

        # add extracted information to the logs
        log_data['threshold'] = self._threshold
        log_data['total_number_messages_human'] = tot_messages_human
        log_data['total_number_messages_robot'] = tot_messages_robot
        log_data['total_allocations_human'] = tot_allocations_human
        log_data['total_allocations_robot'] = tot_allocations_robot
        log_data['firefighter_danger'] = firefighter_danger
        log_data['firefighter_decisions'] = firefighter_decisions
        log_data['sensitivity'] = sensitivity
        log_data['decision'] = decision
        if firefighter_decisions > 0:
            log_data['firefighter_danger_rate'] = firefighter_danger / firefighter_decisions
        # add threshold specific information to the logs
        if self._threshold == '5.0':
            tot_allocations = CRR_ND_self + FR_ND_self + FRR_MD_self + CR_MD_self + CRR_MD_robot + FR_MD_robot
            tot_interventions = FR_ND_self + CR_MD_self + FR_MD_robot
            correct_behavior = CRR_ND_self + CR_MD_self + CRR_MD_robot
            incorrect_behavior = FR_ND_self + FRR_MD_self + FR_MD_robot
            incorrect_interventions = FR_ND_self  + FR_MD_robot
            correct_interventions = CR_MD_self
            log_data['CRR_ND_self'] = CRR_ND_self
            log_data['FR_ND_self'] = FR_ND_self
            log_data['FRR_MD_self'] = FRR_MD_self
            log_data['CR_MD_self'] = CR_MD_self
            log_data['CRR_MD_robot'] = CRR_MD_robot
            log_data['FR_MD_robot'] = FR_MD_robot
            log_data['CRR_ND_robot'] = ''
            log_data['FR_ND_robot'] = ''
            log_data['total_allocations'] = tot_allocations
            log_data['total_interventions'] = tot_interventions
            if tot_allocations > 0:
                log_data['disagreement_rate'] = tot_interventions / tot_allocations
                log_data['correct_behavior_rate'] = correct_behavior / tot_allocations
                log_data['incorrect_behavior_rate'] = incorrect_behavior / tot_allocations
            if tot_interventions > 0:
                log_data['incorrect_intervention_rate'] = incorrect_interventions / tot_interventions
                log_data['correct_intervention_rate'] = correct_interventions / tot_interventions
        if self._threshold == '3.5':
            tot_allocations = CRR_ND_self + FR_ND_self + CRR_ND_robot + FR_ND_robot + CRR_MD_robot + FR_MD_robot
            tot_interventions = FR_ND_self + FR_ND_robot + FR_MD_robot
            correct_behavior = CRR_ND_self + CRR_ND_robot + CRR_MD_robot
            incorrect_behavior = FR_ND_self + FR_ND_robot + FR_MD_robot
            log_data['CRR_ND_self'] = CRR_ND_self
            log_data['FR_ND_self'] = FR_ND_self
            log_data['CRR_ND_robot'] = CRR_ND_robot
            log_data['FR_ND_robot'] = FR_ND_robot
            log_data['CRR_MD_robot'] = CRR_MD_robot
            log_data['FR_MD_robot'] = FR_MD_robot
            log_data['FRR_MD_self'] = ''
            log_data['CR_MD_self'] = ''
            log_data['correct_intervention_rate'] = ''
            log_data['incorrect_intervention_rate'] = ''
            log_data['total_allocations'] = tot_allocations
            log_data['total_interventions'] = tot_interventions
            if tot_allocations > 0:
                log_data['disagreement_rate'] = tot_interventions / tot_allocations
                log_data['correct_behavior_rate'] = correct_behavior / tot_allocations
                log_data['incorrect_behavior_rate'] = incorrect_behavior / tot_allocations

        return log_data