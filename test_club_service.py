import club_service_pb2_grpc
import club_service_pb2
from functions import generate_guid, generate_random_name, generate_random_number
from requests import add_club, get_club_by_room_code_without_new_club


# Только обязательные поля
def test_add_club_required_field(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(12)
    room_name = generate_random_name(12)
    request = club_service_pb2.AddClubRequest(
    room_code=room_code,
    room_name=room_name)

    response = stub.AddOrUpdateClub(request)

    assert len(response.guid) == 36
    assert response.room_name == room_name
    assert response.room_code == room_code


# Добавление клуба, room_code не заполнен
def test_add_club_without_room_code(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = ""
    room_name = generate_random_name(12)
    try:
        request = club_service_pb2.AddClubRequest(
            room_code=room_code,
            room_name=room_name)

        response = stub.AddOrUpdateClub(request)

        assert len(response.guid) == 0
    except Exception as e:
        status_code = e.code()
        grpc_details = e.details()
        assert status_code.value[0] == 3
        assert grpc_details == "Room Code empty value not allowed"


# Добавление клуба, передан несуществующий guid
def test_add_club_with_nonexist_guid(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    nonexist_guid = generate_guid()

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=room_name,
        guid=nonexist_guid)

    response = stub.AddOrUpdateClub(request)

    assert response.guid == nonexist_guid
    assert response.room_name == room_name
    assert response.room_code == room_code


# Добавление клуба, room_name не заполнен
def test_add_club_without_room_name(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(12)
    room_name = ""

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=room_name)

    response = stub.AddOrUpdateClub(request)
    print(response)
    assert len(response.guid) == 36
    assert response.room_code == room_code
    assert len(response.room_name) == 0


# Добавление клуба с существующим room_code
def test_add_club_exist_room_code(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(12)
    room_name = generate_random_name(12)
    new_room_name = generate_random_name(15)
    created_club = add_club(room_code, room_name)

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=new_room_name
    )

    response = stub.AddOrUpdateClub(request)

    assert len(response.guid) == 36
    assert response.room_name == new_room_name
    assert response.room_code == room_code
    assert response.room_code == created_club.room_code


# Добавление клуба с существующим room_name
def test_add_club_exist_room_name(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(12)
    room_name = generate_random_name(12)
    new_room_code = generate_random_name(15)
    created_club = add_club(room_code, room_name)

    request = club_service_pb2.AddClubRequest(
        room_code=new_room_code,
        room_name=room_name
    )

    response = stub.AddOrUpdateClub(request)

    assert len(response.guid) == 36
    assert response.room_name == room_name
    assert response.room_code == new_room_code
    assert response.room_name == created_club.room_name


# Добавление клуба с существующим rom_name
def test_add_club(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    room_code = generate_random_name(12)
    room_name = generate_random_name(12)
    created_club = add_club(room_code, room_name)

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=room_name
    )

    response = stub.AddOrUpdateClub(request)

    get_created_club = get_club_by_room_code_without_new_club(room_code)

    assert len(response.guid) == 36
    assert response.room_name == room_name
    assert response.room_code == room_code


# Тест обнвления клуба - обновление room_name
def test_update_room_name(grpc_channel):
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    new_room_name = generate_random_name(32)
    created_club = add_club(room_code, room_name)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=new_room_name,
        guid=created_club.guid)

    response = stub.AddOrUpdateClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == new_room_name
    assert response.room_code == room_code


# Тест обнвления клуба - без внесения изменения
def test_update_without_change(grpc_channel):
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    created_club = add_club(room_code, room_name)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.AddClubRequest(
        room_code=room_code,
        room_name=room_name,
        guid=created_club.guid)

    response = stub.AddOrUpdateClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == room_name
    assert response.room_code == room_code


# Тест обнвления клуба - обновление room_code
def test_update_room_code(grpc_channel):
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    new_room_code = generate_random_name(16)
    created_club = add_club(room_code, room_name)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.AddClubRequest(
        room_code=new_room_code,
        room_name=room_name,
        guid=created_club.guid)

    response = stub.AddOrUpdateClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == room_name
    assert response.room_code == new_room_code


# Тест получения клуба по guid
def test_get_club_by_guid(grpc_channel):
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    created_club = add_club(room_code, room_name)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.GetClubRequest(
        guid=created_club.guid)

    response = stub.GetClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == created_club.room_name
    assert response.room_code == created_club.room_code


# Тест получения клуба по room_code
def test_get_club_by_room_code(grpc_channel):
    room_code = generate_random_name(15)
    room_name = generate_random_name(12)
    created_club = add_club(room_code, room_name)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.GetClubRequest(
        room_code=created_club.room_code)

    response = stub.GetClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == created_club.room_name
    assert response.room_code == created_club.room_code


# Тест получения клуба по room_code
def test_get_club_by_invalid_room_code(grpc_channel):
    room_code = generate_random_name(15)

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    try:
        request = club_service_pb2.GetClubRequest(
            room_code=room_code)

        response = stub.GetClub(request)
        assert response.guid == 0
    except Exception as e:
        status_code = e.code()
        assert status_code.value[0] == 5


# Тест получения клуба по  несуществующему guid
def test_get_club_by_invalid_guid(grpc_channel):
    guid = generate_guid()

    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)
    try:
        request = club_service_pb2.GetClubRequest(
            guid=guid)

        response = stub.GetClub(request)
        assert response.guid == 0
    except Exception as e:
        status_code = e.code()
        assert status_code.value[0] == 5


# Тест получения клубов по room_code
def test_get_clubs_by_room_code(grpc_channel):
    created_clubs_count = 2
    # Создание шаблона с базовым room_code
    base_room_code = generate_random_name(15)
    # Объявление списка для хранения room_code
    room_codes = []

    # Добавление в массив сгенерированных room_code с общей базовой частью + уникальная часть
    for i in range(created_clubs_count):
        # Добавление к шаблону room_code уникальной части
        room_codes.append(base_room_code+generate_random_name(5))

    # Создание клубов с room_code содержащими шаблон
    for i in range(len(room_codes)):
        room_name = generate_random_name(12)
        created_club = add_club(room_codes[i], room_name)

    # Получение созданных клубов по базовой части room_code
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.GetClubRequest(
        room_code=base_room_code)

    response = stub.GetClub(request)

    assert response.guid == created_club.guid
    assert response.room_name == created_club.room_name
    assert response.room_code == created_club.room_code


# Тест получения всех клубов
def test_get_all_clubs(grpc_channel):
    stub = club_service_pb2_grpc.ClubServiceGrpcStub(grpc_channel)

    request = club_service_pb2.GetAllClubsRequest()
    response = stub.GetAllClubs(request)
