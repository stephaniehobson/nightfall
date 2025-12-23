#!/usr/bin/env python3
# Visual indication of time using blinkstick
# Copyright (C) 2019  Stephanie Hobson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime, argparse, random, time
import blinkstick
import usb

def get_step_color(from_color, to_color, transition_duration, transition_progress, verbose):
    transition_range =  to_color - from_color
    if verbose:
        print('  %s' % transition_range)
    if transition_duration == 0:
        if verbose:
            print('  transition_duration is 0, returning from_color')
        return from_color
    single_step = transition_range / transition_duration
    if verbose:
        print('  %s' % single_step)
    current_step = single_step * transition_progress
    if verbose:
        print('  %s' % current_step)
    new_color = from_color + current_step
    return new_color

def christmas_light_mode(bstick, verbose=False):
    """
    Christmas light mode: randomly cycles through festive colors with smooth transitions
    """
    christmas_colors = [
        [255, 0, 0],      # Red
        [0, 255, 0],      # Green
        [255, 255, 255],  # White
        [255, 215, 0],    # Gold
        [0, 100, 255],    # Blue
        [128, 0, 128],    # Purple
        [255, 192, 203],  # Pink
        [64, 224, 208],   # Turquoise
        [65, 105, 225],   # Royal Blue
    ]
    
    fade_duration = 5  # seconds to fade between colors
    hold_duration = 20  # seconds to hold the color
    update_interval = 0.1  # seconds between updates (smoother = smaller value)
    
    current_color = [0, 0, 0]  # Start from off
    
    if verbose:
        print("Starting Christmas light mode (Press Ctrl+C to stop)")
    
    try:
        while True:
            # Pick a random target color different from the current one
            target_color = random.choice(christmas_colors)
            while target_color == current_color:
                target_color = random.choice(christmas_colors)
            
            if verbose:
                print(f"Transitioning to {target_color}")
            
            # Fade to the new color
            steps = int(fade_duration / update_interval)
            for step in range(steps + 1):
                red = get_step_color(current_color[0], target_color[0], fade_duration, step * update_interval, False)
                green = get_step_color(current_color[1], target_color[1], fade_duration, step * update_interval, False)
                blue = get_step_color(current_color[2], target_color[2], fade_duration, step * update_interval, False)
                
                try:
                    bstick.set_color(channel=0, index=0, red=int(red), green=int(green), blue=int(blue))
                except usb.USBError as e:
                    if verbose:
                        print(f"USB error: {e}")
                
                time.sleep(update_interval)
            
            # Update current color to target
            current_color = target_color
            
            if verbose:
                print(f"Holding color for {hold_duration} seconds")
            
            # Hold the color
            time.sleep(hold_duration)
            
    except KeyboardInterrupt:
        if verbose:
            print("\nChristmas mode stopped")
        # Turn off the light
        bstick.set_color(channel=0, index=0, red=0, green=0, blue=0)

parser = argparse.ArgumentParser(description='Visual indication of time using blinkstick')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                    help='suppress normal output')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='enable extra debugging output')
parser.add_argument('-t', '--time', dest='time',
                    type=str,
                    help='UTC formated time (e.g. 20:07:00)')
parser.add_argument('-d', '--day', dest='day',
                    type=int, choices=range(0, 7),
                    help='Day of the week (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday)')
parser.add_argument('--christmas', dest='christmas', action='store_true',
                    help='enable Christmas light mode (random color cycling)')
args = parser.parse_args()

if not args.quiet or args.verbose:
    print("Starting...")

if args.time:
    current_time = datetime.datetime.strptime(args.time, '%H:%M:%S').time()
    # Use today's date for weekday check even with custom time
    current_date = datetime.datetime.today()
else:
    current_date = datetime.datetime.today()
    current_time = current_date.time()

# Override the day of week if specified
if args.day is not None:
    # Calculate the offset to the desired day
    current_weekday = current_date.weekday()
    days_offset = args.day - current_weekday
    current_date = current_date + datetime.timedelta(days=days_offset)

if not args.quiet or args.verbose:
    print('current time:' + str(current_time))
    print('day of week: %s (%d)' % (current_date.strftime('%A'), current_date.weekday()))


weekend_colors = [
    {
        'time': '06:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '06:15:00',
        'color': [0, 255, 0] # green - wake up
    },
    {
        'time': '06:40:00',
        'color': [0, 255, 0] # green 
    },
    {
        'time': '06:45:00',
        'color': [255, 255, 0] # yellow - eat
    },
    {
        'time': '07:35:00',
        'color': [255, 255, 0] # yellow
    },
    {
        'time': '07:40:00',
        'color': [102, 255, 255] #sky 
    },
    {
        'time': '08:59:00',
        'color': [102, 255, 255] #sky 
    },
    {
        'time': '09:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '16:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '17:30:00',
        'color': [102, 255, 255] #sky 
    },
    {
        'time': '18:35:00',
        'color': [102, 255, 255] #sky
    },
    {
        'time': '18:40:00',
        'color': [60, 0, 128] #darkpurple
    },
    {
        'time': '20:00:00',
        'color': [60, 0, 128] #darkpurple
    },
    {
        'time': '20:30:00',
        'color': [250, 200, 0] #yellow - don't start anything new
    },
    {
        'time': '20:45:00',
        'color': [255, 30, 0] #burnt orange - finish up, head to bed
    },
    {
        'time': '21:00:00',
        'color': [255, 0, 0] #red - go to bed RIGHT NOW
    },
    {
        'time': '21:30:00',
        'color': [135, 0, 0] #dark red - there's no help for you
    },
    {
        'time': '23:00:00',
        'color': [0, 0, 0] #off
    }
]

