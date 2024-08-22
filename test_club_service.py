import club_service_pb2_grpc
import club_service_pb2
from functions import generate_guid, generate_random_name, generate_random_number


# Только обязательные поля
def test_add_club(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_guid()
    room_name = generate_random_name(12)
    request = club_service_pb2.AddClubRequest(
    room_code=room_code,
    room_name=room_name
    )

    response = stub.AddOrUpdateClub(request)
    print(f"\nroom_name: {room_name}\n")
    print(f"\nroom_code: {room_code}\n")

    print(f"\n{response}\n")

    assert len(response.guid) == 36
    assert response.room_name == room_name
    assert response.room_code == room_code

