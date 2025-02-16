# coding: utf-8
# license: GPLv3
import math

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects, max_distance):
    """
    Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        angle = math.atan2(body.y - obj.y, body.x - obj.x)
        if r >= max_distance / 1000:  # если два тела очень близко и появляется проблема бесконечной силы при
            # конечном времени, поэтому нулевые силы, пока не улетит хоть на сколько-то
            body.Fx -= gravitational_constant * obj.m * body.m / r ** 2 * math.cos(angle)
            body.Fy -= gravitational_constant * obj.m * body.m / r ** 2 * math.sin(angle)


def move_space_object(body, dt):
    """
    Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.x += ax * dt ** 2 / 2 + body.Vx * dt
    body.Vx += ax * dt
    body.y += ay * dt ** 2 / 2 + body.Vy * dt
    body.Vy += ay * dt


def recalculate_space_objects_positions(space_objects, dt, max_distance):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects, max_distance)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
