import sys
import yaml
import argparse

ordered_keys = ['t', 'i', 'c', 'v']

def lemma(string):
    return string.split()[0]

def reversed_lemma(string):
    return lemma(string)[::-1]

def print_entry(header, data, file = sys.stdout):
    print('{}:'.format(header), file = file)
    for key in ordered_keys:
        if key in data:
            print(' {}: {}'.format(key, data[key]), file = file)
    for key in data:
        if key not in ordered_keys:
            print(' {}: {}'.format(key, data[key]), file = file)
    print(file = file)

def print_yaml_header(file = sys.stdout):
    for line in ['%YAML 1.1', '---', '']:
        print(line, file = file)
 
def to_sorted(in_file, out_file, key):
    with open(in_file, 'r') as f:
        raw_data = yaml.safe_load(f)
    with open(out_file, 'w') as f:
        print_yaml_header(f)
        for header in sorted(raw_data, key = key):
            print_entry(header, raw_data[header], file = f)

def to_reverse(in_file, out_file):
    to_sorted(in_file, out_file, reversed_lemma)

def to_direct(in_file, out_file):
    to_sorted(in_file, out_file, lemma)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort the YAML dictionary')
    parser.add_argument('-i', nargs = 1, help = 'Input file')
    parser.add_argument('-o', nargs = 1, help = 'Output file')
    parser.add_argument('-r', action = 'store_const', const = True, help = 'Reverse dictionary')
    args = parser.parse_args()
    fun = to_reverse if args.r else to_direct
    fun(args.i[0], args.o[0])
