import tkinter as tk
from tkinter import ttk
import grpc
import tournament_pb2
import tournament_pb2_grpc

class PlayerApp:
    def __init__(self, root, stub):
        self.stub = stub
        self.root = root
        self.root.title("Tournament Registration System")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.create_tab = ttk.Frame(self.notebook)
        self.read_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.bracket_tab = ttk.Frame(self.notebook)
        self.schedule_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.create_tab, text="Create Player")
        self.notebook.add(self.read_tab, text="Read Players")
        self.notebook.add(self.update_tab, text="Update Player")
        self.notebook.add(self.delete_tab, text="Delete Player")
        self.notebook.add(self.bracket_tab, text="Create Bracket")
        self.notebook.add(self.schedule_tab, text="Schedule Match")

        self.create_player_widgets()
        self.read_players_widgets()
        self.update_player_widgets()
        self.delete_player_widgets()
        self.create_bracket_widgets()
        self.schedule_match_widgets()

    def create_player_widgets(self):
        self.create_label = ttk.Label(self.create_tab, text="Create a new player:")
        self.create_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_label = ttk.Label(self.create_tab, text="Team Name:")
        self.team_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_entry = ttk.Entry(self.create_tab)
        self.team_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.player_name_label = ttk.Label(self.create_tab, text="Player Name:")
        self.player_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.player_name_entry = ttk.Entry(self.create_tab)
        self.player_name_entry.grid(row=2, column=1, padx=10, pady=5)

        self.role_label = ttk.Label(self.create_tab, text="Role:")
        self.role_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.role_entry = ttk.Entry(self.create_tab)
        self.role_entry.grid(row=3, column=1, padx=10, pady=5)

        self.age_label = ttk.Label(self.create_tab, text="Age:")
        self.age_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.age_entry = ttk.Entry(self.create_tab)
        self.age_entry.grid(row=4, column=1, padx=10, pady=5)

        self.region_label = ttk.Label(self.create_tab, text="Region:")
        self.region_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.region_entry = ttk.Entry(self.create_tab)
        self.region_entry.grid(row=5, column=1, padx=10, pady=5)

        self.create_button = ttk.Button(self.create_tab, text="Create Player", command=self.create_player)
        self.create_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_player(self):
        team_name = self.team_name_entry.get()
        name = self.player_name_entry.get()
        role = self.role_entry.get()
        age = int(self.age_entry.get())
        region = self.region_entry.get()

        player = tournament_pb2.Player(
            name=name,
            role=role,
            age=age,
            team_name=team_name,
            region=region
        )

        response = self.stub.RegisterPlayer(player)
        print("Player registration response:", response)

    def read_players_widgets(self):
        self.read_label = ttk.Label(self.read_tab, text="Read players by team:")
        self.read_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_read_label = ttk.Label(self.read_tab, text="Team Name:")
        self.team_name_read_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_read_entry = ttk.Entry(self.read_tab)
        self.team_name_read_entry.grid(row=1, column=1, padx=10, pady=5)

        self.read_button = ttk.Button(self.read_tab, text="Read Players", command=self.read_players_by_team)
        self.read_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.read_text = tk.Text(self.read_tab, wrap="word", height=10, width=50)
        self.read_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def read_players_by_team(self):
        team_name = self.team_name_read_entry.get()

        team_players_request = tournament_pb2.TeamPlayersRequest(team_name=team_name)
        team_players_response = self.stub.ReadPlayersByTeam(team_players_request)

        self.read_text.delete(1.0, tk.END)

        if team_players_response.players:
            self.read_text.insert(tk.END, f"Players in team {team_name}:\n")
            for player in team_players_response.players:
                self.read_text.insert(tk.END, f"Name: {player.name}, Age: {player.age}, Role: {player.role}, Region: {player.region}\n")
        else:
            self.read_text.insert(tk.END, "No players found in the team.")

    def update_player_widgets(self):
        self.update_label = ttk.Label(self.update_tab, text="Update a player:")
        self.update_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_update_label = ttk.Label(self.update_tab, text="Team Name:")
        self.team_name_update_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_update_entry = ttk.Entry(self.update_tab)
        self.team_name_update_entry.grid(row=1, column=1, padx=10, pady=5)

        self.player_name_update_label = ttk.Label(self.update_tab, text="Current Player Name:")
        self.player_name_update_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.player_name_update_entry = ttk.Entry(self.update_tab)
        self.player_name_update_entry.grid(row=2, column=1, padx=10, pady=5)

        self.new_name_label = ttk.Label(self.update_tab, text="New Player Name:")
        self.new_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.new_name_entry = ttk.Entry(self.update_tab)
        self.new_name_entry.grid(row=3, column=1, padx=10, pady=5)

        self.new_role_label = ttk.Label(self.update_tab, text="New Role:")
        self.new_role_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.new_role_entry = ttk.Entry(self.update_tab)
        self.new_role_entry.grid(row=4, column=1, padx=10, pady=5)

        self.new_age_label = ttk.Label(self.update_tab, text="New Age:")
        self.new_age_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.new_age_entry = ttk.Entry(self.update_tab)
        self.new_age_entry.grid(row=5, column=1, padx=10, pady=5)

        self.new_region_label = ttk.Label(self.update_tab, text="New Region:")
        self.new_region_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.new_region_entry = ttk.Entry(self.update_tab)
        self.new_region_entry.grid(row=6, column=1, padx=10, pady=5)

        self.update_button = ttk.Button(self.update_tab, text="Update Player", command=self.update_player)
        self.update_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def update_player(self):
        team_name = self.team_name_update_entry.get()
        name = self.player_name_update_entry.get()
        new_name = self.new_name_entry.get()
        role = self.new_role_entry.get()
        age = int(self.new_age_entry.get())
        region = self.new_region_entry.get()

        update_request = tournament_pb2.UpdatePlayerRequest(
            team_name=team_name,
            name=name,
            new_name=new_name,
            role=role,
            age=age,
            region=region
        )

        response = self.stub.UpdatePlayer(update_request)
        print("Player update response:", response)

    def delete_player_widgets(self):
        self.delete_label = ttk.Label(self.delete_tab, text="Delete a player:")
        self.delete_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_delete_label = ttk.Label(self.delete_tab, text="Team Name:")
        self.team_name_delete_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_delete_entry = ttk.Entry(self.delete_tab)
        self.team_name_delete_entry.grid(row=1, column=1, padx=10, pady=5)

        self.player_name_delete_label = ttk.Label(self.delete_tab, text="Player Name:")
        self.player_name_delete_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.player_name_delete_entry = ttk.Entry(self.delete_tab)
        self.player_name_delete_entry.grid(row=2, column=1, padx=10, pady=5)

        self.delete_button = ttk.Button(self.delete_tab, text="Delete Player", command=self.delete_player)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def delete_player(self):
        team_name = self.team_name_delete_entry.get()
        name = self.player_name_delete_entry.get()

        delete_request = tournament_pb2.DeletePlayerRequest(
            team_name=team_name,
            name=name
        )

        response = self.stub.DeletePlayer(delete_request)
        print("Player delete response:", response)

    def create_bracket_widgets(self):
        self.bracket_label = ttk.Label(self.bracket_tab, text="Create a bracket:")
        self.bracket_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.teams_label = ttk.Label(self.bracket_tab, text="Teams (comma-separated):")
        self.teams_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.teams_entry = ttk.Entry(self.bracket_tab)
        self.teams_entry.grid(row=1, column=1, padx=10, pady=5)

        self.create_bracket_button = ttk.Button(self.bracket_tab, text="Create Bracket", command=self.create_bracket)
        self.create_bracket_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.bracket_text = tk.Text(self.bracket_tab, wrap="word", height=10, width=50)
        self.bracket_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_bracket(self):
        teams = self.teams_entry.get().split(',')
        teams = [team.strip() for team in teams]

        create_bracket_request = tournament_pb2.CreateBracketRequest(team_names=teams)
        create_bracket_response = self.stub.CreateBracket(create_bracket_request)

        self.bracket_text.delete(1.0, tk.END)
        self.bracket_text.insert(tk.END, "Bracket Matches:\n")
        for match in create_bracket_response.matches:
            self.bracket_text.insert(tk.END, f"{match.team1} vs {match.team2}\n")

    def schedule_match_widgets(self):
        self.schedule_label = ttk.Label(self.schedule_tab, text="Schedule a match:")
        self.schedule_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team1_label = ttk.Label(self.schedule_tab, text="Team 1:")
        self.team1_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team1_entry = ttk.Entry(self.schedule_tab)
        self.team1_entry.grid(row=1, column=1, padx=10, pady=5)

        self.team2_label = ttk.Label(self.schedule_tab, text="Team 2:")
        self.team2_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.team2_entry = ttk.Entry(self.schedule_tab)
        self.team2_entry.grid(row=2, column=1, padx=10, pady=5)

        self.time_label = ttk.Label(self.schedule_tab, text="Scheduled Time:")
        self.time_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.time_entry = ttk.Entry(self.schedule_tab)
        self.time_entry.grid(row=3, column=1, padx=10, pady=5)

        self.schedule_button = ttk.Button(self.schedule_tab, text="Schedule Match", command=self.schedule_match)
        self.schedule_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.schedule_text = tk.Text(self.schedule_tab, wrap="word", height=10, width=50)
        self.schedule_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def schedule_match(self):
        team1 = self.team1_entry.get()
        team2 = self.team2_entry.get()
        scheduled_time = self.time_entry.get()

        match_request = tournament_pb2.ScheduleMatchRequest(team1=team1, team2=team2, scheduled_time=scheduled_time)

        try:
            response = self.stub.ScheduleMatch(match_request)
            self.schedule_text.delete(1.0, tk.END)
            self.schedule_text.insert(tk.END, f"Match between {response.team1} and {response.team2} scheduled at {response.scheduled_time}")
        except grpc.RpcError as e:
            self.schedule_text.delete(1.0, tk.END)
            self.schedule_text.insert(tk.END, f"Error: {e.code()} - {e.details()}")
    

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = tournament_pb2_grpc.TournamentRegistrationStub(channel)

    root = tk.Tk()
    app = PlayerApp(root, stub)
    root.mainloop()

if __name__ == '__main__':
    main()
