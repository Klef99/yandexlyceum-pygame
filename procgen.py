# Class to produce random map layouts
from random import *
from math import *


def make_room():
    """Randomly produce room size"""
    rtype = 5
    rwide = randrange(8) + 3
    rlong = randrange(8) + 3
    return rwide, rlong, rtype


def make_corridor():
    """Randomly produce corridor length and heading"""
    clength = randrange(18) + 3
    heading = randrange(4)
    if heading == 0:  # North
        wd = 1
        lg = -clength
    elif heading == 1:  # East
        wd = clength
        lg = 1
    elif heading == 2:  # South
        wd = 1
        lg = clength
    elif heading == 3:  # West
        wd = -clength
        lg = 1
    return wd, lg, heading


class Map:
    def __init__(self):
        self.map_array = []
        self.size_y = 0
        self.size_x = 0
        self.roomList = []
        self.cList = []

    def make_map(self, xsize, ysize, fail, b1, mrooms):
        """Generate random layout of rooms, corridors and other features"""
        # makeMap can be modified to accept arguments for values of failed, and percentile of features.
        # Create first room
        self.size_x = xsize
        self.size_y = ysize
        # initialize map to all walls
        self.map_array = []
        for i in range(ysize):
            tmp = []
            for j in range(xsize):
                tmp.append(1)
            self.map_array.append(tmp)

        w, l, t = make_room()
        while len(self.roomList) == 0:
            i = randrange(ysize - 1 - l) + 1
            j = randrange(xsize - 1 - w) + 1
            p = self.place_room(l, w, j, i, xsize, ysize, 6, 0)
        failed = 0
        while failed < fail:  # The lower the value that failed< , the smaller the dungeon
            choose_room = randrange(len(self.roomList))
            ex, ey, ex2, ey2, et = self.make_exit(choose_room)
            feature = randrange(100)
            if feature < b1:  # Begin feature choosing (more features to be added here)
                w, l, t = make_corridor()
            else:
                w, l, t = make_room()
            room_done = self.place_room(l, w, ex2, ey2, xsize, ysize, t, et)
            if room_done == 0:  # If placement failed increase possibility map is full
                failed += 1
            elif room_done == 2:  # Possibility of linking rooms
                if self.map_array[ey2][ex2] == 0:
                    if randrange(100) < 7:
                        self.make_portal(ex, ey)
                    failed += 1
            else:  # Otherwise, link up the 2 rooms
                self.make_portal(ex, ey)
                failed = 0
                if t < 5:
                    tc = [len(self.roomList) - 1, ex2, ey2, t]
                    self.cList.append(tc)
                    self.join_corridor(len(self.roomList) - 1, ex2, ey2, t, 50)
            if len(self.roomList) == mrooms:
                failed = fail
        self.finalJoins()

    def place_room(self, ll, ww, xpos, ypos, xsize, ysize, rty, ext):
        """Place feature if enough space and return can_place as true or false"""
        # Arrange for heading
        xpos = xpos
        ypos = ypos
        if ll < 0:
            ypos += ll + 1
            ll = abs(ll)
        if ww < 0:
            xpos += ww + 1
            ww = abs(ww)
        # Make offset if type is room
        if rty == 5:
            if ext == 0 or ext == 2:
                offset = randrange(ww)
                xpos -= offset
            else:
                offset = randrange(ll)
                ypos -= offset
        # Then check if there is space
        can_place = 1
        if ww + xpos + 1 > xsize - 1 or ll + ypos + 1 > ysize:
            can_place = 0
            return can_place
        elif xpos < 1 or ypos < 1:
            can_place = 0
            return can_place
        else:
            for j in range(ll):
                for k in range(ww):
                    if self.map_array[ypos + j][xpos + k] != 1:
                        can_place = 2
        # If there is space, add to list of rooms
        if can_place == 1:
            temp = [ll, ww, xpos, ypos]
            self.roomList.append(temp)
            for j in range(ll + 2):  # Then build walls
                for k in range(ww + 2):
                    self.map_array[(ypos - 1) + j][(xpos - 1) + k] = 2
            for j in range(ll):  # Then build floor
                for k in range(ww):
                    self.map_array[ypos + j][xpos + k] = 0
        return can_place  # Return whether placed is true/false

    def make_exit(self, rn):
        """Pick random wall and random point along that wall"""
        room = self.roomList[rn]
        while True:
            rw = randrange(4)
            if rw == 0:  # North wall
                rx = randrange(room[1]) + room[2]
                ry = room[3] - 1
                rx2 = rx
                ry2 = ry - 1
            elif rw == 1:  # East wall
                ry = randrange(room[0]) + room[3]
                rx = room[2] + room[1]
                rx2 = rx + 1
                ry2 = ry
            elif rw == 2:  # South wall
                rx = randrange(room[1]) + room[2]
                ry = room[3] + room[0]
                rx2 = rx
                ry2 = ry + 1
            elif rw == 3:  # West wall
                ry = randrange(room[0]) + room[3]
                rx = room[2] - 1
                rx2 = rx - 1
                ry2 = ry
            if self.map_array[ry][rx] == 2:  # If space is a wall, exit
                break
        return rx, ry, rx2, ry2, rw

    def make_portal(self, px, py):
        """Create doors in walls"""
        ptype = randrange(100)
        if ptype > 90:  # Secret door
            self.map_array[py][px] = 5
            return
        elif ptype > 75:  # Closed door
            self.map_array[py][px] = 4
            return
        elif ptype > 40:  # Open door
            self.map_array[py][px] = 3
            return
        else:  # Hole in the wall
            self.map_array[py][px] = 0

    def join_corridor(self, cno, xp, yp, ed, psb):
        """Check corridor endpoint and make an exit if it links to another room"""
        c_area = self.roomList[cno]
        if xp != c_area[2] or yp != c_area[3]:  # Find the corridor endpoint
            endx = xp - (c_area[1] - 1)
            endy = yp - (c_area[0] - 1)
        else:
            endx = xp + (c_area[1] - 1)
            endy = yp + (c_area[0] - 1)
        check_exit = []
        if ed == 0:  # North corridor
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                check_exit.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                check_exit.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                check_exit.append(coords)
        elif ed == 1:  # East corridor
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                check_exit.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                check_exit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                check_exit.append(coords)
        elif ed == 2:  # South corridor
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                check_exit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                check_exit.append(coords)
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                check_exit.append(coords)
        elif ed == 3:  # West corridor
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                check_exit.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                check_exit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                check_exit.append(coords)
        for xxx, yyy, xxx1, yyy1 in check_exit:  # Loop through possible exits
            if self.map_array[yyy][xxx] == 0:  # If joins to a room
                if randrange(100) < psb:  # Possibility of linking rooms
                    self.make_portal(xxx1, yyy1)

    def finalJoins(self):
        """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
        for x in self.cList:
            self.join_corridor(x[0], x[1], x[2], x[3], 10)


def generate_dungeon(filename, xsize, ysize, fail, b1, mrooms):
    file = open(filename, mode='w')
    main_map = Map()
    main_map.make_map(xsize, ysize, fail, b1, mrooms)
    for y in range(ysize):
        line = ""
        for x in range(xsize):
            if main_map.map_array[y][x] == 0:
                line += ":"
            if main_map.map_array[y][x] == 1:
                line += " "
            if main_map.map_array[y][x] == 2:
                line += "#"
            if main_map.map_array[y][x] == 3 or main_map.map_array[y][x] == 4 or main_map.map_array[y][x] == 5:
                line += "="
        file.write(line + '\n')
    file.close()