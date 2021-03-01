from Space import Space


def workspace_divider(needed: int):
    from math import sqrt
    while int(sqrt(needed)) != sqrt(needed):
        needed += 1
    return int(sqrt(needed))


def create_matplotlib_graphs(space_object: Space, generations: int, save: tuple = (False, None), show: bool = True,
                             onebyone: bool = False):
    """
    This function will create matplotlib figures for both saving and displaying at every generation.

    :param space_object: The Space object
    :param generations: An integer of generation number
    :param save: A tuple which is (will_save, file_name_prefix). Default is (False, None)
    :param show: True if want to show, False if don't want.
    :param onebyone: True if show one by one and False for showing together.
    :return:
    """
    # Making imports here because of unnecessary usage
    # of matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Creating the first values without .update()
    values = Space.clear_ndarray(space_object.export())

    if not onebyone:
        fig = plt.figure()
        workspace_dims = workspace_divider(generations)
        for gen in range(generations):
            fig.add_subplot(110 * workspace_dims + gen + 1, projection="3d")
            ax = fig.gca()
            ax.set_aspect('auto')
            ax.voxels(values, edgecolor="k")
            if save[0]:
                plt.savefig(f"{save[1]}_gen_{gen}")

            space_object.update()
            values = Space.clear_ndarray(space_object.export())

        if show:
            plt.show()
    else:
        for gen in range(generations):
            fig = plt.figure(gen)
            ax = fig.gca(projection='3d')
            ax.set_aspect('auto')
            ax.voxels(values, edgecolor="k")
            if save[0]:
                plt.savefig(f"{save[1]}_gen_{gen}")
            if show:
                print("You must close the figure in order to see next generation.")
                plt.show()

            space_object.update()
            values = Space.clear_ndarray(space_object.export())


def create_mayavi_animation(space_object: Space, generations: int, wait: int, ui: bool = False):
    """
    This function will create a 3D animation using mayavi.mlab module. You can't directly change
    camera positions while calculating the generations but after, you can. It should be fixed in
    new versions.

    :param space_object: The Space object which will simulated.
    :param generations: Generation count.
    :param wait: The delay rate for animation.
    :param ui: User inteface option for stop/start animation. (Mayavi)
    """
    from mayavi import mlab

    x, y, z, val = space_object.export(seperate_dims=True)
    figure = mlab.figure(size=(800, 600))
    plt = mlab.points3d(x, y, z, val, mode="cube", color=(1, 0, 0), figure=figure)
    print("Generation 0: Inital state")

    # TODO: Fix the non-changeable camera during the calculation of generations.
    @mlab.animate(delay=wait, ui=ui)
    def __animate(gen):
        fig = mlab.gcf()
        dist = mlab.view()[2]
        for index in range(gen):
            space_object.update()
            _x, _y, _z, _val = space_object.export(seperate_dims=True)
            plt.mlab_source.reset(x=_x, y=_y, z=_z, scalars=_val, reset_zoom=True)
            print(f"Generation: {index + 1}")
            mlab.view(distance=dist+index, focalpoint="auto", figure=fig)
            index += 1
            if index == gen:
                print("Simulation has completed.")
            yield
        return True

    while True:
        is_ended = __animate(generations)
        if is_ended:
            break

    mlab.show()
