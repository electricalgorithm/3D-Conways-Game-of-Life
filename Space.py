from VoxelCell import VoxelCell
import numpy as np
from random import randint
from copy import deepcopy


class Space:
    LENGTH_EXPAND_RATE: int = 3

    def __init__(self, row_count, col_count, page_count, chance_1_divided_by=3, restricted_page=None):

        # Checking for if the parameters are 0 and change is 1.
        if any([i <= 0 for i in [row_count, col_count, page_count]]) \
                or chance_1_divided_by <= 0 or chance_1_divided_by == 1:
            raise Exception("You can't construct a Space object dimensionless or have a living chance %100.")

        # Assigning the properties
        self._entered_dims = (row_count, col_count, page_count)
        self._chance: int = chance_1_divided_by
        self._max_page: int = restricted_page if not restricted_page else 0
        self._rows: int = row_count + self.LENGTH_EXPAND_RATE * 2
        self._cols: int = col_count + self.LENGTH_EXPAND_RATE * 2
        self._pages: int = \
            page_count + self.LENGTH_EXPAND_RATE * 2 if self._check_page_restriction(page_count) else restricted_page
        self._rules_born: list = [3]
        self._rules_stayalive: list = [2, 3]

        # Creating the multidimensional array
        self._grid = self.create_grid(self._pages, self._rows, self._cols)

    def assign_grid(self, grid: list) -> bool:
        """
        NOT READY YET: DON'T USE IT. A function to assign given grid to the Space.

        :param grid: A grid which has Space's dimensions.
        :returns: True if it worked.
        """
        if self.get_dimensions(grid) == self._entered_dims:
            try:
                self._grid = grid
            except Exception as err:
                print(f"[ERROR] {err}")
                return False
            return True
        else:
            return False

    def expand(self) -> list:
        """
        A function to expand Space object's grid lengths. The expanding is adding LENGTH_EXPAND_RATE
        to the all sides of the current grid.

        :returns: Expanded grid, 3-dimensional nested list.
        """
        # TODO: Restriction doesn't work. Fix it.
        # Getting expended dimensions for self._grid.
        new_z, new_x, new_y = self._get_expended_dim(self._pages, self._rows, self._cols)
        # Creating a new (with expended lengths) grid.
        expended_grid = self.create_grid(new_z, new_x, new_y)
        # Combining the new grid with the old one, so that livings are protected.
        self.combine_two_grid(expended_grid, self._grid, (self._pages, self._rows, self._cols), self.LENGTH_EXPAND_RATE)
        # Setting new expended dimensions to the instance.
        self._set_expended_dim()

        return expended_grid

    def export(self, seperate_dims: bool = False) -> np.ndarray or tuple:
        """
        This function exports the current grid of the Space to ndarray (numpy) or tuple. ndarray is a 3D array
        which it's dimensions are [pages, rows, columns]. Tuple, on the other hand, contains four ndarrays for,
        respectivly, x, y, z and values (0 or 1).

        :param seperate_dims: Optional. It must be set to True if the main purpose of exporting is 3D modelling.
        :returns: np.ndarray (seperate_dims=False) or Tuple (seperate_dims=True).
        """
        # Pre-allocation for better performance results.
        np_array = np.zeros([self._pages, self._rows, self._cols])

        # Creating the ndarray from the nested list.
        for page_i in range(self._pages):
            for row_i in range(self._rows):
                for col_i in range(self._cols):
                    np_array[page_i, row_i, col_i] = self._grid[page_i][row_i][col_i].get_numeric_alive()
        # Returning the ndarray directly.
        if not seperate_dims:
            return np_array

        # Converting the existing 3D ndarray to 2D ndarray which has
        # a format like explained bellow.
        else:
            # Getting size of ndarray.
            size = np_array.shape[0] * np_array.shape[1] * np_array.shape[2]
            # Pre-allocation for new ndarray.
            new_matrix = np.zeros((4, size))

            # TODO: Convert the nested list directly to the 2D numpy.ndarray with using VoxelCell objects'
            #  get_coordinates() method without converting the numpy.ndarray firstly.
            # Here, we're assigning of the every objects indices to new array.
            insterted_index = 0
            for index, is_alive in np.ndenumerate(np_array):
                # Output ndarray
                # 1, 0, 0... (Is alive?)
                # 2, 3, 7... (X coordinates - 3th dim)
                # 1, 1, 4... (Y coordinates - 2th dim)
                # 1, 1, 2... (Z coordinates - 1th dim)
                new_matrix[:, insterted_index] = np.transpose(np.array([is_alive, index[2], index[1], index[0]]))
                insterted_index += 1
            return new_matrix[1, :], new_matrix[2, :], new_matrix[3, :], new_matrix[0, :]

    def randomize(self) -> None:
        """
        This function is for randomly create living cells in the Space after creation. Don't use it after calling
        update().
        """
        for __page in range(self._pages):
            for __row in range(self._rows):
                for __col in range(self._cols):
                    # Centering the Scene inside the big matrix.
                    # We need that big matrix because it is needed
                    # for simulating unlimited space.
                    if self.LENGTH_EXPAND_RATE < __page <= self._entered_dims[2] + self.LENGTH_EXPAND_RATE \
                            and self.LENGTH_EXPAND_RATE < __row <= self._entered_dims[0] + self.LENGTH_EXPAND_RATE \
                            and self.LENGTH_EXPAND_RATE < __col <= self._entered_dims[1] + self.LENGTH_EXPAND_RATE:

                        # Since randint(0, x) returns a integer in [0, 1, 2, ..., x-1]
                        # it works as a chance rate
                        if not randint(0, self._chance):
                            self._grid[__page - 1][__row - 1][__col - 1].set_alive()

    def set_cell(self, indices: tuple, status):
        """
        This function makes a cell "dead" or "alive". The parameter indices
        must be in this order: (page, row, col).

        :param indices: A tuple which indices (page, row, column)
        :param status: "alive" or "dead"
        :returns: True if there's no error.
        """
        cell = self._grid[indices[0]][indices[1]][indices[2]]
        if status.lower() == "alive":
            cell.set_alive()
            return True
        elif status.lower() == "dead":
            cell.set_dead()
            return True
        else:
            return False

    def set_rules(self, rules: str):
        """
        A function to change/set the ruleset for Game of Life. If it hasn't changed, the rules are defaults
        (the ones which described by Conwey).

        :param rules: A string like "Bxx/Sxx" where x's are integers. B means "born" and S means stay alive.
        :returns:
        """
        # Additional function to use it on set_rules method
        # Taken directly from GeeksForGeeks
        def _split2list(word: str) -> list:
            return [char for char in word]

        # A function to convert string array to
        # integer array.
        def _make_int(str_arr: list) -> list:
            return [int(index) for index in str_arr]

        # Since the rules given in "B23/S34" semantic,
        # firstly we have to split it with "/" char.
        rule_set = rules.split("/")
        for set_mem in rule_set:
            # Checking born rules and assigning it.
            if "B" in set_mem:
                self._rules_born = _make_int(_split2list(set_mem.replace("B", "")))
            # Checking stay alive rules and assigning it.
            if "S" in set_mem:
                self._rules_stayalive = _make_int(_split2list(set_mem.replace("S", "")))

    def update(self) -> None:
        """
        A function to update the generations. It means that if you use this method, the Game of Life
        will update its generation to the next one.
        """
        # We're firstly deepcopy the grid, so that changing it and finding neighbours
        # can be done in separate nested lists. This process slows down the algorithm.
        _copy_grid = deepcopy(self._grid)

        for page_i in range(self._pages):
            for row_i in range(self._rows):
                for col_i in range(self._cols):
                    # Finding the neighbours for VoxelCell in position of (row_i, col_i, page_i).
                    neighbours = self._find_neighbours(row_i, col_i, page_i, grid=_copy_grid)

                    # Counting the living cells.
                    alive_count = 0
                    for cell_i in neighbours:
                        if cell_i.is_alive():
                            alive_count += 1

                    # Getting a reference for that particular VoxelCell object.
                    _VoxelCell = self._grid[page_i][row_i][col_i]
                    # Applying the rules.
                    self._apply_rules(_VoxelCell, alive_count)

        # Expanding the grid size for next generation.
        self._grid = self.expand()

    @staticmethod
    def clear_ndarray(tdarray: np.ndarray, override=False) -> np.ndarray:
        """
        A function to clear the non used dimensions (a page, a row or a column) in a numpy.ndarray.
        It can be used for further algorithm improvments.

        :param tdarray: The ndarray which will be cleared.
        :param override: If you want to return another ndarray, choose False but it'll be slower. Choosing
        True means that replacing the parameter array with output.
        :returns: Returns a numpy.ndarray if override=False.
        """
        # If the caller don't want to create a new array, we can assign
        # same memory space as follows. Or create a new copied one.
        if not override:
            returned_arr = tdarray.copy()
        else:
            returned_arr = tdarray

        # Getting the shape of original array
        shape = returned_arr.shape

        # Clearing the pages
        removed = 0
        for page_index in range(shape[0]):
            if np.all(returned_arr[page_index - removed, :, :] == 0):
                returned_arr = np.delete(returned_arr, page_index - removed, 0)
                removed += 1

        # Clearing the rows
        removed = 0
        for row_index in range(shape[1]):
            if np.all(returned_arr[:, row_index - removed, :] == 0):
                returned_arr = np.delete(returned_arr, row_index - removed, 1)
                removed += 1

        # Clearing the columns
        removed = 0
        for col_index in range(shape[2]):
            if np.all(returned_arr[:, :, col_index - removed] == 0):
                returned_arr = np.delete(returned_arr, col_index - removed, 2)
                removed += 1

        return returned_arr

    @staticmethod
    def combine_two_grid(expanded_grid: list, small_grid: list, small_g_size: tuple, expand_rate: int) -> None:
        """
        A function to add two 3D grids together. First argument's lengths must be bigger than the
        seconds argument's lengths.

        :param expanded_grid: The bigger grid
        :param small_grid: The small grid.
        :param small_g_size: The small grid's sizes.
        :param expand_rate: The expanding rate of grids. (Dimension difference of big and small grids.)
        """
        # TODO: Use get_dimensions().
        for z in range(small_g_size[0]):
            for x in range(small_g_size[1]):
                for y in range(small_g_size[2]):
                    if small_grid[z][x][y].is_alive():
                        expanded_grid[z + expand_rate][x + expand_rate][y + expand_rate].set_alive()

    @staticmethod
    def create_grid(pages, rows, cols) -> list:
        """
        A function to create a grid which is a 3D nested list. Automaticly called when instance constructed.

        :param pages: Page count. Think it as z-axis length.
        :param rows: Row count. Think it as y-axis length.
        :param cols: Column count. Think it as x-axis length.
        :returns: Nested 3d list
        """
        grid = [[[
            VoxelCell(_k, _j, _i) for _j in range(cols)
        ] for _k in range(rows)
        ] for _i in range(pages)
        ]
        return grid

    @staticmethod
    def get_dimensions(nested_list: list) -> tuple or bool:
        try:
            _no_need = nested_list[0][0][0][0]
        except TypeError:
            try:
                nested_list[0][0][0]
            except IndexError:
                raise Exception("The nested_list must be exactly 3D list.")

            page_length = len(nested_list)
            row_length = len(nested_list[0])
            col_length = len(nested_list[0][0])
            return row_length, col_length, page_length

    def _apply_rules(self, voxel_cell_object: VoxelCell, neighbour_alive_count: int) -> None:
        # This the method for checking and applying the rules. Changing here will changing
        # the logic of the game.
        if voxel_cell_object.is_alive():
            if neighbour_alive_count in self._rules_stayalive:
                pass
            else:
                voxel_cell_object.set_dead()
        else:
            if neighbour_alive_count in self._rules_born:
                voxel_cell_object.set_alive()

    def _check_page_restriction(self, entered_page_size) -> bool:
        if self._max_page:
            if entered_page_size > self._max_page:
                print(
                    f'You can\'t construct a Space object with {entered_page_size} pages if \
                    restricted to {self._max_page}.')
                return False
        return True

    def _find_neighbours(self, param_x_rows, param_y_cols, param_z_pages, grid=None) -> list:
        neighbour_list = []
        if not grid:
            grid = self._grid

        # Xs are rows, Ys are columns, Zs are pages.
        for page_search in [-1, 0, 1]:
            for col_search in [-1, 0, 1]:
                for row_search in [-1, 0, 1]:
                    nto_check_x = param_x_rows + row_search
                    nto_check_y = param_y_cols + col_search
                    nto_check_z = param_z_pages + page_search

                    if 0 <= nto_check_x < self._rows:
                        if 0 <= nto_check_y < self._cols:
                            if 0 <= nto_check_z < self._pages:
                                if not (nto_check_x == param_x_rows
                                        and nto_check_y == param_y_cols
                                        and nto_check_z == param_z_pages):
                                    neighbour_list.append(grid[nto_check_z][nto_check_x][nto_check_y])

        return neighbour_list

    def _get_expended_dim(self, normal_z: int, normal_x: int, normal_y: int) -> tuple:
        # We're multiplying it with 2 because it must expand
        # in every direction in every dimension.
        x: int = normal_x + self.LENGTH_EXPAND_RATE * 2
        y: int = normal_y + self.LENGTH_EXPAND_RATE * 2
        z: int = normal_z + self.LENGTH_EXPAND_RATE * 2
        return z, x, y

    def _set_expended_dim(self):
        self._rows = self._rows + self.LENGTH_EXPAND_RATE * 2
        self._cols = self._cols + self.LENGTH_EXPAND_RATE * 2
        self._pages = self._pages + self.LENGTH_EXPAND_RATE * 2
