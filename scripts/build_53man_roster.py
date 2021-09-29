# build_madden_roster.py
#
# CREATED: 09/28/21
# LAST EDIT: 09/28/21
#
# This script randomly builds a full roster (without the long snapper) consisting of NFL players in Madden 22
#
######################################################################################
# REQUIRED MODULES
######################################################################################
import pandas as pd
import random

######################################################################################
# DATA AND FUNCTIONS
######################################################################################

# Dataframe of all players in Madden 22, data retrieved from u/Pestilence_XIV on Reddit r/Madden
# (https://www.reddit.com/r/Madden/comments/ouzjvd/madden_22_player_ratings_spreadsheet_fully/)
all_players = pd.read_csv('https://raw.githubusercontent.com/pterwoo/misc/main/Madden%2022%20Player%20Ratings%20-%20Launch%20(dist).xlsx%20-%20All%20Players.csv')

# Breakdown of how many players should be in each position
pos_breakdown = {"QB": 3,
                 "WR": 6,
                 "HB": 3,
                 "FB": 1,
                 "TE": 3,
                 "C": 2,
                 "LG": 1,
                 "RG": 1,
                 "LT": 2,
                 "RT": 2,
                 "LE": 2,
                 "RE": 2,
                 "DT": 5,
                 "LOLB": 3,
                 "ROLB": 3,
                 "MLB": 3,
                 "CB": 4,
                 "SS": 2,
                 "FS": 2,
                 "K": 1,
                 "P": 1,}

def GetRandomPlayer(position, n):
  """
    Features:
      - Retrieves random player from the players players database

    Inputs:
      - position: the position of the player
      - n: number of players to choose

    Outputs:
      - pos: dataframe consisting of the player(s) selected
  """
  idx = all_players['Unnamed: 2'] == position
  pos_info = all_players[idx]
  pos = pos_info.sample(n = n)
  return pos

def BuildRoster():
  """
  Features:
    - Builds the full roster and saves it as a csv file in the selected path

  Inputs:
    - None

  Outputs:
    - roster: dataframe containing the full roster
  """
  roster = pd.DataFrame()

  for posit in pos_breakdown:
    num_players = (int(pos_breakdown.get(posit)))
    players = GetRandomPlayer(position = posit, n = num_players )
    roster = roster.append(players)

  roster.to_csv('your_roster.csv')

######################################################################################
# MAIN
######################################################################################
if __name__ == "__main__":
    BuildRoster()

    print('Check your current directory for the file your_roster.csv')



