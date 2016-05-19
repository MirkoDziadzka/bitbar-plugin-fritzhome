#!/Users/mirko/fritz.env/bin/python
# <bitbar.title>Fritz Dect Devices</bitbar.title>
# <bitbar.author></bitbar.author>
# <bitbar.author.github>MirkoDziadzka</bitbar.author.github>
# <bitbar.desc>See Status of Fritz devices</bitbar.desc>
# <bitbar.dependencies>python,fritzhome</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/MirkoDziadzka/bitbar-plugin-fritzhome</bitbar.abouturl>


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

HOSTNAME="fritz.box"
USERNAME="smarthome"
PASSWORD=""
assert PASSWORD , "edit this file and set USERNAME and PASSWORD for your fritz.box"

def main(device=None, action=None):
    parser = argparse.ArgumentParser(description='fritzhome devices')
    parser.add_argument('--device', help='the device actor id')
    parser.add_argument('--action', help='on or off')

    args = parser.parse_args()

    box = FritzBox(HOSTNAME, USERNAME, PASSWORD)
    box.login()

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
        print("%d On (%d W)| color=red" % (len(actors_on), power / 1000))
    else:
        print("All Off| color=green")
    print("---")
    for actor in actors_on:
        text = "{1} ({0}) is using {2} W - switch off".format(actor.actor_id, actor.name, actor.get_power() / 1000)
        action = "bash={0} param1=--device param2={1} param3=--action param4=off terminal=false refresh=true".format(sys.argv[0], urllib.quote(actor.actor_id))
        print("%s|%s" % (text, action))
    for actor in actors_off:
        text = "switch {1} ({0}) on".format(actor.actor_id, actor.name)
        action = "bash={0} param1=--device param2={1} param3=--action param4=on terminal=false refresh=true".format(sys.argv[0], urllib.quote(actor.actor_id))
        print("%s|%s" % (text, action))




if __name__ == '__main__':
    main()

