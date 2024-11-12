import numpy as np
from matrx.actions.action import Action, ActionResult
from matrx.objects.agent_body import AgentBody
from matrx.objects.standard_objects import AreaTile
from matrx.actions.object_actions import _is_drop_poss, _act_drop, _possible_drop, _find_drop_loc, GrabObjectResult
from matrx.objects import EnvObject
from matrx.utils import get_distance
import random

class AddObject(Action):
    """ An action that can add an object to the gridworld. """

    def __init__(self, duration_in_ticks=0):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, **kwargs):
        return AddObjectResult(AddObjectResult.ACTION_SUCCEEDED, True)

    def mutate(self, grid_world, agent_id, **kwargs):
        for i in range(len(kwargs['add_objects'])):
            obj_body_args = {
                "location": kwargs['add_objects'][i]['location'],
                "name": kwargs['add_objects'][i]['name'],
                "class_callable": EnvObject,
                "is_traversable": kwargs['add_objects'][i]['is_traversable'],
                "is_movable": kwargs['add_objects'][i]['is_movable'],
                "visualize_size": kwargs['add_objects'][i]['visualize_size'],
                "visualize_opacity": kwargs['add_objects'][i]['visualize_opacity'],
                "img_name": kwargs['add_objects'][i]['img_name']
            }
        
            env_object = EnvObject(**obj_body_args)
            grid_world._register_env_object(env_object)


        return AddObjectResult(AddObjectResult.ACTION_SUCCEEDED, True)
    
class AddObjectResult(ActionResult):
    """ Result of add object action """
    NO_AGENTBRAIN = "No object passed under the `agentbrain` key in kwargs"
    NO_AGENTBODY = "No object passed under the `agentbody` key in kwargs"
    ACTION_SUCCEEDED = "Object was succesfully added to the gridworld."

    def __init__(self, result, succeeded):
        super().__init__(result, succeeded)

class Idle(Action):
    """ Action of remaining idle. Displays the image of the firefighter icon again when executed by a firefighter. """
    def __init__(self, duration_in_ticks=1):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, **kwargs):
        return IdleResult(IdleResult.RESULT_SUCCESS, True)
    
    def mutate(self, grid_world, agent_id, **kwargs):
        if 'fire_fighter' in agent_id or 'robbert' in agent_id or 'sebastiaan' in agent_id:
            reg_ag = grid_world.registered_agents[agent_id]
            reg_ag.change_property("visualize_opacity", 1)
        return IdleResult(IdleResult.RESULT_SUCCESS, True)
    
class IdleResult(ActionResult):
    """ Result of idling actions. """
    RESULT_SUCCESS = 'Idling action successful'
    RESULT_FAILED = 'Failed to idle'

    def __init__(self, result, succeeded):
        super().__init__(result, succeeded)
    
class IdleDisappear(Action):
    """ Action of remaining idle. Removes the image of the firefighter icon when executed by a firefighter. """
    def __init__(self, duration_in_ticks=1):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, **kwargs):
        return IdleResult(IdleResult.RESULT_SUCCESS, True)
    
    def mutate(self, grid_world, agent_id, **kwargs):
        if 'fire_fighter' in agent_id or 'robbert' in agent_id or 'sebastiaan' in agent_id:
            reg_ag = grid_world.registered_agents[agent_id]
            reg_ag.change_property("visualize_opacity", 0)
        return IdleResult(IdleResult.RESULT_SUCCESS, True)

