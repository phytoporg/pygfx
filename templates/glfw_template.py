# Simple template to bootstrap experiments

import glfw
import numpy as np
from OpenGL.GL import *

WIDTH = 1280
HEIGHT = 720

def init():
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

def render(window):
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glfw.swap_buffers(window)

def main():
    window = init()
    prev_time = glfw.get_time()

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