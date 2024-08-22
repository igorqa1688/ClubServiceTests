import grpc
import pytest
from functions import generate_guid
from global_vars import server
import club_service_pb2
import club_service_pb2_grpc


@pytest.fixture(scope="module")
def grpc_channel():
    #Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        yield channel