class CarryObject(Action):
    """ Grab and hold objects action. """

    def __init__(self, duration_in_ticks=0):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, world_state, **kwargs):
        object_id = None if 'object_id' not in kwargs else kwargs['object_id']
        grab_range = np.inf if 'grab_range' not in kwargs else kwargs['grab_range']
        max_objects = np.inf if 'max_objects' not in kwargs else kwargs['max_objects']
        if object_id and 'stone' in object_id or object_id and 'rock' in object_id or object_id and 'tree' in object_id:
            return GrabObjectResult(GrabObjectResult.RESULT_OBJECT_UNMOVABLE, False)
        else:
            return _is_possible_grab(grid_world, agent_id=agent_id, object_id=object_id, grab_range=grab_range, max_objects=max_objects) 

    def mutate(self, grid_world, agent_id, world_state, **kwargs):
        assert 'object_id' in kwargs.keys()
        assert 'grab_range' in kwargs.keys()
        assert 'max_objects' in kwargs.keys()
        object_id = kwargs['object_id']
        reg_ag = grid_world.registered_agents[agent_id]
        env_obj = grid_world.environment_objects[object_id]
        env_obj.carried_by.append(agent_id)
        reg_ag.is_carrying.append(env_obj)
        if 'healthy' in object_id and 'human' in agent_id:
            reg_ag.change_property("img_name", "/images/carry-healthy-human.svg")
        if 'mild' in object_id and 'human' in agent_id:
            reg_ag.change_property("img_name", "/images/carry-mild-human.svg")
        if 'mild' in object_id and 'brutus' in agent_id and 'elderly_man' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-granddad-brutus.svg")
        if 'mild' in object_id and 'brutus' in agent_id and 'elderly_woman' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-grandma-brutus.svg")
        if 'mild' in object_id and 'brutus' in agent_id and 'injured_man' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-man-brutus.svg")
        if 'mild' in object_id and 'brutus' in agent_id and 'injured_woman' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-woman-brutus.svg")
        if 'mild' in object_id and 'titus' in agent_id and 'elderly_man' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-granddad-titus2.svg")
        if 'mild' in object_id and 'titus' in agent_id and 'elderly_woman' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-grandma-titus2.svg")
        if 'mild' in object_id and 'titus' in agent_id and 'injured_man' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-man-titus2.svg")
        if 'mild' in object_id and 'titus' in agent_id and 'injured_woman' in object_id:
            reg_ag.change_property("img_name", "/images/evacuate-woman-titus2.svg")
        if 'critical' in object_id and 'fire_fighter' in agent_id:
            reg_ag.change_property("img_name", "/images/carry-critical-human.svg")
        succeeded = grid_world.remove_from_grid(object_id=env_obj.obj_id, remove_from_carrier=False)
        if not succeeded:
            return GrabObjectResult(GrabObjectResult.FAILED_TO_REMOVE_OBJECT_FROM_WORLD.replace("{OBJECT_ID}", env_obj.obj_id), False)
        env_obj.location = reg_ag.location

        return GrabObjectResult(GrabObjectResult.RESULT_SUCCESS, True)


class GrabObjectResult(ActionResult):
    """Result of the carry action. """
    RESULT_SUCCESS = 'Grab action success'
    FAILED_TO_REMOVE_OBJECT_FROM_WORLD = 'Grab action failed; could not remove object with id {OBJECT_ID} from grid.'
    NOT_IN_RANGE = 'Object not in range'
    RESULT_AGENT = 'This is an agent, cannot be picked up'
    RESULT_NO_OBJECT = 'No Object specified'
    RESULT_CARRIES_OBJECT = 'Agent already carries the maximum amount of objects'
    RESULT_OBJECT_CARRIED = 'Object is already carried by {AGENT_ID}'
    RESULT_UNKNOWN_OBJECT_TYPE = 'obj_id is no Agent and no Object, unknown what to do'
    RESULT_OBJECT_UNMOVABLE = 'Object is not movable'

    def __init__(self, result, succeeded):
        super().__init__(result, succeeded)

