import pandas as pd
import numpy as np


names = ["num_rows", "width", "total_eye_movement", "total_pen_movement", "total_symbols_written", "facts_recalled", "gets"]

def to_roman_string(num):
    vals = [1000, 500, 100, 50, 10, 5, 1]
    letters = ['M', 'D', 'C', 'L', 'X', 'V', 'I']

    out = ''
    for v, l in zip(vals, letters):
        out += l * (num // v)
        num %= v

    return out

def dataset_to_coordinates(dataset, normalizer):
    outs = [name + '\n\t coordinates {' for name in names]

    for i, (vals, count) in enumerate(zip(dataset, normalizer)):
        if count != 0:
            outs = [s + f"({i*4},{v/count})" for s, v in zip(outs, vals)]
    
    [print(s +"};") for s in outs]

if __name__ == '__main__':
    files = ['data/macbeth_again.csv', 'data/milton_again.csv']

    for file in files:
        print(file)
        df = pd.read_csv(file)
        by_roman_length_divisor = [np.zeros(len(names)) for _ in range(20)]
        by_roman_length_dividend = [np.zeros(len(names)) for _ in range(20)]
        by_dividend_value = [np.zeros(len(names)) for _ in range(40)]
        by_divisor_value  = [np.zeros(len(names)) for _ in range(40)]

        divisor_value_counts = [0] * 40
        dividend_value_counts = [0] * 40
        divisor_counts = [0] * 20
        dividend_counts = [0] * 20
        by_sum = [np.zeros(len(names)) for _ in range(40)]
        sum_counts = [0] * 40
        

        count = 0
        for row in df.iterrows():
            # num_rows = row[1]["num_rows"]
            # width = row[1]["width"]
            # total_eye_movement = row[1]["total_eye_movement"]
            # total_pen_movement= row[1]["total_pen_movement"]
            total_symbols_written = row[1]["total_symbols_written"]
            # facts_recalled = row[1]["facts_recalled"]
            vals = np.asarray([row[1][name] for name in names])
            divisor  = row[1]["divisor"]
            dividend = row[1]["dividend"]
            # it seems my divisors and dividends have switched
            divisor, dividend = dividend, divisor

            dividend_len = len(to_roman_string(dividend))
            divisor_len = len(to_roman_string(divisor))


            by_divisor_value[divisor//4] += vals
            by_dividend_value[(dividend-500)//140] += vals
            divisor_value_counts[divisor//4] += 1
            dividend_value_counts[(dividend-500)//140] += 1

            by_roman_length_dividend[dividend_len] += vals
            by_roman_length_divisor[divisor_len] += vals
            by_sum[divisor_len + dividend_len] += vals
            dividend_counts[dividend_len] += 1
            divisor_counts[divisor_len] += 1
            sum_counts[dividend_len + divisor_len] += 1

        for dataset, normalizer, name in [(by_divisor_value, divisor_value_counts, "divisor_value"),(by_dividend_value, dividend_value_counts, "dividend_value"), (by_roman_length_divisor, divisor_counts, "by_divisor"), (by_roman_length_dividend, dividend_counts, "by_dividend"), (by_sum, sum_counts, "by_sum")]:
            if name not in ["dividend_value", "divisor_value"]: continue
            print(name)
            print(normalizer)
            dataset_to_coordinates(dataset, normalizer)

            