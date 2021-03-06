#
#  (C) Copyright 2001 Alexandre Courbot <alexandrecourbot@linuxgames.com>
#  Part of the Adonthell Project http://adonthell.linuxgames.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY.
#
#  See the COPYING file for more details
#

# -- Introduction sequence for Waste's Edge. 
#
#    Dirty, ugly, quickly made, random programmed.

from adonthell import *

# -- pygettext support
def _(message): return nls_translate (message)

def update_im (im, x):
    if x <= -im.length (): x = x + im.length ()
    else: x = x - 1
    return x

def draw_im (im, x):
    im.draw (x, 0, da)
    if x < screen_length () - im.length (): im.draw (im.length () + x, 0, da)

# Our drawing area for the scrolling forest.
da = drawing_area ()
da.resize (screen_length (), screen_height ())
da.move (0, 0)

# The images...
im1 = image ()
im2 = image ()
im3 = image ()
bg = image ()
inn_close = image ()
talan = image ()
player = image ()

im1.load_raw ("gfx/cutscene/forest3.img")
im2.load_raw ("gfx/cutscene/forest2.img")
im2.set_mask (1)
im3.load_raw ("gfx/cutscene/forest1.img")
im3.set_mask (1)
bg.load_raw ("gfx/cutscene/intro_bg.img")
bg.set_alpha (0)
inn_close.load_raw ("gfx/cutscene/intro_inn.img")
inn_close.set_mask (1)
talan.load_raw ("gfx/cutscene/intro_talan.img")
talan.set_mask (1)
player.load_raw ("gfx/cutscene/player.img")
player.set_mask (1)

imblack = image ()
imblack.resize (screen_length (), screen_height ())
imblack.fillrect (0, 0, imblack.length (), imblack.height (), 0)

# ...their x coordinate...
x1 = 0
x2 = 0
x3 = 0

# ...and their delay time.
o1 = 0
o2 = 0
o3 = 0

# The text window.
theme = win_manager_get_theme ("original")
font = win_manager_get_font ("white")
cont = win_container ()
cont.resize (250, 100)
cont.move ((screen_length () - cont.length ())/2,
           (screen_height () - cont.height ())/4)

cont.set_border (theme)
cont.set_background (theme)
cont.set_trans_background (1)

lab = win_label ()
lab.move (5, 5)
lab.resize (cont.length () - 10, cont.height () - 10)
lab.set_font (font)
lab.pack ()

cont.add (lab)

wintext = (_("One week out of Cirdanth, the trail had\nbecome hard. I had begun to wonder\ndays ago whether \
it could still be called\na trail, but it was the only way the\ncaravans had."),
           _("There were no caravans now, only me,\nand I had seen few others on the road.\nEven those had \
become more scarce\nthe further I went."),
           _("It was easy to see why."),
           _("The Lady Silverhair, intent on her\nmission, had gone on ahead while I was\nleft to complete \
business in her name,\ntrusting me to follow in good speed."),
           _("A lone Half-Elf may travel with much\nmore speed than an Elven lady and her\nservants, so she \
was now only a day\nahead.  The thought nearly caused me\nto forget \
the harshness of the road."),
           _("Still, Waste's Edge was a welcome sight."),
           _("As you approach the trading post, there\nseems to be little sign of life.      \
           \n       \nEventually you find the Redwyne Inn,\nwhich seems to be the main building\nhere."),
           _("The heavy wooden doors are closed,\nand no one is there \
to let you in. As you\napproach the gate, you suddenly hear a voice from within."),
           _("                      \nSuddenly, it looked like the day would\nbe harder than I thought ..."))

cont.set_visible_background (0);
cont.set_visible_border (0);
cont.set_visible_all (1);
cont.set_activate (1)

# Images for the speech
bubbg = (0, image(), image())
bubbg[1].load_raw ("gfx/cutscene/intro_guard.img")
bubbg[2].load_raw ("gfx/cutscene/intro_player.img")

# Text for the speech
if gamedata_player () != None: myname = gamedata_player ().get_name ()
else: myname = "Banec"

bubtext = ((_("Halt! Stand and declare yourself, stranger!"), "red", 25, 5, 350, 1),
           (_("I am ") + myname + _(", come as an agent for my employer. Tell me, is this the trading \
post of Waste's Edge?"), "yellow", 130, 5, 500, 2),
           (_("That it is, but this is all you'll see of it."), "red", 25, 5, 300, 1),
           (_("If you turn now and make haste, you should be able to make safe camping \
before dark."), "red", 25, 5, 400, 1),
           (_("Turn back?  Whatever for?  And why is the gate of a free Inn locked \
against a footsore traveller?"), "yellow", 140, 20, 500, 0),
           (_("I am sorry, traveller, but the Inn is barred and you must be off."), "red", 25, 5, 300, 0),
           (_("There has been trouble inside and I have instructions to turn away all who \
need not be here."), "red", 25, 5, 400, 0),
           (_("Trouble?  Why then, I must get inside.  My employer will need me close at \
hand!"), "yellow", 140, 30, 500, 0))