weekday_colors = [
    {
        'time': '06:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '06:15:00',
        'color': [0, 255, 0] # green - wake up
    },
    {
        'time': '06:40:00',
        'color': [0, 255, 0] # green 
    },
    {
        'time': '06:45:00',
        'color': [255, 255, 0] # yellow - eat
    },
    {
        'time': '07:35:00',
        'color': [255, 255, 0] # yellow
    },
    {
        'time': '07:40:00',
        'color': [255, 0, 0] # red - get ready
    },
    {
        'time': '08:59:00',
        'color': [255, 0, 0] # red
    },
    {
        'time': '09:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '16:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '17:30:00',
        'color': [102, 255, 255] #sky 
    },
    {
        'time': '18:35:00',
        'color': [102, 255, 255] #sky
    },
    {
        'time': '18:40:00',
        'color': [60, 0, 128] #darkpurple
    },
    {
        'time': '20:00:00',
        'color': [60, 0, 128] #darkpurple
    },
    {
        'time': '20:30:00',
        'color': [250, 200, 0] #yellow - don't start anything new
    },
    {
        'time': '20:45:00',
        'color': [255, 30, 0] #burnt orange - finish up, head to bed
    },
    {
        'time': '21:00:00',
        'color': [255, 0, 0] #red - go to bed RIGHT NOW
    },
    {
        'time': '21:30:00',
        'color': [135, 0, 0] #dark red - there's no help for you
    },
    {
        'time': '23:00:00',
        'color': [0, 0, 0] #off
    }
]

#define speed of transition
transition_duration = 10
transition_progress = 5

# Determine if today is a weekday (Monday=0, Sunday=6)
# is_weekday = current_date.weekday() < 5  # Monday-Friday are 0-4
is_weekday = False # vacay!

# Set colors based on weekday or weekend
if is_weekday:
    colors = weekday_colors
    if not args.quiet or args.verbose:
        print('Using weekday colors')
else:
    colors = weekend_colors
    if not args.quiet or args.verbose:
        print('Using weekend colors')

# Always resolve a color and time, even if current_time is outside the defined ranges
from_color = colors[0]['color']
from_time = datetime.datetime.strptime(colors[0]['time'], '%H:%M:%S').time()
to_color = colors[0]['color']
to_time = from_time
found = False
for index, key in enumerate(colors):
    this_time = datetime.datetime.strptime(key['time'], '%H:%M:%S').time()
    if current_time < this_time:
        to_color = key['color']
        to_time = this_time
        # Use previous color/time if available, else first
        if index > 0:
            from_color = colors[index-1]['color']
            from_time = datetime.datetime.strptime(colors[index-1]['time'], '%H:%M:%S').time()
        found = True
        if args.verbose:
            print('next time ' + str(to_time))
        break
    else:
        from_color = key['color']
        from_time = this_time

# If current_time is after the last color, use the last color for both from and to
if not found:
    to_color = from_color
    to_time = from_time

transition_duration_time = (datetime.datetime.combine(datetime.date.today(), to_time) - datetime.datetime.combine(datetime.date.today(), from_time))
transition_duration = transition_duration_time.total_seconds()
transition_progress_time = (datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), from_time))
transition_progress = transition_progress_time.total_seconds()
if args.verbose:
    print(str(transition_progress))

if args.verbose:
    print('red:')
red = get_step_color(from_color[0], to_color[0], transition_duration, transition_progress, args.verbose)
if args.verbose:
    print('green:')
green = get_step_color(from_color[1], to_color[1], transition_duration, transition_progress, args.verbose)
if args.verbose:
    print('blue:')
blue = get_step_color(from_color[2], to_color[2], transition_duration, transition_progress, args.verbose)

for bstick in blinkstick.find_all():
    #if True:
    if args.christmas:
        if not args.quiet or args.verbose:
            print("Starting Christmas light mode")
        christmas_light_mode(bstick, args.verbose)
    else:
        if not args.quiet or args.verbose:
            print("setting color")
        try:
            bstick.set_color(channel=0, index=0, red=red, green=green, blue=blue, name=None, hex=None)
        except usb.USBError as e:
            if not args.quiet or args.verbose:
                print("failed: %s" % e)

if not args.quiet or args.verbose:
    print("...done")