class Drop(Action):
    """ Drops a carried object. """
    
    def __init__(self, duration_in_ticks=0):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, world_state, **kwargs):
        reg_ag = grid_world.registered_agents[agent_id]
        drop_range = 1 if 'drop_range' not in kwargs else kwargs['drop_range']
        if 'object_id' in kwargs:
            obj_id = kwargs['object_id']
        elif len(reg_ag.is_carrying) > 0:
            obj_id = reg_ag.is_carrying[-1].obj_id
        else:
            return DropObjectResult(DropObjectResult.RESULT_NO_OBJECT, False)
        return _possible_drop(grid_world, agent_id=agent_id, obj_id=obj_id, drop_range=drop_range)

    def mutate(self, grid_world, agent_id, world_state, **kwargs):
        reg_ag = grid_world.registered_agents[agent_id]
        if 'brutus' in agent_id:
            reg_ag.change_property("img_name", "/images/robot-final4.svg")
        if 'titus' in agent_id:
            reg_ag.change_property("img_name", "/images/final-titus2.svg")
        if 'fire_fighter' in agent_id:
            reg_ag.change_property("img_name", "/images/rescue-man-final3.svg")
            reg_ag.change_property("visualize_opacity", 0)
        drop_range = 1 if 'drop_range' not in kwargs else kwargs['drop_range']
        if 'object_id' in kwargs:
            obj_id = kwargs['object_id']
            env_obj = [obj for obj in reg_ag.is_carrying if obj.obj_id == obj_id][0]
        elif len(reg_ag.is_carrying) > 0:
            env_obj = reg_ag.is_carrying[-1]
        else:
            return DropObjectResult(DropObjectResult.RESULT_NO_OBJECT_CARRIED, False)
        if not env_obj.is_traversable and not reg_ag.is_traversable and drop_range == 0:
            raise Exception(
                f"Intraversable agent {reg_ag.obj_id} can only drop the intraversable object {env_obj.obj_id} at its "
                f"own location (drop_range = 0), but this is impossible. Enlarge the drop_range for the DropAction to "
                f"atleast 1")
        curr_loc_drop_poss = _is_drop_poss(grid_world, env_obj, reg_ag.location, agent_id)
        if curr_loc_drop_poss:
            return _act_drop(grid_world, agent=reg_ag, env_obj=env_obj, drop_loc=reg_ag.location)
        elif not curr_loc_drop_poss and drop_range == 0:
            return DropObjectResult(DropObjectResult.RESULT_OBJECT, False)
        drop_loc = _find_drop_loc(grid_world, reg_ag, env_obj, drop_range, reg_ag.location)
        if not drop_loc:
            return DropObjectResult(DropObjectResult.RESULT_OBJECT, False)
        return _act_drop(grid_world, agent=reg_ag, env_obj=env_obj, drop_loc=drop_loc)


class DropObjectResult(ActionResult):
    """ Result of drop action. """
    RESULT_SUCCESS = 'Drop action success'
    RESULT_NO_OBJECT = 'The item is not carried'
    RESULT_NONE_GIVEN = "'None' used as input id"
    RESULT_AGENT = 'Cannot drop item on an agent'
    RESULT_OBJECT = 'Cannot drop item on another intraversable object'
    RESULT_UNKNOWN_OBJECT_TYPE = 'Cannot drop item on an unknown object'
    RESULT_NO_OBJECT_CARRIED = 'Cannot drop object when none carried'

    def __init__(self, result, succeeded, obj_id=None):
        super().__init__(result, succeeded)
        self.obj_id = obj_id


