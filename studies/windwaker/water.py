# Simple template to bootstrap experiments

# TODO: need to set up shaders

import glfw
import numpy as np
from OpenGL.GL import *

WIDTH = 1280
HEIGHT = 720

GRID_LATTICE_SIZE = 20

g_lattice_verts = None
g_lattice_inds = None

g_lattice_vao = None
g_lattice_vbo = None
g_lattice_ebo = None

def init_vertices():
    global g_lattice_verts
    global g_lattice_inds
    global g_lattice_vao
    global g_lattice_vbo
    global g_lattice_ebo

    half_size = GRID_LATTICE_SIZE / 2
    x = np.linspace(-half_size, half_size, GRID_LATTICE_SIZE)
    y = np.linspace(-half_size, half_size, GRID_LATTICE_SIZE)
    g_lattice_verts = np.array([(xi, yi, 0) for xi in x for yi in y], dtype=np.float32)

    x_len = len(x)
    y_len = len(y)
    assert(x_len > 1)
    assert(y_len > 1)

    x_len_m1 = x_len - 1
    y_len_m1 = y_len - 1
    g_lattice_inds = np.zeros(x_len_m1 * y_len_m1 * 6, dtype=np.uint32)

    lattice_index = 0
    for xi in range(x_len_m1):
        for yi in range(y_len_m1):
            vi = xi + yi * x_len

            # Each iteration here "pushes" the indices for a quad via
            # two triangles (CCW winding order):

            # 0
            # | \
            # |  \
            # |   \
            # |    \
            # 1-----2
            #
            # vi -> 0
            # vi + x_len -> 1
            # vi + x_len + 1 -> 2

            g_lattice_inds[lattice_index + 0] = vi
            g_lattice_inds[lattice_index + 1] = vi + x_len
            g_lattice_inds[lattice_index + 2] = vi + x_len + 1
            lattice_index += 3

            # 0-----2
            #  \    |
            #   \   |
            #    \  |
            #     \ |
            #      \|
            #       1
            #
            # vi -> 0
            # vi + x_len + 1 -> 1
            # vi + 1 -> 2

            g_lattice_inds[lattice_index + 0] = vi
            g_lattice_inds[lattice_index + 1] = vi + x_len + 1
            g_lattice_inds[lattice_index + 2] = vi + 1
            lattice_index += 3

    lattice_vao = glGenVertexArrays(1)
    lattice_vbo = glGenBuffers(1)
    lattice_ebo = glGenBuffers(1)

    glBindVertexArray(lattice_vao)

    glBindBuffer(GL_ARRAY_BUFFER, lattice_vbo)
    glBufferData(GL_ARRAY_BUFFER, g_lattice_verts.nbytes, g_lattice_verts, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, lattice_ebo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, g_lattice_inds.nbytes, g_lattice_inds, GL_STATIC_DRAW)

    # index, size, type, normalized, stride, pointer
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindVertexArray(0)


def init_window():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(WIDTH, HEIGHT, "OpenGL Experiment", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create window")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glEnable(GL_DEPTH_TEST)

    return window

def update(dt):
    pass

def render_lattice():
    # TODO: glUseProgram(...)
    glBindVertexArray(g_lattice_vao)

    glDrawElements(GL_TRIANGLES, len(g_lattice_inds), GL_UNSIGNED_INT, None)

    glBindVertexArray(0)
    # TODO: glUseProgram(0)

def render(window):
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glfw.swap_buffers(window)

def main():
    window = init_window()
    prev_time = glfw.get_time()

    init_vertices()

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        dt = current_time - prev_time
        prev_time = current_time

        glfw.poll_events()

        update(dt)
        render(window)

    glfw.terminate()

if __name__ == "__main__":
    main()