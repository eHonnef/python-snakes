import tkinter as tk
from Snake import Body
from Objects import Apple, Wall
import random


class Game:
  """
  Class that manages the game
  """

  def __init__(self, canvas, limits):
    self._canvas = canvas
    self._limits = limits

    # create snake
    self._snake = Body(self._canvas)

    # create walls
    self._walls = []
    self._create_walls()

    self._apples = []
    self._count = 1

    self.points = 0

  def loop(self):
    # loop that move the snake, create apples and check if a wall was hitted
    self._snake.iterate()
    # self._snake.iterate(self._limits)
    self._count -= 1
    if self._count == 0:
      self.generate_apple()

    self._check_hit()

  def _check_hit(self):
    # Check if something was hitted (wall, apple, body)
    head = self._snake._body[0]
    self._apple_rule(head)
    self._wall_rule(head)
    self._eat_itself_rule(head)

  def _from_rgb(self, rgb):
    """
    translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

  def generate_apple(self):
    # Generate an apple inside the game area
    # it doesnt check if it is inside walls or inside the player
    self._count = random.randint(50, 70)
    x = ((random.randint(self._limits[0], self._limits[2]) * 10) %
         self._limits[2])

    if x <= self._limits[0]:
      x += 20
    elif x >= self._limits[2]:
      x -= 20

    y = ((random.randint(self._limits[1], self._limits[3]) * 10) %
         self._limits[3])

    if y <= self._limits[1]:
      y += 20
    elif x >= self._limits[3]:
      y -= 20

    self._apples.append(
        Apple(
            self._canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline=""), x,
            y))

    # change color because i'm stupid (should have done the Objects classes diferent)
    self._canvas.itemconfig(
        self._apples[-1]._id, fill=self._from_rgb(self._apples[-1]._color))

  def _apple_rule(self, head):
    # Define some rules for the apple
    for a in self._apples:
      if a._x == head._x and a._y == head._y:
        self.points += a._value
        self._canvas.delete(a._id)
        self._apples.remove(a)

        if a._value > 8:
          self._snake.add(-3)

        if a._value > 7:
          # instant generate a new apple if the value of eaten apple > 7
          self.generate_apple()

          if a._value < 9:
            self._snake.add(3)
        else:
          self._snake.add(1)

        print("Score: " + str(self.points) + " Snake size: " +
              str(len(self._snake._body)))

  def change_snake_direction(self, direction):
    self._snake.change_direction(direction)

  def _wall_rule(self, head):
    # checking if some wall was hitted
    gb = self._game_bound
    if not (head._x >= (gb._x_i + 10) and head._y >=
            (gb._y_i + 10) and head._x <= (gb._x_f - 10) and head._y <=
            (gb._y_f - 10)):
      self.end()

    for w in self._walls:
      if head._x >= w._x_i and head._y >= w._y_i and head._x <= w._x_f and head._y <= w._y_f:
        self.end()

  def _create_walls(self):
    self._game_bound = Wall(
        self._canvas.create_rectangle(*self._limits), *self._limits)

  def _eat_itself_rule(self, head):
    # check if the player killed himself
    for b in self._snake._body:
      if b == head:
        continue

      if b._x == head._x and b._y == head._y:
        self.end()

  def end(self):
    # Something, something... the end
    print("DEAD")


class Window(tk.Tk):
  """
  Class that manages the window
  """

  def __init__(self, screenName=None, width=100, height=100):
    # create main window
    super().__init__(screenName=screenName)

    # create canvas, where everything is drawn
    self._canvas = tk.Canvas(
        self,
        width=width,
        height=height,
        borderwidth=0,
        highlightthickness=0,
        bg="white")
    # align canvas
    self._canvas.grid()

    self._game = Game(self._canvas, [10, 10, width - 10, height - 10])

    # bind events
    self.bind("<Key>", self._key_press)

    # run game loop every x ms
    self.after(100, self._loop)

    # start tkinter
    self.mainloop()

  def _loop(self):
    self.after(100, func=self._loop)
    self._game.loop()

  def _key_press(self, event):
    if event.keycode == 37:
      # left arrow
      self._game.change_snake_direction("left")
    elif event.keycode == 38:
      # up arrow
      self._game.change_snake_direction("up")
    elif event.keycode == 39:
      # right arrow
      self._game.change_snake_direction("right")
    elif event.keycode == 40:
      # down arrow
      self._game.change_snake_direction("down")


if __name__ == "__main__":
  # Start
  Window("Snakes", 500, 500)
