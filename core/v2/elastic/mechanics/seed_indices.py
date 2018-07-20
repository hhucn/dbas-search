from core.v2.elastic.interface.es_interface import ESInterface

if __name__ == "__main__":
    ESInterface(file="request.sql").initialize_new_index()
