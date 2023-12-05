import numpy as np
GOAL_CENTER = np.array([120,40])
LEFT_POST = np.array([120,36])
RIGHT_POST = np.array([120,44])
BINS = (121,81)
PITCH_DIMS = np.array([[0,120],[0,80]])
GOAL_LEFT_BINNED = np.array([120,36])
GOAL_RIGHT_BINNED = np.array([120,44])
FEET = ['Left Foot','Right Foot']
STATSBOMB_COLUMNS = ["location_shot","shot_first_time_shot","shot_technique_shot","shot_one_on_one_shot","shot_open_goal_shot",
                     "play_pattern_shot","player_shot","season","team_shot","league","shot_statsbomb_xg_shot","position_shot",
                     "pass_type_pass","pass_cross_pass","shot_body_part_shot","pass_height_pass","pass_technique_pass",
                     "goalkeeper_position","shot_freeze_frame_shot","under_pressure_shot","pass_length_pass","play_before_type","shot_outcome_shot"
                     ]