"""
explain_columns.py - explain the columns of a csv file
"""

import argparse
import csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("from_file")
    parser.add_argument("to_file")
    args = parser.parse_args()

    with open(args.from_file,'r') as fin:
        cin = csv.reader( fin )
        header = next(cin)

    with open(args.to_file,'w') as fout:
        cout = csv.writer(fout)
        cout.writerow(['column','header'])
        for (i, name) in enumerate(header):
            cout.writerow( [i,name] )

if __name__=="__main__":
    main()
