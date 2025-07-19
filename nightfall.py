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

import datetime, argparse
import blinkstick
import usb

def get_step_color(from_color, to_color, transition_duration, transition_progress, verbose):
    transition_range =  to_color - from_color
    if verbose:
        print('  %s' % transition_range)
    single_step = transition_range / transition_duration
    if verbose:
        print('  %s' % single_step)
    current_step = single_step * transition_progress
    if verbose:
        print('  %s' % current_step)
    new_color = from_color + current_step
    return new_color

parser = argparse.ArgumentParser(description='Visual indication of time using blinkstick')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                    help='suppress normal output')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='enable extra debugging output')
parser.add_argument('-t', '--time', dest='time',
                    type=str,
                    help='UTC formated time (e.g. 20:07:00)')
args = parser.parse_args()

if not args.quiet or args.verbose:
    print("Starting...")

if args.time:
    current_time = datetime.datetime.strptime(args.time, '%H:%M:%S').time()
else:
    current_time = datetime.datetime.today().time()

if not args.quiet or args.verbose:
    print('current time:' + str(current_time))

colors = [
    {
        'time': '17:00:00',
        'color': [0, 0, 0] #off
    },
    {
        'time': '17:30:00',
        'color': [102, 255, 255] #sky - whatevs
    },
    {
        'time': '18:30:00',
        'color': [255, 102, 255] #pink - brush teeth
    },
    {
        'time': '19:00:00',
        'color': [60, 0, 128] #darkpurple - boring
    },
    {
        'time': '19:30:00',
        'color': [102, 255, 255] #sky - whatevs
    },
    {
        'time': '20:45:00',
        'color': [250, 200, 0] #yellow - don't start anything new
    },
    {
        'time': '21:00:00',
        'color': [255, 30, 0] #burnt orange - finish up, head to bed
    },
    {
        'time': '21:20:00',
        'color': [255, 0, 0] #red - go to bed RIGHT NOW
    },
    {
        'time': '21:50:00',
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

#set variable values to be over ridden later if a better match is found
to_time = datetime.datetime.strptime(colors[0]['time'], '%H:%M:%S').time() 
from_color = [0, 0, 0]
from_time = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time() 

for key in colors:
    this_time = datetime.datetime.strptime(key['time'], '%H:%M:%S').time()
    if this_time > current_time:
        to_color = key['color']
        to_time = datetime.datetime.strptime(key['time'], '%H:%M:%S').time()
        if args.verbose:
            print('next time ' + str(to_time))
        break
    else:
        from_color = key['color']
        from_time = datetime.datetime.strptime(key['time'], '%H:%M:%S').time()
        

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
    if not args.quiet or args.verbose:
        print("setting color")
    try:
        bstick.set_color(channel=0, index=0, red=red, green=green, blue=blue, name=None, hex=None)
    except usb.USBError as e:
        if not args.quiet or args.verbose:
            print("failed: %s" % e)

if not args.quiet or args.verbose:
    print("...done")
