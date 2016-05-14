#!/usr/local/bin/python
# use 5.010;
# use strict;
# use warnings;

# say("Yo");

# my @userinput = <STDIN>;
# foreach my $input (@userinput) {
#         print $input;
#         chomp($input);
#         if($input eq "^[[D") {
#             say("baspinga left");
#         }
#         else {
#             say("nope");
#         }
# }


# Modelling my code after https://github.com/Max00355/SpaceInvaders to jump into pygame
import pygame
from pygame.locals import *
import sys
import random
import math
import colorsys as cs
# import time


from subprocess import call




# Take from SO
#   https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # Ones I'm Using
    TEAL_TEXT = '\033[36m'
    TEAL = '\033[46m'


color_cycle = [
  '\033[46m',
  '\033[45m',
  '\033[44m',
  '\033[43m',
  '\033[42m',
  '\033[41m'
]


# # Returns RGB tuple that shifts from start_col to end_col based on percent in the HSV colorspace. start_col and end_col are RGB tuples, each component ranges from 0.0-1.0. Percent ranges from 0.0-1.0 (hmmm... not the best name here)
# def rgb_shift_hsv(start_col, end_col, percent):
#   start_hsv = cs.rgb_to_hsv(start_col[0], start_col[1], start_col[2])
#   end_hsv = cs.rgb_to_hsv(end_col[0], end_col[1], end_col[2])
#   hdiff = end_hsv[0] - start_hsv[0]
#   sdiff = end_hsv[1] - start_hsv[1]
#   vdiff = end_hsv[2] - start_hsv[2]

#   new_hsv = (start_hsv[0] + hdiff * percent, 
#     start_hsv[1] + sdiff * percent, 
#     start_hsv[2] + vdiff * percent)
  
#   return cs.hsv_to_rgb(new_hsv[0], new_hsv[1], new_hsv[2])

# # inputs are hsv and outputs to rgb
# def hsv_shift_hsv(start_col, end_col, percent):
#   hdiff = end_col[0] - start_col[0]
#   sdiff = end_col[1] - start_col[1]
#   vdiff = end_col[2] - start_col[2]

#   new_hsv = (start_col[0] + hdiff * percent, 
#     start_col[1] + sdiff * percent, 
#     start_col[2] + vdiff * percent)
  
#   return cs.hsv_to_rgb(new_hsv[0], new_hsv[1], new_hsv[2])


class WallpaperChange:
  def __init__(self):

    self.screen = pygame.display.set_mode((1,1))

    self.fps = 60
    self.frame = 0
    self.change_timeout = 0.1 * self.fps       # Timeout between wallpaper changes

    self.count = 0              # Number of times wallpaper changed
    # self.change_timeout

    self.printheader()

  def printheader(self):
    print("==--==~~==--==~~==--==~~==--==~~ ~~==--==~~==--==~~==--==~~==--==")
    print("                        Wallpaper Changer")
    print("==--==~~==--==~~==--==~~==--==~~ ~~==--==~~==--==~~==--==~~==--==")


  def print_count(self):


    block_width = 30


    # cur_color = color_cycle[ (self.count // block_width) % (len(color_cycle))]
    # cur_color = color_cycle[ (self.count // 2) % (len(color_cycle))]

    sys.stdout.write("\r")
    sys.stdout.flush()

    sys.stdout.write(bcolors.TEAL_TEXT + "[")
    for idx in range(block_width):



      cur_color = color_cycle[ (idx // 5) % (len(color_cycle))]

      if idx <= (self.count%block_width):
        sys.stdout.write(bcolors.ENDC + " " + cur_color + " " + bcolors.ENDC)

      else:
        sys.stdout.write(bcolors.ENDC + "  ")



    sys.stdout.write(" " + bcolors.TEAL_TEXT + "]" + bcolors.ENDC + " " + str(self.count))


  def next_wallpaper(self):
    call(["osascript", "/Users/devgru/code/scripts/apple_scripts/change_all_wallpapers.scpt"])


  def run(self):

    clock = pygame.time.Clock()

    last_key_hit = self.frame
    timed_out = False

    while True:


      key = pygame.key.get_pressed()
      if key[K_q]:
        print("\n\n")
        sys.exit()

      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit()
        if event.type == pygame.KEYDOWN:
          key = pygame.key.get_pressed()

          if (self.frame - last_key_hit > self.change_timeout):
            if key[K_RIGHT]:
              # print("K_RIGHT\n")
              # timed_out = True
              last_key_hit = self.frame
              self.count += 1
              self.next_wallpaper()
            elif key[K_LEFT]:
              # print("K_LEFT\n")
              # print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
              # timed_out = True
              last_key_hit = self.frame

            # if last_key_hit == self.frame:
            #   self.print_count()

      # pygame.display.flip()

      # clock.tick(60)
      clock.tick(self.fps)

      self.frame += 1
      self.print_count()



if __name__ == "__main__":
  pygame.display.init()
  WallpaperChange().run()

