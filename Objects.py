import random
"""
Classes concerning the game objects.
Apples, walls, static and movable objects
"""


class StaticObject:

  def __init__(self, tag, x, y):
    self._id = tag
    self._x = x
    self._y = y


class MovableObject(StaticObject):

  def __init__(self, tag, x, y, direction):
    super().__init__(tag, x, y)
    self._direction = direction


class Apple(StaticObject):

  def __init__(self, tag, x, y):
    super().__init__(tag, x, y)
    self._value = random.randint(0, 10)

    if self._value < 3:
      self._color = (255, 0, 0)
    elif self._value >= 3 and self._value < 6:
      self._color = (0, 255, 0)
    elif self._value >= 6 and self._value <= 9:
      self._color = (0, 0, 255)
    elif self._value == 10:
      self._color = (242, 255, 0)


class Wall:

  def __init__(self, tag, x_i, y_i, x_f, y_f):
    self._id = tag
    self._x_i = x_i
    self._y_i = y_i
    self._x_f = x_f
    self._y_f = y_f
