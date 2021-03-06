#
#  (C) Copyright 2001/2002/2003 Kai Sterker <kaisterker@linuxgames.com>
#  Part of the Adonthell Project http://adonthell.linuxgames.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY.
#
#  See the COPYING file for more details
#

# -- Movement schedule for all characters to get to Bjarn's room

import adonthell
import random

class to_cellar:

    def __init__ (self, mapcharacterinstance):
        self.myself = mapcharacterinstance

        # -- gives the proper exit for each submap to reach Bjarn's room
        # (yard, common room, parlour, kitchen, cellar, bath, Alek's room,
        # Bjarn's room, store room, 1st floor Fellnir's room, Frostbloom's
        # room, Player's room, Silverhair's room)
        self.exits = \
            [(18, 13, adonthell.STAND_NORTH), \
            (9, 1, adonthell.STAND_NORTH), \
            (0, 4, adonthell.STAND_WEST), \
            (6, 6, adonthell.STAND_SOUTH), \
            (10, 7, adonthell.STAND_EAST), \
            (4, 7, adonthell.STAND_SOUTH), \
            (6, 6, adonthell.STAND_EAST), \
            (-1, -1, -1), \
            (7, 3, adonthell.STAND_EAST), \
            (8, 1, adonthell.STAND_NORTH), \
            (0, 3, adonthell.STAND_WEST), \
            (5, 3, adonthell.STAND_EAST), \
            (5, 1, adonthell.STAND_NORTH), \
            (5, 1, adonthell.STAND_NORTH), \
            (4, 1, adonthell.STAND_SOUTH)]

        self.myself.set_callback (self.walk)


    def walk (self):        
        x, y, dir = self.exits[self.myself.submap ()]

        # -- in Bjarn's room
        if x == -1:
            self.myself.set_callback (self.goal_reached)
            
            submap = self.myself.mymap ().get_submap (self.myself.submap ())
            x = random.randint (2, 5)
            y = random.randint (5, 9)

            while not submap.get_square (x, y).is_free () or (y == 5 and x > 2):
                x = random.randint (2, 5)
                y = random.randint (5, 9)

            # -- calculate direction
            # -- north-western area
            if x + y < 10:
                if x + 3 > y: dir = adonthell.STAND_SOUTH
                else: dir = adonthell.STAND_EAST
            # -- south-east corner
            else:
                if y - (x + 3) > 0: dir = adonthell.STAND_NORTH
                else: dir = adonthell.STAND_WEST

        if not self.myself.set_goal (x, y, dir):
            self.myself.time_callback ("1t", self.walk)

    # -- teleport to the next exit
    def warp (self):
        x, y, dir = self.exits[self.myself.submap ()]
        self.myself.jump_to (self.myself.submap (), x, y, dir)
        self.myself.time_callback ("1t", self.walk)

    # -- reached Bjarn's room
    def goal_reached (self):
        if self.myself.get_name () == adonthell.gamedata_player ().get_name ():
            self.myself.set_schedule ("keyboard_control")
            bjarn = adonthell.gamedata_get_character ("Bjarn Fingolson")
            bjarn.set_dialogue ("dialogues.extro")
            bjarn.pause ()
            bjarn.launch_action (self.myself)
                        
        else:
            if self.myself.posx () == 1 and self.myself.posy () == 7:
                self.walk ()
            else:
                self.myself.pause ()
