from math import inf
from PIL import Image
import numpy as np
import pandas as pd


def lerp_color(in_color, out_color, scale): 
    def lerp(ammont):
        v = ammont / scale
        return in_color * (1-v) + out_color * v
    return lerp

def np_to_picture(data, out_name='my_img'):
    img = Image.fromarray(data, 'RGB')
    img.save(f'data/{out_name}.png')

def slope_intercept(slope, intercept, maximum=inf):
    def ymxb(x):
        return min(x * slope + intercept, maximum)
    return ymxb   

if __name__ == "__main__":
    file_names = ['data/milton.csv']
    dfs = [pd.read_csv(file, sep=',') for file in file_names]
    scale_nr = 201
    scale_width = 202
    for df, n in zip(dfs, file_names):
        df['divisor'] = df['divisor'] - 500
        _, _, _, _, _, _, _, w,h = df.max()

        data_nr = np.zeros((w+1, h+1, 3), dtype=np.int8)
        data_width = np.zeros((w+1, h+1, 3), dtype=np.int8)

        color_scale_nr = lerp_color(np.asarray([0, 0, 255]), np.asarray([255, 0, 0]), scale_nr)
        color_scale_width = lerp_color(np.asarray([0, 0, 255]), np.asarray([255, 0, 0]), scale_width)

        lines = [
            slope_intercept(1/50, 10),
            slope_intercept(2/50, 20),
            slope_intercept(1/50 * 1.5, 10*1.5),
            slope_intercept(1/100, 5)
        ]

        for row in df.iterrows():
            x = row[1]["divisor"]
            y = row[1]["dividend"]
            v1 = row[1]["num_rows"]
            v2 = row[1]["width"]
            data_nr[x, y] = color_scale_nr(v1)
            data_width[x, y] = color_scale_width(v2)
            """ for r in [5, 10, 50, 100, 500, 1000]:
                if y % r == 0 or x % r == 0:
                    data_nr[x, y] += np.asarray([0, 16, 0], dtype=np.int8)
                    data_width[x, y] += np.asarray([0, 16, 0], dtype=np.int8) """
            # for line in lines:
            #     if int(line(x)) == y:
            #         data_nr[x, y] += np.asarray([0, 100, 0], dtype=np.int8)
            #         data_width[x, y] += np.asarray([0, 100, 0], dtype=np.int8)
        np_to_picture(data_nr, out_name=f"{n[5:-4]}_rows_used_macbeth_scale")
        np_to_picture(data_width, out_name=f"{n[5:-4]}_colums_used_macbeth_scale")

        