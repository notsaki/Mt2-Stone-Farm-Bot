import bmath
import bfile
import classes

def get_value_by_name(list, name):
    for r in list:
        if name == r.name:
            return r

    return None

def get_resolution():
    r = 0    
    while r < 1 or r > len(res):
        res = bfile.get_files('config\\relatives')
        for i in range(0, len(res)):
            res[i] = res[i][:-4]
            res[i] = res[i][17:]
            print(str(i + 1) + '.', res[i])
        r = int(input('Select resolution: '))

    return res[r - 1]

def init_settings():
    resolution = get_resolution()
    client_list, map_list, relative_values_list = bfile.get_settings(resolution)
    clients = []
    maps = []
    relative_values = []

    # Normalize data.
    # Get accounts.
    for c in client_list:
        if c['account']['enabled'] == 'true':
            name = c['account']['username']
            pos = c['position']['pos']
            channel = c['account'].getint('channel')
            map = c['account']['map']
            id = c['account'].getint('id')
            ring = c['navigation']['ring']
            horse_slash = c['horse-skills']['slash']
            navigation = {
                'task_bar': bmath.get_tuple(c['navigation']['task-bar']), 
                'top_left': bmath.get_tuple(c['navigation']['top-left']), 
                'window_size': bmath.get_tuple(relative_values_list['window-size']['val'])
            }

            skills = []
            if 'skills' in c:
                for k, j in c['skills'].items():
                    skills.append(j)
            else:
                skills = None

            clients.append(classes.Client(id=int(id), 
                                    name=name, 
                                    map=map, 
                                    channel=channel, 
                                    skills=skills, 
                                    status='kicked', 
                                    pos=pos, 
                                    navigation=navigation, 
                                    same_hp_count=0, 
                                    prev_hp=101, 
                                    not_found=0,
                                    ring=ring,
                                    horse_slash=horse_slash))

    # Get maps.
    for m in map_list:
        name = m['map']['name']
        dir = m['stone-sample']['dir']
        navigation = [
            bmath.get_tuple(m['navigation']['menu']), 
            bmath.get_tuple(m['navigation']['area'])
        ]
        object_detection = {
            'method': bmath.method_to_const(m['object-detection']['method']), 
            'hl': m['object-detection'].getint('hl'), 
            'threshold': m['object-detection'].getfloat('threshold')
        }

        maps.append(classes.Map(name, dir, navigation, object_detection))

        # Get relative values.
        for k, r in relative_values_list.items():
            if k == 'DEFAULT':
                continue
            values = bmath.get_tuple(r['val'])
            relative_values.append(classes.Relatives(k, values))


    return clients, maps, relative_values