import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, FontManager, Sbopen
import numpy as np
from xg.utils import *
def create_fig(shot_row,t1,t2,t3):
    pitch = VerticalPitch(half=True, goal_type='box', pad_bottom=-20)

# We will use mplsoccer's grid function to plot a pitch with a title axis.
    fig, axs = pitch.grid(figheight=8, endnote_height=0,  # no endnote
                        title_height=0.1, title_space=0.02,
                        # Turn off the endnote/title axis. I usually do this after
                        # I am happy with the chart layout and text placement
                        axis=False,
                        grid_height=0.83)

    # Plot the players
    sc1 = pitch.scatter(t1.x, t1.y, s=600, c='#727cce', label='Attacker', ax=axs['pitch'])
    sc2 = pitch.scatter(t2.x, t2.y, s=600,
                        c='#5ba965', label='Defender', ax=axs['pitch'])
    sc4 = pitch.scatter(t3.x, t3.y, s=600,
                        ax=axs['pitch'], c='#c15ca5', label='Goalkeeper')

    # plot the shot
    sc3 = pitch.scatter(shot_row.x, shot_row.y, marker='football',
                        s=600, ax=axs['pitch'], label='Shooter', zorder=1.2)
 
    # plot the angle to the goal
    pitch.goal_angle(shot_row.x, shot_row.y, ax=axs['pitch'], alpha=0.2, zorder=1.1,
                    color='#cb5a4c', goal='right')

    # fontmanager for google font (robotto)
    robotto_regular = FontManager()

    # plot the jersey numbers
    # add a legend and title
    legend = axs['pitch'].legend(loc='center left', labelspacing=1.5)
    for text in legend.get_texts():
        text.set_fontproperties(robotto_regular.prop)
        text.set_fontsize(20)
        text.set_va('center')

    return fig

def create_plot(shot_row):
    
    freeze = pd.DataFrame(shot_row['freeze_frame'])
    
    nfreeze = format_freeze_data(freeze)
    t1 = nfreeze[nfreeze['teammate']]
    t2 = nfreeze[(~nfreeze['teammate']) & (~nfreeze['isGoalkeeper'])]
    t3 = nfreeze[(~nfreeze['teammate']) & (nfreeze['isGoalkeeper'])]
    f = create_fig(shot_row,t1,t2,t3)
    return f