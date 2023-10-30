from base import *
from file_management import *
from frontend import *

TEST_FILE = False
TEST_BASE = False
TEST_GUI = True
ISOLATED_TESTS = False

def isolated_test():
    data = {"Hi": 1,
            "Hello": 2,
            "Hola": 3,
            "Bonjour": 4}
    
    data_in_string = json.dumps(data, indent=4)

    new = load_game(r"C:\Users\tandu\Documents\Python\Projects\StoryOfU\data\games\Test_1.json")

    print(new.data)

def run():
    if TEST_FILE:

        test_file_system()
        
    if TEST_BASE:

        test_base()
 
    if TEST_GUI == True:

        test_GUI() 

    if ISOLATED_TESTS == True:
        isolated_test()


if __name__ == "__main__":
    run()
