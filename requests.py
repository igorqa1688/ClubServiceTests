import grpc
import club_service_pb2
import club_service_pb2_grpc
from functions import generate_guid, generate_random_name
from global_vars import server


def add_club(room_code: str, room_name: str):
    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.AddClubRequest(
            room_code=room_code,
            room_name=room_name)
        try:
            response = stub.AddOrUpdateClub(request)
            return response
        except Exception as e:
            print(e)
            return "Error add_club"


def double_add_club(count: int):
    clubs = []
    for i in range(count):
        room_name = generate_random_name(15)
        room_code = generate_guid()
        clubs.append(add_club(room_code, room_name))
    return clubs


if __name__ == "__main__":
    print(double_add_club(2))