from base import *
import json
import os
import io

PARENT = os.getcwd()

DATA_DIRECTORY = os.path.join(PARENT, "data")
GAME_DIRECTORY = os.path.join(DATA_DIRECTORY, "games")
GLOBAL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "global.json")

global_data_dict = {"games" : []}

data_dict = {"name" : None,
            "attributes": None,
            "actions": None,
            "entities": None}

def initialize():
    if not os.path.exists(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)

    if not os.path.exists(GAME_DIRECTORY):
        os.mkdir(GAME_DIRECTORY)

    if not os.path.exists(GLOBAL_DATA_DIRECTORY):
        global_data = io.open(GLOBAL_DATA_DIRECTORY, "x")
        json.dump(global_data_dict, global_data, indent = 4)
        global_data.close()

def update_global_data():

    global_data_file = io.open(GLOBAL_DATA_DIRECTORY, "r")

    global_data = json.load(global_data_file)

    global_data_file.close

    game_files = os.listdir(GAME_DIRECTORY)

    temporary_game_data_holder = {"games": []}

    for ele in game_files:
        with io.open(os.path.join(GAME_DIRECTORY, ele)) as game_file:
            game_data = json.load(game_file)
            file_data = {"name": game_data["name"], "path": os.path.join(GAME_DIRECTORY, ele)}
            
            temporary_game_data_holder["games"].append(file_data)

    global_data_file = io.open(GLOBAL_DATA_DIRECTORY, "w")
    
    json.dump(temporary_game_data_holder, global_data_file, indent=4)

    global_data_file.close()

def load_global_data() -> dict:
    with io.open(GLOBAL_DATA_DIRECTORY, "r") as g:
        return json.load(g)

def save_game(game: TRPG):

    file_name = game.get_name() + ".json"
    game_file_path = os.path.join(GAME_DIRECTORY, file_name)

    
    if not os.path.exists(game_file_path):
        file = io.open(game_file_path, mode="tx")
        
    else:
        file = io.open(game_file_path, mode="tw")

    json.dump(game.data, file, indent=4)

    with io.open(GLOBAL_DATA_DIRECTORY, "rt") as glo:
        data: dict = json.load(glo)
        data["games"].append({"name": game.get_name(),
                              "path": game_file_path})

def load_game(file_path: str) -> TRPG:

    if not os.path.exists(file_path):
        raise FileNotFoundError("File {} was not found.\n".format(file_path))
    
    file = io.open(file_path)

    data = file.read()

    new = TRPG("temp")

    new.data = json.loads(data)

    new.load_data()
    return new
    
def test_file_system():
    
    new = TRPG("File_System_Test")

    new.new_attribute("HP", "num")
    new.new_attribute("Condition", "alpha")

    new.new_action("doom", effects=[EffectStruct("HP", "st", ConditionStruct("HP", "target", ">", 0), "+", -7)])

    new.new_entity("Lel", [AttrValueStruct("HP", "num", 30), AttrValueStruct("Condition", "alpha", "Bad")], ["doom"])

    save_game(new)

    game = load_game(os.path.join(GAME_DIRECTORY, "File_System_Test.json"))

    print(game.data)
