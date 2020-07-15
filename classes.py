class Client:
    def __init__(self, id=0, name=None, map=None, channel=4, skills=None, status='kicked', pos=None, navigation=None, same_hp_count=0, prev_hp=101, not_found=0, hp_history=[], ring=None, horse_slash=None, count_stuck=0):
        self.id = id
        self.name = name
        self.map = map
        self.channel = channel
        self.skills = skills
        self.status = status
        self.pos = pos
        self.navigation = navigation
        self.same_hp_count = same_hp_count
        self.prev_hp = prev_hp
        self.not_found = not_found
        self.hp_history = hp_history
        self.ring = ring
        self.horse_slash = horse_slash
        self.count_stuck = count_stuck

class Map:
    def __init__(self, name, dir, navigation, object_detection):
        self.name = name
        self.dir = dir
        self.navigation = navigation
        self.object_detection = object_detection

class Relatives:
    def __init__(self, name, value):
        self.name = name
        self.value = value