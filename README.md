# Conway's Game of Life 3D

This repository is both provides an API for Game of Life and an command line application interface to use the API. I built the API and the algorithm just for fun and learn new things. I hope you'll like it.

Note that, there may be lots of bugs and lots of performance issues, if you want to contribute it, I would be very happy.

![An example of terminal output](https://github.com/electricalgorithm/3D-Conways-Game-of-Life/blob/main/assets/terminal-output.png?raw=true)

![An example of matploylib output](https://github.com/electricalgorithm/3D-Conways-Game-of-Life/blob/main/assets/matplotlib.gif?raw=true)

![An example of mayavi output](https://github.com/electricalgorithm/3D-Conways-Game-of-Life/blob/main/assets/mayavi.gif?raw=true)

### Installation

| Dependency                                         | Installation                                      |
| -------------------------------------------------- | ------------------------------------------------- |
| Python3                                            | https://www.python.org/downloads/                 |
| numpy                                              | via pip: `pip install numpy`                      |
| matplotlib (for 3D)                                | via pip: `pip install matplotlib`                 |
| mayavi (for 3D) _(Use the bleeding edge version.)_ | https://github.com/enthought/mayavi#bleeding-edge |

I recommend you to use virtual enviroment for application.  You may have noticed that `requirements.txt` file does not have mayavi since I want you to use it's bleeding edge version. If the `pip` version of mayavi works with your system, tell me or update the `README.md` file.

##### Detailed Explaination of Installing

```sh
~$ git clone https://github.com/electricalgorithm/3D-Conways-Game-of-Life.git
~$ cd 3D-Conways-Game-of-Life
~$ virtualenv . # I had used Python 3.7 to develop the project. You can specify it with `--python=path/to/python3.7`
~$ source bin/active # For Windows users, it think it's ".\Scripts\activate".
~$ pip install numpy
~$ pip install matplotlib
# Installing of mayavi bleeding edge
~$ git clone https://github.com/enthought/mayavi.git
~$ cd mayavi
~$ pip install -r requirements.txt
~$ pip install PyQt5
~$ python setup.py install
# Returning back to main.py directory.
# Opening the program.
~$ python main.py --row=3 --col=3 --page=2 --gen=2 --renderer=mayavi
```



### Using as application

The application requires using flags to simulate. They are:

* `--row=`	**Required**. Must be an _integer_. It sets the Game of Life's row/y dimension for randomizing values. _The life's grid won't be restricted to these dimensions._
* `--col=`	**Required**. Must be an _integer_. It sets the Game of Life's col/x dimension for randomizing values. _The life's grid won't be restricted to these dimensions._
* `--page=`	**Required**. Must be an _integer_. It sets the Game of Life's page/z dimension for randomizing values. _The life's grid won't be restricted to these dimensions._
* `--gen=`	**Required**. Must be an _integer_. It is the number of the generations which will be calculated. For higher numbers, the simulation will be very slow. Consider changing  `LENGTH_EXPAND_RATE` constant with a lower value in `Space.py` file.
* `--chance=` Optional. Must be an _integer_. It defines the chance of randomize() function as one over given integer.
* `--rules=` Optional. Default is "B3/S23". It defines the ruleset.
* `--waitms=` Optional. Must be an _integer_. This is the delay in the calculations of the generations. Don't sure if it works correctly, check it out.
* `--renderer=` Optional. Must be `mayavi`, `matplotlib` or `matplotlib:1by1`. This the rendering method of 3D view. If not spesified, nothing will pop-up to show you the generations.
* `--save=` Optional. Default is `True`. Must be `True` or `False`. To do not save matplotlib figures, make it `False`.
* `--save-prefix=` Optional. Default is `GoL`. The prefix for saving matplotlib figures.
##### Example

```sh
~$ python main.py --row=5 --col=5 --page=4 --chance=4 --rules=B36/S23 --gen=2 --renderer=matplotlib:1by1 --save=True --save-prefix=GoL-example
```

> Note: If you use 1by1 method, you have to close the current figure window to see next generation.




### API

| Class                    |                                    |
| ------------------------ | ---------------------------------- |
| VoxelCell (VoxelCell.py) | The cell class for using in Space. |
| Space (Space.py)         | The class for creating the game.   |

| Methods of VoxelCell class   |                                                          |
| ---------------------------- | -------------------------------------------------------- |
| `VoxelClass(row, col, page)` | It creates a VoxelCell object with given positions.      |
| `set_alive()`                | It revitalizes (set the cell alive) the VoxelCell.       |
| `set_dead()`                 | It kills (set the cell dead) the VoxellCell.             |
| `is_alive()`                 | Returns `True` if the VoxelCell is living.               |
| `get_numeric_alive()`        | Same as `is_alive` but returns `int` instead of `bool`.  |
| `get_coordinates()`          | It returns VoxelCell's indices in the instance of Space. |

| Methods of Space class                                       |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `Space(row_count, col_count, page_count, chance_1_divided_by=3, restricted_page=None)` | It creates a Space object which has `row_count * col_count * page_count` VoxelCell instances.  Note that, after the creation, the cell expands. It should be fixed for new versions. `restricted_page` doesn't work for now. |
| `expand()`                                                   | Expands the Space object's grid.                             |
| `export(seperate_dims)`                                      | Returns the Space grid as `numpy.ndarray`. If `seperate_dims` given as True, it returns a `tuple` of `numpy.ndarray`. |
| `randomize()`                                                | It randomly sets the VoxelCells alive.                       |
| `set_cell(indices, status)`                                  | It sets the VoxelCell at `(page, row, col)` indices as `status` which must be "alive" or "dead". |
| `set_rules(rules)`                                           | _Default: "B3/S23"_. It changes the ruleset for Game of Life. |
| `update()`                                                   | It creates new generation. Note: New generation will be assigned to the current `_grid` property. |
| static: `clear_ndarray(tdarray, override=False)`             | Clears all the non-neccecary (which is whole dimension is 0/dead) VoxelCells. It may use for another purposes too. Note: Works only for 3D `numpy.ndarray` objects. |
| static: `combine_two_grid(expanded_grid, small_grid: list, small_g_size, expand_rate)` | It combines two grid (3D nested list) while preserving their living status. |
| static: `create_grid(pages, rows, cols)`                     | Creates a 3D nested list which has VoxelCell objects.        |
| static: `get_dimensions(nested_list)`                        | Returns a 3D nested list (or a grid)'s dimensions.           |

| Functions of Utils.py                                        |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `create_matplotlib_graphs(space_object, generations, save=(False, None), show=True, onebyone=False)` | To show 3D projections of the Space object with using matplotlib. If `onebyone` is `True`, it'll create every generation in a new window. If it is `False`, they will be in a window/figure together. |
| `create_mayavi_animation(space_object, generations, wait, ui=False)` | To show 3D projection of Space object as a animation with using mayavi. Notice that, while the function calculates newer generations you can't change the position of the camera. It should be fixed in new versions. |

##### Example Usage of the API

```python
from Space import Space
from utils import create_matplotlib_graphs

# Creates the Life (or Space instance)
Life = Space(5, 5, 4, chance_1_divided_by=4)
# Randomly sets the VoxelCells in the grid alive.
Life.randomize()
# Set the VoxelCell at (6, 5, 3) alive.
Life.set_cell((6, 5, 3), "alive")
# Calculate the next generation.
Life.update()
# Save the figures of generation and the next one with using matplotlib and show them as seperate windows.
create_matplotlib_graphs(Life, 2, save=(True, "GoL-example"), show=True, onebyone=True)
# All done.

```

