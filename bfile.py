import os
import glob
import configparser
import cv2 as cv

def get_files(dir):
    # Get sample images from a directory. They will be used to find patterns on the screenshot.
    data_path = os.path.join(dir, '*g')
    files = glob.glob(data_path)

    return files

def get_settings(res):
    client = get_config('config\\clients\\', 'screen')
    maps = get_config('config\\maps\\')
    relatives = get_config('config\\relatives\\', res)

    return client, maps, relatives[0]

def get_config(dir='', name=''):
    files = get_files(dir)
    
    config = []
    for f in files:
        if len(name) < 1 or name in f:
            cfg = configparser.ConfigParser()
            cfg.read(f)
            config.append(cfg)

    return config

def get_images(dir, name):
    files = get_files(dir)
    data = []

    for f in files:
        if len(name) <= 0 or name in f:
            img = cv.imread(f, cv.TM_CCOEFF)
            data.append(img)

    return data