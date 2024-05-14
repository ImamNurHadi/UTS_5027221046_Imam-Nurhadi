import tkinter as tk
from tkinter import ttk
import grpc
import tournament_pb2
import tournament_pb2_grpc

class PlayerApp:
    def __init__(self, root, stub):
        self.root = root
        self.stub = stub
        self.root.title("Player Management System")
        
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.create_tab = ttk.Frame(self.notebook)
        self.read_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.create_tab, text="Create Player")
        self.notebook.add(self.read_tab, text="Read Players by Team")
        self.notebook.add(self.update_tab, text="Update Player")
        self.notebook.add(self.delete_tab, text="Delete Player")
        
        self.create_player_widgets()
        self.read_players_widgets()
        self.update_player_widgets()
        self.delete_player_widgets()

    def create_player_widgets(self):
        self.create_label = ttk.Label(self.create_tab, text="Create a new player:")
        self.create_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_label = ttk.Label(self.create_tab, text="Team Name:")
        self.team_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_entry = ttk.Entry(self.create_tab)
        self.team_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.name_label = ttk.Label(self.create_tab, text="Player Name:")
        self.name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self.create_tab)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)

        self.role_label = ttk.Label(self.create_tab, text="Player Role:")
        self.role_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.role_entry = ttk.Entry(self.create_tab)
        self.role_entry.grid(row=3, column=1, padx=10, pady=5)

        self.age_label = ttk.Label(self.create_tab, text="Player Age:")
        self.age_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.age_entry = ttk.Entry(self.create_tab)
        self.age_entry.grid(row=4, column=1, padx=10, pady=5)

        self.create_button = ttk.Button(self.create_tab, text="Create Player", command=self.create_player)
        self.create_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_player(self):
        team_name = self.team_name_entry.get()
        name = self.name_entry.get()
        role = self.role_entry.get()
        age = int(self.age_entry.get())

        player = tournament_pb2.Player(
            name=name,
            role=role,
            age=age,
            team_name=team_name
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

        self.read_button = ttk.Button(self.read_tab, text="Read Players", command=self.read_players)
        self.read_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.players_text = tk.Text(self.read_tab, height=10, width=40)
        self.players_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def read_players(self):
        team_name = self.team_name_read_entry.get()
        team_players_request = tournament_pb2.TeamPlayersRequest(team_name=team_name)
        team_players_response = self.stub.ReadPlayersByTeam(team_players_request)

        self.players_text.delete(1.0, tk.END)
        if team_players_response.players:
            for player in team_players_response.players:
                player_info = f"Name: {player.name}, Age: {player.age}, Role: {player.role}\n"
                self.players_text.insert(tk.END, player_info)
        else:
            self.players_text.insert(tk.END, "No players found in the team.")

    def update_player_widgets(self):
        self.update_label = ttk.Label(self.update_tab, text="Update player details:")
        self.update_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.team_name_update_label = ttk.Label(self.update_tab, text="Team Name:")
        self.team_name_update_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.team_name_update_entry = ttk.Entry(self.update_tab)
        self.team_name_update_entry.grid(row=1, column=1, padx=10, pady=5)

        self.name_update_label = ttk.Label(self.update_tab, text="Player Name:")
        self.name_update_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.name_update_entry = ttk.Entry(self.update_tab)
        self.name_update_entry.grid(row=2, column=1, padx=10, pady=5)

        self.new_name_label = ttk.Label(self.update_tab, text="New Player Name:")
        self.new_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.new_name_entry = ttk.Entry(self.update_tab)
        self.new_name_entry.grid(row=3, column=1, padx=10, pady=5)

        self.role_update_label = ttk.Label(self.update_tab, text="New Player Role:")
        self.role_update_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.role_update_entry = ttk.Entry(self.update_tab)
        self.role_update_entry.grid(row=4, column=1, padx=10, pady=5)

        self.age_update_label = ttk.Label(self.update_tab, text="New Player Age:")
        self.age_update_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.age_update_entry = ttk.Entry(self.update_tab)
        self.age_update_entry.grid(row=5, column=1, padx=10, pady=5)

        self.update_button = ttk.Button(self.update_tab, text="Update Player", command=self.update_player)
        self.update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def update_player(self):
        team_name = self.team_name_update_entry.get()
        player_name = self.name_update_entry.get()
        new_name = self.new_name_entry.get()
        role = self.role_update_entry.get()
        age = int(self.age_update_entry.get())

        update_request = tournament_pb2.UpdatePlayerRequest(
            team_name=team_name,
            name=player_name,
            new_name=new_name,
            role=role,
            age=age
        )

        response = self.stub.UpdatePlayer(update_request)
        print("Player update response:", response)

    def delete_player_widgets(self):
        self.delete_label = ttk.Label(self.delete_tab, text="Delete a player:")
        self.delete_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.name_delete_label = ttk.Label(self.delete_tab, text="Player Name:")
        self.name_delete_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.name_delete_entry = ttk.Entry(self.delete_tab)
        self.name_delete_entry.grid(row=1, column=1, padx=10, pady=5)

        self.team_name_delete_label = ttk.Label(self.delete_tab, text="Team Name:")
        self.team_name_delete_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.team_name_delete_entry = ttk.Entry(self.delete_tab)
        self.team_name_delete_entry.grid(row=2, column=1, padx=10, pady=5)

        self.delete_button = ttk.Button(self.delete_tab, text="Delete Player", command=self.delete_player)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def delete_player(self):
        player_name = self.name_delete_entry.get()
        team_name = self.team_name_delete_entry.get()

        delete_request = tournament_pb2.DeletePlayerRequest(
            name=player_name,
            team_name=team_name
        )

        response = self.stub.DeletePlayer(delete_request)
        print("Player delete response:", response)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = tournament_pb2_grpc.TournamentRegistrationStub(channel)

    root = tk.Tk()
    app = PlayerApp(root, stub)
    root.mainloop()

if __name__ == "__main__":
    main()