def _is_possible_grab(grid_world, agent_id, object_id, grab_range, max_objects):
    """ Private MATRX method that checks if object can be grabbed by an agent. """
    reg_ag = grid_world.registered_agents[agent_id]
    loc_agent = reg_ag.location
    if object_id is None:
        return GrabObjectResult(GrabObjectResult.RESULT_NO_OBJECT, False)
    if len(reg_ag.is_carrying) >= max_objects:
        return GrabObjectResult(GrabObjectResult.RESULT_CARRIES_OBJECT, False)
    objects_in_range = grid_world.get_objects_in_range(loc_agent, object_type="*", sense_range=grab_range)
    objects_in_range.pop(agent_id)
    if not object_id:
        for obj in list(objects_in_range.keys()):
            if obj not in grid_world.environment_objects.keys():
                objects_in_range.pop(obj)
        if objects_in_range:
            object_id = grid_world.rnd_gen.choice(list(objects_in_range.keys()))
        else:
            return GrabObjectResult(GrabObjectResult.NOT_IN_RANGE, False)
    if object_id not in objects_in_range:
        return GrabObjectResult(GrabObjectResult.NOT_IN_RANGE, False)
    if object_id in grid_world.registered_agents.keys():
        return GrabObjectResult(GrabObjectResult.RESULT_AGENT, False)
    if object_id in grid_world.environment_objects.keys():
        env_obj = grid_world.environment_objects[object_id] 
        if len(env_obj.carried_by) != 0:
            return GrabObjectResult(GrabObjectResult.RESULT_OBJECT_CARRIED.replace("{AGENT_ID}", str(env_obj.carried_by)), False)
        elif not env_obj.properties["is_movable"]:
            return GrabObjectResult(GrabObjectResult.RESULT_OBJECT_UNMOVABLE, False)
        else:
            return GrabObjectResult(GrabObjectResult.RESULT_SUCCESS, True)
    else:
        return GrabObjectResult(GrabObjectResult.RESULT_UNKNOWN_OBJECT_TYPE, False)

def _act_drop(grid_world, agent, env_obj, drop_loc):
    """ Private MATRX method that drops the carried object. """
    agent.is_carrying.remove(env_obj)
    env_obj.carried_by.remove(agent.obj_id)
    env_obj.location = drop_loc
    grid_world._register_env_object(env_obj, ensure_unique_id=False)
    return DropObjectResult(DropObjectResult.RESULT_SUCCESS, True)


def _is_drop_poss(grid_world, env_obj, drop_location, agent_id):
    """ Private MATRX method that used a breadth first search to find the closest drop location.  """
    objs_at_loc = grid_world.get_objects_in_range(drop_location, object_type="*", sense_range=0)
    for key in list(objs_at_loc.keys()):
        if AreaTile.__name__ in objs_at_loc[key].class_inheritance:
            objs_at_loc.pop(key)
    if agent_id in objs_at_loc.keys():
        objs_at_loc.pop(agent_id)
    in_trav_objs_count = 1 if not env_obj.is_traversable else 0
    in_trav_objs_count += len([obj for obj in objs_at_loc if not objs_at_loc[obj].is_traversable])
    if in_trav_objs_count >= 1 and (len(objs_at_loc) + 1) >= 2:
        return False
    else:
        return True


def _possible_drop(grid_world, agent_id, obj_id, drop_range):
    """ Private MATRX method that checks if an object can be dropped by an agent. """
    reg_ag = grid_world.registered_agents[agent_id]
    loc_agent = reg_ag.location
    loc_obj_ids = grid_world.grid[loc_agent[1], loc_agent[0]]
    if not obj_id:
        return DropObjectResult(DropObjectResult.RESULT_NONE_GIVEN, False)
    if isinstance(obj_id, str) and not any([obj_id == obj.obj_id for obj in reg_ag.is_carrying]):
        return DropObjectResult(DropObjectResult.RESULT_NO_OBJECT, False)
    if len(loc_obj_ids) == 1:
        return DropObjectResult(DropObjectResult.RESULT_SUCCESS, True)
    return DropObjectResult(DropObjectResult.RESULT_SUCCESS, True)


def _find_drop_loc(grid_world, agent, env_obj, drop_range, start_loc):
    """ Private MATRX method that used a breadth first search to find the closest valid drop location. """
    queue = collections.deque([[start_loc]])
    seen = {start_loc}
    width = grid_world.shape[0]
    height = grid_world.shape[1]
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if get_distance([x, y], start_loc) > drop_range:
            return False
        if _is_drop_poss(grid_world, env_obj, [x, y], agent.obj_id):
            return [x, y]
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= x2 < width and 0 <= y2 < height and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
    return False