class VoxelCell:
    def __init__(self, x_row, y_col, z_page):
        self._alive = False
        self._X = x_row
        self._Y = y_col
        self._Z = z_page

    def set_alive(self):
        self._alive = True

    def set_dead(self):
        self._alive = False

    def is_alive(self):
        return self._alive

    def get_numeric_alive(self):
        if self._alive:
            return 1
        return 0

    def get_coordinates(self):
        return [self._X, self._Y, self._Z]

    def __add__(self, other):
        if isinstance(other, VoxelCell):
            if self._alive or other._alive:
                new_voxelcell = VoxelCell()
                new_voxelcell.set_alive()
                return new_voxelcell
        else:
            raise ValueError("The both sides of '+' statement must be VoxelCell object.")

    def __repr__(self):
        return f"VoxelCell(alive={self._alive})"
