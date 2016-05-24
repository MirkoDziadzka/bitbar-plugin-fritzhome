#!/usr/bin/env python
# <bitbar.title>Fritz Dect Devices</bitbar.title>
# <bitbar.author></bitbar.author>
# <bitbar.author.github>MirkoDziadzka</bitbar.author.github>
# <bitbar.desc>See Status of Fritz devices</bitbar.desc>
# <bitbar.dependencies>python,fritzhome</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/MirkoDziadzka/bitbar-plugin-fritzhome<bitbar.abouturl>

import sys
import os
import os.path
import subprocess
import time
import argparse
import urllib

# get fritzhome with "pip install fritzhome"
from fritzhome.actor import Actor
from fritzhome.fritz import FritzBox

# see the README.md for username and password
HOSTNAME = "fritz.box"
USERNAME = "smarthome"
PASSWORD = ""
if not PASSWORD:
    print("ERROR| color=red")
    print("---")
    print("edit the plugin and set USERNAME and PASSWORD for your fritz box|color=red")
    print("file: " + os.path.abspath(__file__) + "|color=red")
    sys.exit(1)


def make_call(prog, *args):
    res = []
    res.append('bash="{0}"'.format(prog))
    for i, arg in enumerate(args):
        res.append('param{0}="{1}"'.format(i + 1, arg))
    return " ".join(res)


def main(device=None, action=None):
    parser = argparse.ArgumentParser(description='fritzhome devices')
    parser.add_argument('--device', help='the device actor id')
    parser.add_argument('--action', help='on or off')

    args = parser.parse_args()

    box = FritzBox(HOSTNAME, USERNAME, PASSWORD)
    try:
        box.login()
    except Exception as e:
        print(str(e))
        sys.exit(1)

    if args.device is not None:
        actor = box.get_actor_by_ain(urllib.unquote(args.device))
        if actor is not None:
            if args.action == "on":
                actor.switch_on()
            elif args.action == "off":
                actor.switch_off()

    actors_on = []
    actors_off = []
    total_power = 0

    for actor in sorted(box.get_actors(), key=lambda a: a.actor_id):
        power = actor.get_power()
        if power == 0:
            actors_off.append(actor)
        else:
            actors_on.append(actor)
            total_power += power

    if actors_on:
        print("%d On (%d W)| color=red" % (len(actors_on), total_power / 1000))
    else:
        print("All Off| color=green")
    print("---")
    for actor in actors_on:
        text = "{1} ({0}) is using {2} W - switch off".format(actor.actor_id, actor.name, actor.get_power() / 1000)
        action = make_call(sys.argv[0], "--device", urllib.quote(actor.actor_id), "--action", "off")
        print("%s|%s terminal=false refresh=true" % (text, action))
    for actor in actors_off:
        text = "switch {1} ({0}) on".format(actor.actor_id, actor.name)
        action = make_call(sys.argv[0], "--device", urllib.quote(actor.actor_id), "--action", "on")
        print("%s|%s terminal=false refresh=true" % (text, action))


if __name__ == '__main__':
    main()

