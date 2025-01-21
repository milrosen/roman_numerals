from math import inf
from PIL import Image
import numpy as np
import pandas as pd


def lerp_color(in_color, out_color, scale): 
    if scale == 0: scale = 1
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
    file_names = ['data/milton_again.csv', 'data/macbeth_again.csv']
    dfs = [pd.read_csv(file, sep=',') for file in file_names]
    attribute_names = ["num_rows","width","total_eye_movement","total_pen_movement","total_symbols_written","facts_recalled","divisor","dividend","max_stack","gets"]
    scale_nr = 105
    scale_width = 105
    w, h = 3499, 99
    max_vals = np.zeros(len(attribute_names))
    for df in dfs:
        df['divisor'] = df['divisor'] - 500
        max_vals = np.maximum(df.max()[1:], max_vals)
        print(df.max()[1:])
    print(max_vals)

    for df, n in zip(dfs, file_names):
        print(list(zip(max_vals, attribute_names)))
        
        data_nr = np.zeros((w+1, h+1, 3), dtype=np.int8)
        data_width = np.zeros((w+1, h+1, 3), dtype=np.int8)

        color_scale_nr = lerp_color(np.asarray([0, 0, 255]), np.asarray([255, 0, 0]), scale_nr)
        color_scale_width = lerp_color(np.asarray([0, 0, 255]), np.asarray([255, 0, 0]), scale_width)

        data = [np.zeros((w+1, h+1, 3), dtype=np.int8) for  _ in attribute_names]
        scales = [lerp_color(np.asarray([0,0,255]), np.asarray([255,0,0]), scale) for scale in max_vals]

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
            vals = [scale(row[1][attr]) for scale, attr in zip(scales, attribute_names)]
            data_nr[x, y] = color_scale_nr(v1)
            data_width[x, y] = color_scale_width(v2)
            for d, v in zip(data, vals):
                d[x, y] = v
            """ for r in [5, 10, 50, 100, 500, 1000]:
                if y % r == 0 or x % r == 0:
                    data_nr[x, y] += np.asarray([0, 16, 0], dtype=np.int8)
                    data_width[x, y] += np.asarray([0, 16, 0], dtype=np.int8) """
            # for line in lines:
            #     if int(line(x)) == y:
            #         data_nr[x, y] += np.asarray([0, 100, 0], dtype=np.int8)
            #         data_width[x, y] += np.asarray([0, 100, 0], dtype=np.int8)

        [np_to_picture(d, out_name=f"{n[5:-4]}_{attr}") for d,attr in zip(data, attribute_names)]
        np_to_picture(data_nr, out_name=f"{n[5:-4]}_rows_used")
        np_to_picture(data_width, out_name=f"{n[5:-4]}_colums_used")

        