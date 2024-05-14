import grpc
import tournament_pb2
import tournament_pb2_grpc

def create_player(stub):
    # Get team name first
    team_name = input("Enter team name: ")
    name = input("Enter player name: ")
    role = input("Enter player role: ")
    age = int(input("Enter player age: "))

    player = tournament_pb2.Player(
        name=name,
        role=role,
        age=age,
        team_name=team_name
    )

    response = stub.RegisterPlayer(player)
    print("Player registration response:", response)

def read_players_by_team(stub):
    # Get team name first
    team_name = input("Enter team name to read players: ")

    team_players_request = tournament_pb2.TeamPlayersRequest(team_name=team_name)
    team_players_response = stub.ReadPlayersByTeam(team_players_request)

    if team_players_response.players:
        print(f"Players in team {team_name}:")
        for player in team_players_response.players:
            print(f"Name: {player.name}, Age: {player.age}, Role: {player.role}")
    else:
        print("No players found in the team.")

def update_player(stub):
    # Get team name first
    team_name = input("Enter team name: ")

    # Get player name to update
    player_name = input("Enter player name to update: ")

    # Get new player details from user
    new_name = input("Enter new player name: ")
    role = input("Enter new player role: ")
    age = int(input("Enter new player age: "))

    # Create a request object with updated player details
    update_request = tournament_pb2.UpdatePlayerRequest(
        team_name=team_name,
        name=player_name,
        new_name=new_name,  # Set new player name
        role=role,
        age=age
    )

    # Call the UpdatePlayer RPC with the updated player request
    response = stub.UpdatePlayer(update_request)

    # Print the response received from the server
    print("Player update response:", response)






def delete_player(stub):
    name = input("Enter player name to delete: ")
    team_name = input("Enter team name: ")

    delete_request = tournament_pb2.DeletePlayerRequest(
        name=name,
        team_name=team_name
    )

    response = stub.DeletePlayer(delete_request)
    print("Player delete response:", response)

def show_menu():
    print("Choose an option:")
    print("1. Create Player")
    print("2. Read Players by Team")
    print("3. Update Player")
    print("4. Delete Player")
    print("0. Exit")

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = tournament_pb2_grpc.TournamentRegistrationStub(channel)

    while True:
        show_menu()
        option = input("Enter option: ")

        if option == "1":
            create_player(stub)
        elif option == "2":
            read_players_by_team(stub)
        elif option == "3":
            update_player(stub)
        elif option == "4":
            delete_player(stub)
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == '__main__':
    run()
