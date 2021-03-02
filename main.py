from Space import Space
from VoxelCell import VoxelCell
from utils import create_matplotlib_graphs, create_mayavi_animation
import sys


def show_help():
    # TODO: Create a help text.
    pass


if __name__ == "__main__":
    # TODO: Create a GUI.
    COL: int = 0
    ROW: int = 0
    PAGE: int = 0
    GEN: int = 0
    WAIT: int = 100
    CHANCE: int = 3
    RENDERER: str = ""
    SAVE: bool = True
    SAVE_PRE: str = "GoL"
    RULESET: str = "B3/S23"
    onebyone: bool = False

    if sys.argv[1] in ["--help", "-h"]:
        show_help()
        exit()

    for arg in sys.argv:
        if arg == "main.py":
            continue
        try:
            arguments = arg.split("=")
            arguments[0] = arguments[0].lower()
            arguments[1] = arguments[1].lower()

            if arguments[0] == "--row":
                ROW = int(arguments[1])
            elif arguments[0] == "--col":
                COL = int(arguments[1])
            elif arguments[0] == "--page":
                PAGE = int(arguments[1])
            elif arguments[0] == "--gen":
                GEN = int(arguments[1])
            elif arguments[0] == "--waitms":
                WAIT = int(arguments[1])
            elif arguments[0] == "--chance":
                CHANCE = int(arguments[1])
            elif arguments[0] == "--renderer":
                RENDERER = arguments[1]
            elif arguments[0] == "--save":
                SAVE = bool(arguments[1])
            elif arguments[0] == "--save-prefix":
                SAVE_PRE = arguments[1]
            elif arguments[0] == "--rules":
            	 RULESET = arguments[1]
        except ValueError or IndexError as error:
            print("Something wrong. Check the provided flags.")
            exit(0)

    # Checking of dimensions and generations.
    if any([i <= 0 for i in [ROW, COL, PAGE, GEN]]):
        print("Size parameters or generation can't be zero or less.")
        exit(0)

    print("Note that, restriction of dimensions doesn't work yet.")
    # Creating the Space object and randomize it.
    Life = Space(PAGE, ROW, COL, chance_1_divided_by=CHANCE)
    Life.set_rules(RULESET)
    Life.randomize()

    # What to do with program
    if RENDERER:
        # Creating 3D Animation
        if RENDERER == "mayavi":
            print("Entering the 3D animation mode with mayavi.")
            create_mayavi_animation(Life, GEN, WAIT)
        # Creating 3D plots with matplotlib
        elif RENDERER.split(":")[0] == "matplotlib":
            print("Entering the 3D plotting mode with matplotlib.")
            try:
                if RENDERER.split(":")[1] == "1by1":
                    onebyone = True
                else:
                    print("Wrong matplotlib method specifier.")
                    exit()
            except IndexError:
                onebyone = False

            create_matplotlib_graphs(Life, GEN, (SAVE, SAVE_PRE), True, onebyone=onebyone)

    # Doing nothing fancy
    else:
        print("You choose doing nothing but program will still calculated the generations.")
        for gen in range(GEN):
            Life.update()
