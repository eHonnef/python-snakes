import tkinter as tk
from Objects import MovableObject
"""
Classes concerning the snake body and movement
"""


class Body:

  def __init__(self, canvas):
    self._canvas = canvas
    self._body = []
    self._current_direction = "right"

    # create initial given the x and y position
    self._create_initial(20, 20)

  def add(self, n):
    # add or remove body parts from the snake
    if n < 0 and len(self._body) > 1:
      if len(self._body) <= abs(n):
        n = len(self._body) - 1

      for _ in range(abs(n)):
        i = self._body.pop()
        self._canvas.delete(i._id)

      return

    for _ in range(n):
      x = self._body[-1]._x
      y = self._body[-1]._y

      if self._body[-1]._direction == self._get_dir("left"):
        x += 10
      elif self._body[-1]._direction == self._get_dir("right"):
        x -= 10
      elif self._body[-1]._direction == self._get_dir("up"):
        y += 10
      elif self._body[-1]._direction == self._get_dir("down"):
        y -= 10

      self._body.append(
          MovableObject(
              self._create_circle(x, y, 5, fill="#BBB", outline=""), x, y,
              self._body[-1]._direction))

  def change_direction(self, direction):
    if direction == self._current_direction:
      return
    if direction == "left" and self._current_direction == "right":
      return
    elif direction == "right" and self._current_direction == "left":
      return
    elif direction == "up" and self._current_direction == "down":
      return
    elif direction == "down" and self._current_direction == "up":
      return

    self._current_direction = direction
    self._body[0]._direction = self._get_dir(direction)

  def _create_initial(self, x, y):
    # x + 40 because the initial size is 5 (inc. head) and each circle have 10 of diameter (5 of radius duh)
    self._body.append(
        MovableObject(
            self._create_circle(x + 40, y, 5, fill="#000", outline=""), x + 40,
            y, self._get_dir(self._current_direction)))

    # x + (10 * r) ---> x = initial position | 10*r = offset from previous body part
    for r in range(3, -1, -1):
      self._body.append(
          MovableObject(
              self._create_circle(x + (10 * r), y, 5, fill="#BBB", outline=""),
              x + (10 * r), y, self._get_dir(self._current_direction)))

  def _create_circle(self, x, y, r, **kwargs):
    return self._canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

  def _get_dir(self, direction):
    if direction == "up":
      return (0, -10)
    if direction == "right":
      return (10, 0)
    if direction == "down":
      return (0, 10)
    if direction == "left":
      return (-10, 0)

  def iterate(self, limits=None):
    # move the snake around
    for i in range(len(self._body) - 1, -1, -1):
      if limits == None:
        self._canvas.move(self._body[i]._id, *self._body[i]._direction)
        self._body[i]._x += self._body[i]._direction[0]
        self._body[i]._y += self._body[i]._direction[1]
      else:
        pass
        # no walls rule (fak this)
        # self._body[i]._x = (self._body[i]._x +
        #                     self._body[i]._direction[0]) % limits[2]

        # if self._body[i]._x < limits[0]:
        #   self._body[i]._x = limits[0]
        # elif self._body[i]._x > limits[2]:
        #   self._body[i]._x = limits[2]

        # self._body[i]._y = (self._body[i]._y +
        #                     self._body[i]._direction[1]) % limits[3]

        # if self._body[i]._y < limits[1]:
        #   self._body[i]._y = limits[1]
        # elif self._body[i]._y > limits[3]:
        #   self._body[i]._y = limits[3]

      if i > 0:
        self._body[i]._direction = self._body[i - 1]._direction
