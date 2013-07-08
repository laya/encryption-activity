#  gcompris - encryption.py
#
# Copyright (C) 2003, 2008 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# encryption activity.
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import gcompris.bonus
import gcompris.sound
import goocanvas
import pango
import random
from key_value import *

from gcompris import gcompris_gettext as _

#
# The name of the class is important. It must start with the prefix
# 'Gcompris_' and the last part 'encryption' here is the name of
# the activity and of the file in which you put this code. The name of
# the activity must be used in your menu.xml file to reference this
# class like this: type="python:encryption"
#
class Gcompris_encryption:
  """Empty gcompris Python class"""


  def __init__(self, gcomprisBoard):
    print "encryption init"

    # Save the gcomprisBoard, it defines everything we need
    # to know from the core
    self.gcomprisBoard = gcomprisBoard
    self.gcomprisBoard.level = 1
    self.gcomprisBoard.maxlevel = 3
    self.gcomprisBoard.sublevel = 1
    self.gcomprisBoard.number_of_sublevel = 3

    # Parameters for different sublevels
    self.NUMBERS = 1
    self.SYMBOLS = 2
    self.ALPHABETS = 3
    self.VALUE = None
  

  def start(self):
    print "encryption start"
    self.points = 0

    # Create our rootitem. We put each canvas item in it so at the end we
    # only have to kill it. The canvas deletes all the items it contains
    # automaticaly.
    self.rootitem = goocanvas.Group(parent =
                                    self.gcomprisBoard.canvas.get_root_item())

    self.next_level()


  def end(self):
    print "encryption end"
    # Remove the root item removes all the others inside it
    self.rootitem.remove()


  def ok(self):
    print("encryption ok.")


  def repeat(self):
    print("encryption repeat.")
    self.next_level()


  #mandatory but unused yet
  def config_stop(self):
    pass


  # Configuration function.
  def config_start(self, profile):
    pass

  def key_press(self, keyval, commit_str, preedit_str):
    pass

  # Called by gcompris core
  def pause(self, pause):
    # print("encryption pause. %i" % pause)
    
    if (pause == 0):
      self.next_level()

    return 


  # Called by gcompris when the user clicks on level icons
  def set_level(self, level):
    self.gcomprisBoard.level = level
    self.gcomprisBoard.sublevel = 1
    self.next_level()


  def increment_level(self):
    self.gcomprisBoard.sublevel += 1

    if(self.gcomprisBoard.sublevel > self.gcomprisBoard.number_of_sublevel):
      self.gcomprisBoard.sublevel = 1
      self.gcomprisBoard.level += 1
      if(self.gcomprisBoard.level > self.gcomprisBoard.maxlevel):
        self.gcomprisBoard.level = 1

    return 1


  # Setup the game stage
  def base_setup(self):
    gcompris.set_background(self.gcomprisBoard.canvas.get_root_item(), "encryption/background.jpg")
    gcompris.bar_set(gcompris.BAR_LEVEL)
    gcompris.bar_set_level(self.gcomprisBoard)
    gcompris.bar_set(gcompris.BAR_LEVEL|gcompris.BAR_REPEAT_ICON)
    gcompris.bar_location(630, -1, 0.5)
    p = key_value(self.rootitem, self.VALUE)
    self.display_arrow()
    self.display_images(p.get_pair())


  def next_level(self):

    self.rootitem.remove()

    if (self.gcomprisBoard.sublevel == 1):
      self.VALUE = self.NUMBERS
    elif (self.gcomprisBoard.sublevel == 2):
      self.VALUE = self.SYMBOLS
    elif (self.gcomprisBoard.sublevel == 3):
      self.VALUE = self.ALPHABETS

    gcompris.bar_set_level(self.gcomprisBoard)
    self.rootitem = goocanvas.Group(parent = \
      self.gcomprisBoard.canvas.get_root_item())

    self.base_setup()


  def display_arrow(self):
    x_init = 40
    n = 26
    for i in range (0,n/2):
      goocanvas.Image(parent = self.rootitem,
                    pixbuf = gcompris.utils.load_pixmap("encryption/arrow.png"),
                    x = x_init,
                    y = 65,
                    )
      goocanvas.Image(parent = self.rootitem,
                    pixbuf = gcompris.utils.load_pixmap("encryption/arrow.png"),
                    x = x_init,
                    y = 155,
                    )
      x_init = x_init + 58

  # Generate random number between l and u
  def gen_random(self, l, u):
    return random.randrange(l, u)

  def display_images(self, pair):
    # Number of letters according to the level
    if self.gcomprisBoard.level == 1:
      nos = 3
    elif self.gcomprisBoard.level == 2:
      nos = 5
    elif self.gcomprisBoard.level == 3:
      nos = 7

    self.points = 0
    self.pair = pair

    # Empty the letter list
    letters = []

    # Randomly generate a list of `nos` numbers 
    # between 65 and 90. 65 and 90 are ascii 
    # character code for A and Z
    for i in range(nos):
      while True:
        num = self.gen_random(65, 91)
        if num not in letters:
          letters.append(num)
          break

    # Convert the numbers in the list to letters
    letters = map(lambda x: chr(x), letters)

    # Initial reference position of tux
    pos_x = 50

    rand_pos = range(nos)
    random.shuffle(rand_pos)

    for index, l in enumerate(letters):
      tux = Tux(self, pos_x + (index*100), 270, l, str(self.pair[l]), rand_pos.pop())

    goocanvas.Text(parent = self.rootitem,
                   x = 220,
                   y = 250,
                   fill_color = "black",
                   font = gcompris.skin.get_font("gcompris/subtitle"),
                   anchor = gtk.ANCHOR_CENTER,
                   text = _("Place the tux on appropriate ice patch")
                   ) 

  # To be run on a win
  def win(self):
    self.increment_level()
    gcompris.sound.play_ogg("sounds/tuxok.wav")
    gcompris.bonus.display(gcompris.bonus.WIN, gcompris.bonus.TUX)

  # Increment game points
  def increment_points(self):
    self.points += 1
    if ((self.gcomprisBoard.level == 1) and (self.points == 3)):
      self.win()

    elif ((self.gcomprisBoard.level == 2) and (self.points == 5)):
      self.win()

    elif ((self.gcomprisBoard.level == 3) and (self.points == 7)):
      self.win()


