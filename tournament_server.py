import grpc
from concurrent import futures
import tournament_pb2
import tournament_pb2_grpc
import pymongo
import json

class TournamentRegistrationServicer(tournament_pb2_grpc.TournamentRegistrationServicer):
    def __init__(self):
        self.players_by_team = {}
        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["valorant"]
        self.collection = self.db["players"]
        self.matches_collection = self.db["matches"]

    def RegisterPlayer(self, request, context):
        if request.team_name not in self.players_by_team:
            self.players_by_team[request.team_name] = []
        self.players_by_team[request.team_name].append(request)
        print("Received registration request:", request)
        # Save player data to MongoDB
        self.collection.insert_one({
            "name": request.name,
            "role": request.role,
            "age": request.age,
            "team_name": request.team_name,
            "region": request.region
        })
        return request

    def ReadPlayersByTeam(self, request, context):
        team_name = request.team_name
        if team_name in self.players_by_team:
            players = self.players_by_team[team_name]
            response = tournament_pb2.PlayerResponse(players=players)
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Team not found")
            return tournament_pb2.PlayerResponse()

    def UpdatePlayer(self, request, context):
        team_name = request.team_name
        player_name = request.name
        role = request.role
        age = request.age
        new_name = request.new_name
        region = request.region

        if team_name in self.players_by_team:
            for player in self.players_by_team[team_name]:
                if player.name == player_name:
                    # Update player's details
                    player.name = new_name
                    player.role = role
                    player.age = age
                    player.region = region
                    # Update player data in MongoDB
                    self.collection.update_one(
                        {"name": player_name, "team_name": team_name},
                        {"$set": {"name": new_name, "role": role, "age": age, "region": region}}
                    )
                    return player

            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Player {player_name} not found in team {team_name}")
            return tournament_pb2.Player()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Team {team_name} not found")
            return tournament_pb2.Player()

    def DeletePlayer(self, request, context):
        team_name = request.team_name
        player_name = request.name

        if team_name in self.players_by_team:
            players = self.players_by_team[team_name]
            for idx, player in enumerate(players):
                if player.name == player_name:
                    del self.players_by_team[team_name][idx]
                    # Delete player data from MongoDB
                    self.collection.delete_one({"name": player_name, "team_name": team_name})
                    print(f"Deleted player {player_name} from team {team_name}")
                    return tournament_pb2.Player()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Player {player_name} not found in team {team_name}")
            return tournament_pb2.Player()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Team not found")
            return tournament_pb2.Player()

    def CreateBracket(self, request, context):
        teams = request.team_names
        matches = []
        for i in range(0, len(teams) - 1, 2):
            matches.append(tournament_pb2.Match(team1=teams[i], team2=teams[i + 1]))
        response = tournament_pb2.BracketResponse(matches=matches)
        self.matches_collection.insert_one({"bracket": [match.team1 + " vs " + match.team2 for match in matches]})
        return response
    

    def ScheduleMatch(self, request, context):
        match = tournament_pb2.Match(team1=request.team1, team2=request.team2)
        scheduled_time = request.scheduled_time
        self.matches_collection.insert_one({
        "team1": request.team1,
        "team2": request.team2,
        "scheduled_time": scheduled_time
        })
        return tournament_pb2.ScheduleMatchResponse(
            team1=match.team1,
            team2=match.team2,
            scheduled_time=scheduled_time
        )

    def ReadScheduledMatches(self, request, context):
        scheduled_matches = []
        cursor = self.matches_collection.find({}, {"_id": 0, "bracket": 1, "scheduled_time": 1})
        for doc in cursor:
            for match_str in doc["bracket"]:
                teams = match_str.split(" vs ")
                scheduled_matches.append(tournament_pb2.ScheduledMatch(
                    scheduled_time=doc["scheduled_time"],
                    team_1=teams[0],
                    team_2=teams[1]
                ))
        response = tournament_pb2.ScheduledMatchesResponse(matches=scheduled_matches)
        return response
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tournament_pb2_grpc.add_TournamentRegistrationServicer_to_server(TournamentRegistrationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
