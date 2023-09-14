team_wins_losses_draws = ['L', 'D', 'D', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'D', 'W', 'D', 'D', 'W', 'L', 'W', 'L', 'D', 'D', 'L', 'D', 'L', 'D', 'L', 'D', 'L', 'W', 'D', 'W']
team_5g_streak = []

for i in range(len(team_wins_losses_draws)):
    # Pour les 5 premiers matchs, ajoutez '-' pour chaque résultat
    if i < 5:
        streak = ["-"] * (5 - i) + team_wins_losses_draws[:i]
    else:
        # Sinon, ajoutez la série des 5 derniers matchs
        streak = team_wins_losses_draws[i-5:i][::-1]
    team_5g_streak.append(streak)

# Afficher la liste résultante
for streak in team_5g_streak:
    print(streak)

# team_wins_losses_draws = ['L', 'D', 'D', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'D', 'W', 'D', 'D', 'W', 'L', 'W', 'L', 'D', 'D', 'L', 'D', 'L', 'D', 'L', 'D', 'L', 'W', 'D', 'W']
# team_5g_streak = []

# for i in range(len(team_wins_losses_draws)):
#     # Pour les 5 premiers matchs, ajoutez '-' pour chaque résultat et inversez la liste
#     if i < 5:
#         streak = list(reversed(["-"] * (5 - i)))
#     else:
#         # Sinon, ajoutez la série des 5 derniers matchs
#         streak = team_wins_losses_draws[i-5:i]
#     team_5g_streak.append(streak)

# # Afficher la liste résultante
# for streak in team_5g_streak:
#     print(streak)