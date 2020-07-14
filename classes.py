class Client:
    def __init__(self, id=0, name=None, map=None, skills=None, status='kicked', pos=None, navigation=None, same_hp_count=0, prev_hp=101, not_found=0, hp_history=[]):
        self.id = id
        self.name = name
        self.map = map
        self.skills = skills
        self.status = status
        self.pos = pos
        self.navigation = navigation
        self.same_hp_count = same_hp_count
        self.prev_hp = prev_hp
        self.not_found = not_found
        self.hp_history = hp_history

class Map:
    def __init__(self, dir, navigation, object_detection):
        self.dir = dir
        self.navigation = navigation
        self.object_detection = object_detection