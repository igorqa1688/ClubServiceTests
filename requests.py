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


# Обновление room_code
def update_club_room_code(room_code: str, room_name: str):
    created_club = add_club(room_code, room_name)
    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.AddClubRequest(
            room_code=generate_random_name(15),
            room_name=generate_guid(),
            guid=created_club.guid)
        try:
            response = stub.AddOrUpdateClub(request)
            return response
        except Exception as e:
            error_data = []
            status_code = e.code()
            error_data.append(status_code.value)
            error_data.append(e.details())
            return error_data


# Обновление room_name
def update_club_room_name(room_code: str, room_name: str):
    created_club = add_club(room_code, room_name)
    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.AddClubRequest(
            room_code=room_code,
            room_name=generate_guid(),
            guid=created_club.guid)

        response = stub.AddOrUpdateClub(request)
        return response


# Получение клуба по guid
def get_club_by_guid():
    created_club = add_club(room_code, room_name)
    print(f"\ncreated_club data by guid:\nguid: {created_club.guid}\nroom_code: {created_club.room_code}\nroom_name: "
          f"{created_club.room_name}\n")

    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.GetClubRequest(

            guid=created_club.guid)

        response = stub.GetClub(request)
        return response


# Получение клуба по room_code
def get_club_by_room_code(room_code: str):
    created_club = add_club(room_code, room_name)
    print(f"\ncreated_club data by room_code:\nguid: {created_club.guid}\nroom_code: {created_club.room_code}\n"
          f"room_name: {created_club.room_name}\n")
    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.GetClubRequest(

            room_code=created_club.room_code)

        response = stub.GetClub(request)
        return response


# Получение клуба по room_code без создания нового клуба
def get_club_by_room_code_without_new_club(room_code: str):
    with grpc.insecure_channel(server) as channel:
        stub = club_service_pb2_grpc.ClubServiceGrpcStub(channel)
        request = club_service_pb2.GetClubRequest(
            room_code=room_code)
        response = stub.GetClub(request)
        return response


if __name__ == "__main__":
    room_name = generate_random_name(15)
    room_code = generate_guid()
    print(get_club_by_room_code(room_code))