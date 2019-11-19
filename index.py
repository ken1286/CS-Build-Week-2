import json
import requests
import sys
import os
import time
import winsound

url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
token = os.environ['MY_KEY']
print(token)


def init():
    r = requests.get(
        url=url+'/init/',
        headers={'Authorization': f'Token {token}'}
    )

    try:
        data = r.json()
        return data
    except:
        data = r.json
        return data
        print('Error')


def move(dir, room_id=None):
    if room_id == None:
        dirobj = {'direction': f'{dir}'}
    else:
        dirobj = {'direction': f'{dir}', 'next_room_id': f'{room_id}'}
    r = requests.post(
        url=url+'/move/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirobj
    )

    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


def move_cont(dir):
    cur_room = move(dir)
    # == 'You cannot move that way: +5s CD':
    # if len(cur_room['errors']) > 0:
    #     return cur_room
    if len(cur_room['errors']) == 0:
        print(cur_room)
        time.sleep(cur_room['cooldown'])
        cur_room = move_cont(dir)
    return cur_room


def move_cont_count(dir, count):
    counter = int(count)
    while counter > 0:
        cur_room = move(dir)
        print(cur_room)
        time.sleep(cur_room['cooldown'])
        counter -= 1
        if len(cur_room['errors']) > 0:
            break
    return cur_room


def get_item(item):
    dirobj = {'name': f'{item}'}
    r = requests.post(
        url=url+'/take/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirobj
    )

    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


def status():
    r = requests.post(
        url=url+'/status/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        })

    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


def sell(item):
    dirobj = {'name': f'{item}', 'confirm': 'yes'}
    r = requests.post(
        url=url+'/sell/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirobj
    )

    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


def examine(item):
    dirobj = {'name': f'{item}'}
    r = requests.post(
        url=url+'/examine/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirobj
    )

    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


if __name__ == '__main__':
    current_room = init()
    print(current_room)
    while True:
        print(current_room)
        print('COOLDOWN REMAINING: ' + str(current_room['cooldown']))
        time.sleep(current_room['cooldown'])
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        cmds = input("-> ").lower().split(" ")
        print(cmds)
        if cmds[0] in ["n", "s", "e", "w"]:
            if len(cmds) == 1:
                current_room = move(cmds[0])  # move
            else:
                # move and predict room #
                current_room = move(cmds[0], cmds[1])
        elif cmds[0] == 'c':
            if cmds[1] in ["n", "s", "e", "w"] and len(cmds) < 3:
                # move direction until stopped
                current_room = move_cont(cmds[1])
            elif len(cmds) > 2:
                # move x times in direction
                current_room = move_cont_count(cmds[1], cmds[2])
        elif cmds[0] == 'get':
            treasure = f'{cmds[1]} {cmds[2]}'
            get_item(treasure)
        elif cmds[0] == 'sell':
            treasure = f'{cmds[1]} {cmds[2]}'
            sell(treasure)
        elif cmds[0] == 'examine':
            item = f'{cmds[1]}'
            print(examine(item))
        elif cmds[0] == 'status':
            print(status())
        elif cmds[0] == 'q':
            sys.exit(0)
        else:
            print("I did not understand that command.")