# A Tux
class Tux:
  # x and y are initial position of the tux
  # letter is the letter on tux's body
  # value is the value for the above letter
  # rp is random position
  def __init__(self, encrypt, x, y, letter, value, rp):
    self.rootitem = encrypt.rootitem
    self.image = gcompris.utils.load_pixmap("encryption/tux.png")
    self.inc_points = encrypt
    self.value = value

    # Tux initial position
    self.init_pos_x = x
    self.init_pos_y = y

    # Tux position
    self.x = self.init_pos_x
    self.y = self.init_pos_y

    # Center of the tux from it's edges
    self.center_x = 50
    self.center_y = 55

    # Position of ice
    self.ice_x = 50 + (rp * 100)
    self.ice_y = 430

    # Tux image
    self.tux_item = goocanvas.Image(parent = self.rootitem,
                                    pixbuf = self.image,
                                    x = self.x,
                                    y = self.y
                                    )
    self.tux_item_press_handler = \
      self.tux_item.connect("button_press_event",
                          self.tux_move, self)
    self.tux_item_motion_handler = \
      self.tux_item.connect("motion_notify_event",
                          self.tux_move, self)
    self.tux_item_release_handler = \
      self.tux_item.connect("button_release_event",
                          self.tux_move, self)

    # Letter on Tux
    self.tux_letter = goocanvas.Text(parent = self.rootitem,
                                     x = self.x + self.center_x,
                                     y = self.y + self.center_y,
                                     fill_color = "blue",
                                     font = gcompris.skin.get_font("gcompris/subtitle"),
                                     anchor = gtk.ANCHOR_CENTER,
                                     text = letter
                                     )
    self.tux_letter_press_handler = \
      self.tux_letter.connect("button_press_event",
                            self.tux_move, self)
    self.tux_letter_motion_handler = \
      self.tux_letter.connect("motion_notify_event",
                            self.tux_move, self)
    self.tux_letter_release_handler = \
      self.tux_letter.connect("button_release_event",
                            self.tux_move, self)

    ice = Ice(self, self.ice_x, self.ice_y, self.value)


  def move(self, x, y):
    self.x = x - self.center_x
    self.y = y - self.center_y

    self.tux_item.set_properties(x = self.x,
                                 y = self.y
                                 )
    self.tux_letter.set_properties(x = self.x + self.center_x,
                                   y = self.y + self.center_y
                                   )
 
  def tux_move(self, widget, target, event, tux):
    if event.type == gtk.gdk.BUTTON_PRESS:
      pass
     
    if event.type == gtk.gdk.MOTION_NOTIFY:
      if event.state & gtk.gdk.BUTTON1_MASK:
        tux.move(event.x, event.y)

    elif event.type == gtk.gdk.BUTTON_RELEASE:
      if (event.x > self.ice_x and event.x < \
         (self.ice_x + 100)) and (event.y > 430 \
          and event.y < 480):
          self.tux_item.disconnect(self.tux_item_press_handler)
          self.tux_item.disconnect(self.tux_item_motion_handler)
          self.tux_item.disconnect(self.tux_item_release_handler)

          self.tux_letter.disconnect(self.tux_letter_press_handler)
          self.tux_letter.disconnect(self.tux_letter_motion_handler)
          self.tux_letter.disconnect(self.tux_letter_release_handler)
          self.inc_points.increment_points()

      else:
        tux.move(self.init_pos_x + self.center_x,
                 self.init_pos_y + self.center_y)


    return True


# An Ice piece
class Ice:
  def __init__(self, encrypt, x, y, number):
    self.rootitem = encrypt.rootitem
    self.image = gcompris.utils.load_pixmap("encryption/ice_patch.png")

    self.x = x
    self.y = y

    self.center_x = 50
    self.center_y = 25

    self.ice_item = goocanvas.Image(parent = self.rootitem,
                                    pixbuf = self.image,
                                    x = x,
                                    y = y
                                    )
    
    self.ice_number = goocanvas.Text(parent = self.rootitem,
                                     x = self.x + self.center_x,
                                     y = self.y + self.center_y,
                                     fill_color = "red",
                                     font = gcompris.skin.get_font("gcompris/subtitle"),
                                     anchor = gtk.ANCHOR_CENTER,
                                     text = number
                                     )
    self.ice_number.lower(None)
    self.ice_item.lower(None)
