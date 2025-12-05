import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_shape(ax, vertices, faces, color):
    vertices = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices[faces], facecolors=color
        , edgecolors='k', linewidths=0.2))


def main(vertices_cube, faces_cube):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d', proj_type='ortho')

    draw_shape(ax, vertices_cube, faces_cube, 'blue')

    ax.set_box_aspect([1,1,1])
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-3, 3)
    ax.view_init(azim=-37.5, elev=30)
    ax.set_xticks(np.linspace(-3, 3, 5))
    ax.set_yticks(np.linspace(-3, 3, 5))
    ax.set_zticks(np.linspace(-3, 3, 5))

    plt.show()
    

if __name__ == '__main__':
    vertices_cube = np.array([
    [0,  2, -2,  0],
    [0,  0,  0,  2],
    [3,  0,  0,  0],
    [1,  1,  1,  1]
    ])

    faces_cube = np.array([
        [0, 1, 3],
        [0, 1, 2],
        [0, 2, 3],
        [1, 2, 3]
    ])
    
    main(vertices_cube, faces_cube)
