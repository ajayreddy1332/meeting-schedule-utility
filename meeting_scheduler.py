import os


class RoomInfo(object):
    """
    Room information mapper with details of floor no., room no., time slots
    """
    def __init__(self, floor_no, room_no, time_slots):
        self.floor_no = floor_no
        self.room_no = room_no
        self.time_slots = time_slots


class Duration(object):
    """
    Slots details of Floor and Meeting room
    """

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


class Rooms(object):
    """
    Available meeting rooms data
    """

    def __init__(self):
        self._rooms = {}
        self._min_team_size = 0
        self._max_team_size = 0

    def get_max_team_size(self):
        return self._max_team_size

    def process_rooms_from_file(self):
        cwd = os.getcwd()
        rooms_path = cwd + '/rooms.txt'
        with open(rooms_path, "r") as file:
            for line in file.readlines():
                room_info_list = line.strip().split(',')
                room_floor = room_info_list[0].split('.')
                floor_no = room_floor[0]
                room_no = room_floor[1]
                team_size = int(room_info_list[1])
                if not self._min_team_size or team_size < self._min_team_size:
                    self._min_team_size = team_size
                if not self._max_team_size or team_size > self._max_team_size:
                    self._max_team_size = team_size

                slots = []
                for ind in range(2, len(room_info_list), 2):
                    start_time = float(room_info_list[ind].replace(':', '.'))
                    end_time = float(room_info_list[ind+1].replace(':', '.'))
                    duration = Duration(start_time, end_time)
                    slots.append(duration)

                room_info = RoomInfo(floor_no, room_no, slots)
                if team_size not in self._rooms:
                    self._rooms[team_size] = [room_info]
                else:
                    self._rooms[team_size].append(room_info)

    def get_rooms_cache(self):
        return self._rooms


def find_room(team_size, floor_no, start_time, end_time, rooms):
    available_rooms = []
    rooms_cache = rooms.get_rooms_cache()
    end_time = float(end_time.replace(':', '.'))
    start_time = float(start_time.replace(':', '.'))
    duration_time = end_time - start_time
    for ts in range(team_size, rooms.get_max_team_size()):
        if ts not in rooms_cache:
            continue

        room_info_list = rooms_cache[ts]
        slots = []
        for ind in range(len(room_info_list)):
            for ri_ts in room_info_list[ind].time_slots:
                if start_time >= ri_ts.start_time and end_time <= ri_ts.end_time:
                    st = ri_ts.start_time
                    et = ri_ts.end_time
                    duration = Duration(st, et)
                    slots.append(duration)
                    break
            if slots:
                room_info = RoomInfo(room_info_list[ind].floor_no, room_info_list[ind].room_no, slots)
                available_rooms.append(room_info)
    return available_rooms


if __name__ == "__main__":
    rooms = Rooms()
    Rooms.process_rooms_from_file(rooms)

    team_size = 5
    start_time = '10:30'
    end_time = '11:30'
    floor_no = 8

    available_rooms = find_room(team_size, floor_no, start_time, end_time, rooms)
    for room in available_rooms:
        print ("Available meeting floor No. and room No.: {}".format(room.floor_no + "." + room.room_no))
