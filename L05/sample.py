"""
sample.py - sample a csv file
"""

import argparse
import csv
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("from_file")
    parser.add_argument("to_file")
    parser.add_argument("sample_size", type=int)
    args = parser.parse_args()

    with open(args.from_file, 'r') as fin:
        csv_in = csv.reader(fin)

        with open(args.to_file, 'w') as fout:
            csv_out = csv.writer(fout)

            csv_out.writerow( next(csv_in) )  # copy over the header

            i = 0
            for row in csv_in:
                if random.randint(1,10) == 7:
                    csv_out.writerow(row)
                    i += 1
                    if i >= args.sample_size:
                        break

if __name__=="__main__":
    main()
