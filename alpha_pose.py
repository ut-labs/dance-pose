import os
import json

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import multiprocessing
from multiprocessing import Pool

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
    json_data = {i['image_id']: i['keypoints'] for i in json_data}

def plot_alphapose_json(fname):
    img_fpath = os.path.join(img_dir, fname)
    img = Image.open(img_fpath)
    if fname in json_data:
        joints = json_data[fname]
        lens = len(joints)
        tmp = []
        assert lens % 3 == 0
        p_number = lens // 3
        # 0-1 dist
        dis_01 = (joints[0] - joints[1*3])**2 + (joints[1] - joints[1*3+1])**2
        if dis_01 > 10000:
            joints[0] = joints[3] +np.sqrt(4000) / np.sqrt(dis_01) * (joints[0]  - joints[3]) 
            joints[1] = joints[3+1] + np.sqrt(4000) / np.sqrt(dis_01) * (joints[1]  - joints[3+1]) 
        # print(dis_01)
        for i in range(p_number):
            x = int(joints[i * 3])
            y = int(joints[i * 3 + 1])
            z = float(joints[i * 3 + 2])
           
            tmp.append((x, y))
            if i in [14, 15, 16, 17]:
                continue
            plt.scatter(x, y, s = 36, color=color)

        point = ((tmp[8][0] + tmp[11][0])/2, (tmp[8][1] + tmp[11][1])/2)
        tmp.append(point)
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
        face_s = (np.sqrt( (tmp[17][1] -  tmp[16][1]) ** 2 + (tmp[17][0] - tmp[16][0])**2 )/2)
        face_s = (face_s + 12) ** 2  / 4
        # print(face_s)
        # def max_dis(origin, tmp):
        #     tmp_list = [14, 15, 16, 17]
        #     dis_max = 600
        #     for j in tmp_list:
        #         dis_max_1 = (origin[0] - tmp[j][0]) ** 2 + (origin[1] - tmp[j][1]) ** 2
        #         if dis_max_1 > dis_max and dis_max_1 < 5000:
        #             dis_max = dis_max_1
        #         print(dis_max_1)
        #     return dis_max  
        # face_s = max_dis(tmp[0], tmp)
        face_s = 600
        face = (tmp[0][0], tmp[0][1])
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
    res_fpath = os.path.join(output_dir, '{}.format(fname)')
    plt.savefig(res_fpath, dpi=500/1.673, bbox_inches='tight', pad_inches=0)
    plt.clf()


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    # f_lists = os.listdir('images')
    # pool = Pool(8)
    # pool.map(gao_image, f_lists)
    # pool.close()
    # pool.join()
    fname = '01956.png'
    # fname = '02578.png'
    # fname = '00801.png'
    gao_image(fname)




