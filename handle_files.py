import os
import re
import sys
import time
import json
import math
import random
import pickle
import logging
import argparse
import subprocess

from collections import defaultdict

import scipy as sc
import numpy as np
import pandas as pd

from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--dirpath', default=BASE_DIR, help='当前目录')
args = parser.parse_args()


def rename_files():
    dirname = 'videos'
    flist = [os.path.join(dirname, fname) for fname in os.listdir(dirname)]
    rs_f = open(os.path.join(dirname, 'map.txt'), 'w', encoding='utf8')
    for ind, fpath in enumerate(flist):
        name = f"{ind}.mp4"
        fpath2 = os.path.join(dirname, name)
        print(fpath, fpath2, file=rs_f)
        rs_dir = os.path.join(dirname, f'{ind}')
        if not os.path.exists(rs_dir):
            os.mkdir(rs_dir)
        os.rename(fpath, fpath2)
        cmdline = f'ffmpeg -i {fpath2} -r 30 -f image2 {rs_dir}/%5d.png'
        subprocess.run(cmdline, shell=True)
        print(cmdline)
    rs_f.close()

def run_models():
    cmdline = 'python demo.py --indir videos/4 --outdir output/4'



def main():
    rename_files()
    
if __name__ == "__main__":
    main()

