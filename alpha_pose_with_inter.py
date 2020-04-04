import os
import json

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import multiprocessing
from multiprocessing import Pool

from tqdm import tqdm
# {0,  "Nose"},
# {1,  "Neck"},
# {2,  "RShoulder"},
# {3,  "RElbow"},
# {4,  "RWrist"},
# {5,  "LShoulder"},
# {6,  "LElbow"},
# {7,  "LWrist"},
# {8,  "RHip"},
# {9,  "RKnee"},
# {10, "RAnkle"},
# {11, "LHip"},
# {12, "LKnee"},
# {13, "LAnkle"},
# {14, "REye"},
# {15, "LEye"},
# {16, "REar"},
# {17, "LEar"},

lines = [(0, 1), 
        #  (0, 14), (0, 15),
         (1, 2), (1, 5), 
         (1, 18), (18, 8), (18, 11),
         (2, 3), (3, 4), (5, 6), (6, 7),
         (8, 9), (9, 10), (11, 12), (12, 13),
        #  (14, 16), (15, 17)
        ]

def which_color(points):
    if any(map(lambda x:x>1400, points)):
        return 0
    if any(map(lambda x:x>1000, points)):
        return 1
    else:
        return 2

#['blue', 'red', 'green']

color_list = ['#006ab6', '#fb2f78', '#0bc8c2']
color = 'red'
mark = 4

img_dir = f'videos/{mark}'
output_dir = f'output/{mark}'
json_res_path = os.path.join(output_dir, 'alphapose-results.json')
with open(json_res_path) as f:
    json_data = json.load(f)
    # json_data = {i['image_id']: i['keypoints'] for i in json_data}

def plot_alphapose_json(inter = 10):
    # firt get seq
    imgs = [i for i in os.listdir(img_dir) if i.find('.png') > 0]
    imgs = sorted(imgs)
    seqs = [] # frame * 18 * 2
    for fname in imgs:
        if fname in json_data:
            item = json_data[fname]
            peoples = [i for i in item['bodies']]
            # assert len(peoples) == 1
            joints = peoples[0]['joints']
            lens = len(joints)
            tmp = []
            assert lens == 18 * 3
            p_number = lens // 3 
            for i in range(p_number):
                x = int(joints[i * 3])
                y = int(joints[i * 3 + 1])
                z = float(joints[i * 3 + 2])
                tmp.append((x, y))
            seqs.append(tmp)
            
        else:
            tmp = []
            for i in range(18):
                x = 0
                y = 0
                tmp.append((x, y))
            seqs.append(tmp)
    seqs = np.array(seqs)
    print(seqs.shape)
    frames = seqs.shape[0]
    for i in tqdm(range(frames // inter)):
        begin_i = i * inter
        end_i = (i+1) * inter
        actions = seqs[begin_i: end_i]
        c = actions.reshape(10, -1)
        t1 = c.min(axis=0, keepdims=1)
        t2 = c.max(axis=0, keepdims=1)
        d = (c.sum(axis=0) - t1 - t2) / (inter - 2)
        # d = (c * m).sum(axis=0) / m.sum(axis=0)
        action = d.reshape(18, 2)
        # print(i*10, action)
        plot_it(f'{i+1:0>5}.png', action)
        

def plot_it(fname, action):

    img_fpath = os.path.join(img_dir, fname)
    img = Image.open(img_fpath)
    if action.sum() > 0:
        joints = action
        lens = len(joints)
        tmp = action
        assert lens % 3 == 0
        p_number = lens // 3

        for i in range(p_number):
            x = tmp[i][0]
            y = tmp[i][1]
            if i in [14, 15, 16, 17]:
                continue
            plt.scatter(x, y, s = 36, color=color)

        point = np.array(((tmp[8][0] + tmp[11][0])/2, (tmp[8][1] + tmp[11][1])/2))
        tmp = np.concatenate([tmp, point.reshape(1, -1)])
        # tmp = np.array(tmp)
        # print(tmp)
        plt.scatter(point[0], point[1], s=36, color=color)
        for line in lines:
            item_1 = tmp[line[0]]
            item_2 = tmp[line[1]]
            x1 = item_1[0]
            x2 = item_2[0]
            y1 = item_1[1]
            y2 = item_2[1]
            dis = (x1-x2)**2+(y1-y2)**2
            dis = np.sqrt(dis)
            if dis > 400:
                continue
            plt.plot((x1, x2), (y1, y2), color=color, linewidth= 4)
        face = ( (tmp[16][0] + tmp[17][0])/2, (tmp[16][1] + tmp[17][1])/2)
        face_s = np.sqrt( (tmp[17][1] -  tmp[16][1]) ** 2 + (tmp[17][0] - tmp[16][0])**2 )/2
        face_s = (face_s) ** 2 
        face_s = 1600
        face = np.array((tmp[0][0], tmp[0][1] - 20))
        face_v = tmp[1]-tmp[0]
        face_v_l = np.sqrt(np.sum(face_v**2))
        # neck_l = 30
        neck_l = 90
        point =  tmp[1] - face_v * (neck_l) / face_v_l
        # plt.scatter(point[0], point[1], s=20, color='white')
        print(face)
        plt.scatter(face[0], face[1], s=face_s, color=color)

    img_np = np.array(img)
    # img_np = np.zeros(img.size)
    img_np = np.zeros(img_np.shape)
    # img_np = np.ones(img_np.shape)
    plt.imshow(img_np)
    # mng = plt.get_current_fig_manager()
    # mng.window.showMaximized()
    # mng.window.state('zoomed')
    # plt.figure(figsize=(1.92, 1.08), dpi=100)
    plt.axis('off')
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.tight_layout(pad=0,h_pad=0,w_pad=0)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
    # plt.show()
    res_fpath = os.path.join(output_dir, '{}'.format(fname))
    plt.savefig(res_fpath, dpi=500/1.673, bbox_inches='tight', pad_inches=0)
    plt.clf()

def main():
    plot_alphapose_json()

if __name__ == '__main__':
    main()
    # multiprocessing.freeze_support()
    # f_lists = os.listdir(img_dir)
    # pool = Pool(8)
    # pool.map(plot_alphapose_json, f_lists)
    # pool.close()
    # pool.join()
    # fname = '00408.png'
    # plot_alphapose_json(fname)
    # fname = '00409.png'
    # plot_alphapose_json(fname)