# The audio
audio_load_background (0, "audio/at-demo-2.ogg");
audio_load_background (1, "audio/at-demo-3.ogg");
audio_load_background (2, "audio/at-demo-4.ogg");

wintextocc = 0
wincpt = 0
windelay = 0
bgcpt = 0

bgy = 0
bgvelocity = 0.18

inny = 510
innvelocity = 0.4

ply = 843
plvelocity = 0.5

status = -1

letsexit = 0

screen_clear ()

gametime_start_action ()
audio_play_background (0)

while not input_has_been_pushed (SDLK_ESCAPE) and not input_has_been_pushed (SDLK_SPACE) and not letsexit:
    # Update the stuff
    input_update ()
    for i in range (0, gametime_frames_to_skip ()):

        # 1st part: forest scrolling and fade to the inn, with
        #the text appearing letter-by-letter
        if status < 4:
            # Magic number
            if o1 >= 4:
                x1 = update_im (im1, x1)
                o1 = 0
            else: o1 = o1 + 1

            # Magic number
            if o2 >= 2:
                x2 = update_im (im2, x2)
                o2 = 0
            else: o2 = o2 + 1

            # Magic number
            if o3 >= 1:
                x3 = update_im (im3, x3)
                o3 = 0
            else: o3 = o3 + 1

            # Update the label text
            if wintextocc < len (wintext) - 1:
                if wincpt < len (wintext[wintextocc]):
                    windelay = windelay + 1
                    if windelay >= 10:
                        if wincpt == 0: lab.set_text ("")
                        lab.add_text (wintext[wintextocc][wincpt])
                        if wintext[wintextocc][wincpt] == '.': windelay = -50
                        else: windelay = 0
                        wincpt = wincpt + 1
                    else:
                        windelay = windelay + 1
                        # Shall we fade to the Inn view?
                        if status == 0 and wintextocc == 5 and windelay == - 250: status = 1
                else:
                    wintextocc = wintextocc + 1
                    wincpt = 0
                    windelay = -500
            else:
                # Switch to close inn view?
                if windelay == -300:
                    audio_play_background (2)
                    status = 4
                    windelay = 0
                    wintextocc = 0
                else: windelay = windelay + 1
            
            cont.update ()

            # Fade to the forest
            if status == -1:
                if (imblack.alpha ()) > 0:
                    imblack.set_alpha (imblack.alpha () - 1)
                else: status = 0

            # Fade to the Inn view.
            if status == 1:
                if (bg.alpha ()) < 255:
                    bg.set_alpha (bg.alpha () + 1)
                    if bg.alpha () == 255:
                        # Start scrolling
                        status = 2
                        audio_play_background (1)

            if status == 2:
                if inny > - (inn_close.height () - screen_height ()):
                    bgy = bgy + bgvelocity
                    inny = inny - innvelocity
                    ply = ply - plvelocity
                else: status = 3

        # 2nd part: speech between Talan and the player.
        if status == 4:
            if windelay >= 0 and wintextocc < len (bubtext):
                windelay = -bubtext[wintextocc][4]
                bub = text_bubble (bubtext[wintextocc][0], bubtext[wintextocc][1], "original")
                bub.move (bubtext[wintextocc][2], bubtext[wintextocc][3])
                windelay = windelay + 1
                currentbg = bubtext[wintextocc][5]
            else:
                windelay = windelay + 1
                if windelay >= 0:
                    wintextocc = wintextocc + 1
                    if wintextocc == len (bubtext):
                        status = 5
                        wintextocc = len (wintext) - 1
                        wincpt = 0
                        windelay = 0
                        lab.set_text ("")

        if status == 5:
            if wincpt < len (wintext[wintextocc]):
                windelay = windelay + 2
                if windelay >= 10:
                    lab.add_text (wintext[wintextocc][wincpt])
                    wincpt = wincpt + 1
                    windelay = 0
            else:
                windelay = windelay + 1
                # Shall we fade to the Inn view?
                if windelay == 500: letsexit = 1
            
    
    # Draw the entire scene
    if status < 2:
        draw_im (im1, x1)
        draw_im (im2, x2)
        draw_im (im3, x3)

    if status > 0 and status < 4:
        bg.draw (0, int(-bgy), da)
        inn_close.draw (0, int(inny), da)
        player.draw (167, int(ply), da)

    if status == -1:
        imblack.draw (0, 0)

    if status >= 4:
        if currentbg == 0:
            bg.draw (0, int(-bgy), da)
            inn_close.draw (0, int(inny), da)
            player.draw (167, int(ply), da)
            talan.draw (51, 39)
        else: bubbg[currentbg].draw (0, 0)
            
        if status == 4: bub.draw ()
    
    if status != 4:
        cont.draw ()

    screen_show ()
    gametime_update ()

audio_unload_background (0)
audio_unload_background (1)
audio_unload_background (2)

# Avoid a bad crash...
cont.remove (lab)
