from xg.constants import *
from xg.math_op import *
from xg.utils import *


def get_statsbomb_features(df,cols=STATSBOMB_COLUMNS):
    """Given statsbomb data read in to the folder Data, get the main columns that will be used also for training/validation."""
    return df[cols]

def is_throughball(pass_technique:str):
    """Return True if pass technique is throughball"""
    return (pass_technique == 'Through Ball')

def is_shot_with_main_foot(player : str, shot_body_part : str, player_footedness : dict):
    """Given a dictionary with player foot preference, change Right/Left foot for Main/Weak foot. If not, just return the value."""
    if shot_body_part in FEET:
       main_foot = player_footedness[player]
       return "Main foot" if shot_body_part == main_foot else "Weak Foot"
    else:
       return shot_body_part 
    
def number_of_opp_player_after_ball_line(shot : np.ndarray,freeze : dict):
    """Given a shot and the freeze frame, count how many opposition players (besides goalkeeper) are after the line ball."""
    yshot = shot[1]
    
    after_ball_line = np.array([True if (p['location'][1] > yshot) and
                       (not p['teammate']) and
                       (p['position']['id'] != 1) else False
                       for p in freeze ])
    
    return after_ball_line.sum()


def is_goal(shot_outcome : str):
    """Return 1 if goal else 0."""
    return int(shot_outcome == 'Goal')


def distance_goalkeeper_to_player(shot : np.ndarray, frame : dict):
    
    """Given shot location and frame, find the distance between shot and keeper.
    If keeper not in frame, returns 30.
    """
    gk = find_gk(frame)
    if gk == "No GK":
        return 30.
    return distance.euclidean(gk['location'],shot)


def distance_to_goal(shot : np.ndarray):
    """Given shot location, gets distance from center of goal."""
    dist = distance.euclidean(shot,GOAL_CENTER)
    return dist

def pressure_radius_function(player : np.ndarray):
    """Function that defines pressure radius on a player, defined by Statsbomb."""
    dist = distance_to_goal(player)
    if dist <= 24:
        return dist*0.15 + 0.85
    else:
        return 4.5

def angle_to_goal(shot : np.ndarray):
    """Given shot location, calculates angle to goal."""
    
    return angle_between_vectors(shot,LEFT_POST,RIGHT_POST)

def goalkeeper_distance_to_goal(freeze_frame:dict):
    """Given freeze frame, find goalkeeper distance to center of goal."""
    gk = find_gk(freeze_frame)
    if gk == "No GK":
        return 30.
    else:
        gk = gk['location']
        return distance.euclidean(gk,GOAL_CENTER)


def create_statistic_bins(x,y,nbins=BINS,_range=PITCH_DIMS,opp=True):
    """Create histogram for gaussian_filter. If opposition player, return histogram matrix. If not, return the 
    the index_loc for the player.
    """
    if opp:
        stat,_,_ = np.histogram2d(x,y,bins=nbins,range=_range)
    else:
        stat = np.array(np.histogram2d([x],[y],bins=nbins,range=_range)[0].nonzero()).ravel()
    return stat


def players_between_goal(shot : np.ndarray,frame : dict):
    """
    Given a shot and the frame, returns a tuple containing (a,b) 
    where:
    
    a. Number of players between the shot and the goal.
    
    b. Number of players in a radius defined by pressure_radius_function.
    
    !!Only outfield players.
    """
    pr = pressure_radius_function(shot)
    
    pos = np.array([p['location'] for p in frame if not p['teammate'] and not p['position']['id']==1.])
    if len(pos) == 0:
        return (0.,0.)
    x,y = pos[:,0], pos[:,1]
    opp_matrix = create_statistic_bins(x,y)
    shot_binned = create_statistic_bins(shot[0],shot[1],opp=False)
    opp_matrix_gaussian = apply_gaussian_filter(opp_matrix)
    a,b = opp_matrix_gaussian.nonzero()
    pairs = np.array(list(zip(a,b)))
    
    
    inside_triangle = np.array([opp_matrix_gaussian[p[0],p[1]] for p in pairs if point_inside_triangle(shot_binned,GOAL_LEFT_BINNED,GOAL_RIGHT_BINNED,p)])
    
    inside_circle = np.array([opp_matrix_gaussian[p[0],p[1]] for p in pairs if point_inside_circle(p,shot_binned,pr)])
    return inside_triangle.sum(),inside_circle.sum()


def goalkeeper_between_goal(shot : np.ndarray,frame : dict):
    """
    Given a shot, returns how much the goalkeeper is between goal.
    If goalkeeper not in frame -> 0
    If not, see how much he is triangle.
    """
    gk = find_gk(frame)
    if gk == "No GK":
        return 0.
    gk_loc= gk['location']
    

    goalkeeper_matrix = create_statistic_bins([gk_loc[0]],[gk_loc[1]])
    shot_binned = create_statistic_bins(shot[0],shot[1],opp=False)
    opp_matrix_gaussian = apply_gaussian_filter(goalkeeper_matrix,radius=2)
    a,b = opp_matrix_gaussian.nonzero()
    pairs = np.array(list(zip(a,b)))
    
    
    inside_triangle = np.array([opp_matrix_gaussian[p[0],p[1]] for p in pairs if point_inside_triangle(shot_binned,GOAL_LEFT_BINNED,GOAL_RIGHT_BINNED,p)])
    
    return inside_triangle.sum()