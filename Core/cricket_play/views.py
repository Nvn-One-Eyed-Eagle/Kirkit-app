from django.shortcuts import render, redirect
from .models import player
import random, json

def home(request):
    errors = []
    teams = []
    constant = None

    if request.method == "POST":
        action = request.POST.get("action")

        # ---- Make Teams ----
        if action == "teams":
            selected_players = request.POST.get("selected_players")
            if selected_players:
                players_list = json.loads(selected_players)

                random.shuffle(players_list)  # shuffle for randomness

                # If odd number of players, randomly select one as common
                if len(players_list) % 2 != 0:
                    # Randomly select a player to be common instead of always taking the last one
                    common_index = random.randint(0, len(players_list)-1)
                    constant = players_list.pop(common_index)
                else:
                    constant = None

                # Form teams of two players each with remaining players
                for i in range(0, len(players_list) - 1, 2):
                    teams.append([players_list[i], players_list[i+1]])

                # store teams in session so main() can access them later
                request.session["teams"] = [" & ".join(t) for t in teams]
                if constant:
                    request.session["constant"] = constant

                profile = player.objects.all()
                return render(request, "game_mode.html", {
                    "teams": teams,
                    "common": constant,
                    "profile": profile
                })

        # ---- Save Player ----
        elif action == "save":
            name = request.POST.get("player_name")
            img  = request.FILES.get("player_img")

            # Validation
            if not name:
                errors.append("Name is required")
            if not img:
                errors.append("Image is required")
            elif not img.content_type.startswith("image/"):
                errors.append("File must be an image")

            if not errors:
                player.objects.create(player_name=name, player_img=img)
                return redirect("home")

    profile = player.objects.all()
    return render(request, "home.html", {
        "profile": profile,
        "errors": errors
    })


def main(request):
    batting_order = request.session.get("batting_order", [])
    teams = request.session.get("teams", [])
    constant = request.session.get("constant", None)
    profile = player.objects.all()

    # Get all players for all teams in batting order
    team_players = []
    if batting_order:
        for team in batting_order:
            team_names = team.split(" & ")
            team_players.extend(player.objects.filter(player_name__in=team_names))
        
        # Add common player if exists
        if constant:
            common_player = player.objects.filter(player_name=constant).first()
            if common_player:
                team_players.append(common_player)

    if request.method == "POST":
        first_team = request.POST.get("first_team")
        batting_order_json = request.POST.get("batting_order")
        
        if batting_order_json:
            # Get batting order from JSON
            batting_order = json.loads(batting_order_json)
            request.session["batting_order"] = batting_order
        elif first_team:
            # Fallback if batting_order is not provided
            batting_order = [first_team] + [t for t in teams if t != first_team]
            request.session["batting_order"] = batting_order

        return redirect("main")

    return render(request, "main.html", {
        "batting_order": batting_order,
        "teams": teams,
        "constant": constant,
        "profile": team_players  # All players from all teams in batting order
    })