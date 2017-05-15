from nba_py import team
from nba_py.constants import TEAMS

team_list = ['IND', 'BOS']
fid = open('nba_after_loss.txt', 'w')
fid.write("TEAM,WINS,LOSSES,WIN_RATE,LW_TOTAL,LW_OPP,LW_RATE,WLW_TOTAL,WLW_OPP,WLW_RATE\n")
for key in TEAMS:
	print(key)
	team_id = TEAMS[key]['id']
	team_summary = team.TeamSummary(team_id)
	team_summary_info = team_summary.info()[0]
	team_wins = team_summary_info['W']
	team_losses = team_summary_info['L']
	team_win_rate = team_wins/(team_wins+team_losses)
	
	gamelog = team.TeamGameLogs(team_id).info()
	gamelog.reverse()

	LW_opp = 0	
	LW_total = 0
	
	for g in range(1,len(gamelog)):
		if gamelog[g-1]['WL'] == 'L':
			LW_opp += 1
			if gamelog[g]['WL'] == 'W':
				LW_total += 1
	
	LW_rate = LW_total / LW_opp
	
	WLW_opp = 0
	WLW_total = 0
	for g in range(2,len(gamelog)):
		if gamelog[g-2]['WL'] == 'W' and gamelog[g-1]['WL'] == 'L':
			WLW_opp += 1
			if gamelog[g]['WL'] == 'W':
				WLW_total += 1
	
	WLW_rate = WLW_total / WLW_opp
			
	fid.write("%s,%d,%d,%f,%d,%d,%f,%d,%d,%f\n" % (key,team_wins,team_losses,team_win_rate,LW_total,LW_opp,LW_rate,WLW_total,WLW_opp,WLW_rate))
	
fid.close()

