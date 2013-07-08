#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# This class display a braille char to a given location
# The char may be static of dynamic. It maintains the value
# of the dots and the char it represents in real time.
#
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import goocanvas
import pango
import string
import random

# For assigning different key-value for different levels
# Initializing all variables
# For assigning different keys for different levels
ALPHABET = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
key_level1 = range(1,27) #numbers assigned random
key_level2 = ["!","@","#","$","%","^","&","*","(",")","{","}","?","/","<",">",":",";",".","-","+","=","[","]","|",","]

class key_value:

  def __init__(self, rootitem, value):
    # Number of characters
    n = 26

    # Type of value
    if (value == 1):
      global key_level1
      self.temp = key_level1[:]
    elif (value == 2):
      global key_level2
      self.temp = key_level2[:]
    elif (value == 3):
      global ALPHABET
      self.temp = ALPHABET[:]

    # Shuffle the values
    random.shuffle(self.temp)

    # Pair key and values in a dictionary
    self.pair = {}
    for index, alphabet in enumerate(ALPHABET):
      self.pair[alphabet] = self.temp[index]

    self.rootitem = goocanvas.Group(parent = rootitem)
    goocanvas.Rect(parent=self.rootitem,
                   x=10,
                   y=20,
                   width=780,
                   height=200,
                   stroke_color="black",
                   fill_color="white",
                   line_width=1.0
                   )

    fill_color = 0x80e072eeL
    stroke_color = 0xed6d6deeL
    fill_color1 = 0xed6d6deeL
    stroke_color1 = 0x80e072eeL

    x1 = 35
    y1 = 35

    # dynamic display width for multigraphs
    xshift=n*0.25
    w = 5*xshift
    h = 30
    y2 = y1+h+20
    y3 = y2+h+10
    y4 = y3+h+20

    # Draw the boxes
    for i in range(n/2):
      # Row 1 Upper box
      self.rect = goocanvas.Rect(
        parent = self.rootitem,
        x = x1,
        y = y1,
        width = w,
        height = h,
        fill_color_rgba = fill_color,
        stroke_color_rgba = stroke_color,
        line_width = 1.0)

      # Row 2 Upper box
      self.rect = goocanvas.Rect(
        parent = self.rootitem,
        x = x1,
        y = y3,
        width = w,
        height = h,
        fill_color_rgba = fill_color,
        stroke_color_rgba = stroke_color,
        line_width = 1.0)

      # Row 1 Lower box
      self.rect = goocanvas.Rect(
        parent = self.rootitem,
        x = x1,
        y = y2,
        width = w,
        height = h,
        fill_color_rgba = fill_color1,
        stroke_color_rgba = stroke_color1,
        line_width = 1.0)

      # Row 2 Lower box
      self.rect = goocanvas.Rect(
        parent = self.rootitem,
        x = x1,
        y = y4,
        width = w,
        height = h,
        fill_color_rgba = fill_color1,
        stroke_color_rgba = stroke_color1,
        line_width = 1.0)
      x1 = x1+w+25

    # Write numbers inside box of Row 1
    x1 =42
    for index in range(0,n/2):

      goocanvas.Text(
            parent = self.rootitem,
            x = x1+2,
            y = y1+7+2*h,
            text = self.temp[index],
            fill_color="black",
            anchor = gtk.ANCHOR_CENTER,
            alignment = pango.ALIGN_CENTER,
            font = 'SANS 10'
            )
      x1 = x1+w+25

    # Write numbers inside box of Row 2
    x1 =42
    y1 = h+100
    for index in range((n/2),n):

      goocanvas.Text(
            parent = self.rootitem,
            x = x1+5,
            y = y1+5+(2*h),
            text = self.temp[index],
            fill_color="black",
            anchor = gtk.ANCHOR_CENTER,
            alignment = pango.ALIGN_CENTER,
            font = 'SANS 10'
            )
  
      x1 = x1+w+25

    # Line dividing the two rows
    goocanvas.Polyline(
          parent = self.rootitem,
          points = goocanvas.Points([(10, 120),
                                     (790,120 )]),
          fill_color = "black",
          line_width = 1.0
          )

    # Write alphabets inside boxes of Row 1
    x1 = 42
    y1 = 30
    for index in range(0,n/2):
      goocanvas.Text(
            parent = self.rootitem,
            x = x1,
            y = y1+12,
            text = ALPHABET[index],
            fill_color="black",
            anchor = gtk.ANCHOR_CENTER,
            alignment = pango.ALIGN_CENTER,
            font = 'SANS 10'
            )

      x1 = x1+w+25

    # Write alphabets inside boxes of Row 2
    x1 =42
    y1 = h+100
    for index in range((n/2),n):
      goocanvas.Text(
            parent = self.rootitem,
            x = x1,
            y = y1+12,
            text = ALPHABET[index],
            fill_color="black",
            anchor = gtk.ANCHOR_CENTER,
            alignment = pango.ALIGN_CENTER,
            font = 'SANS 10'
            )

      x1 = x1+w+25

  # Returns a dictionary of key-value pairs
  def get_pair(self):
    return self.pair
