1. Установить зависимости из файла requirements.txt;
2. Перетащить в папку с проектом *.proto файл;
3. Выполнить команду в папке с *.proto файлом: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto_file_name.proto;
3.1.Для пагинации: protoc --python_out=. --proto_path=. Protos/*.proto
4. В файле global_vars.py задать актуальный адрес сервера и порт.
5. Используемая версия python: 3.12
6. 
Файл с тестами: test_club_service.py остальные файлы примеры или зависимости.
