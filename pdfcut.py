#!/usr/bin/env python3

import sys

import PyPDF2

def parse_ranges(ranges):
    if ranges.isalpha():
        return ranges
    ranges = ranges.split(',')
    ret = []
    for r in ranges:
        if r.find('-') == -1:
            ret.append(int(r))
            continue
        r = r.split('-')
        if len(r) != 2:
            raise RuntimeError('Invalid Range')
        for i in range(int(r[0]), int(r[1]) + 1):
            ret.append(i)
    return ret

def load_pdf(filename, ranges):
    ret = []
    reader = PyPDF2.PdfFileReader(filename)
    num_of_pages = reader.getNumPages()
    if isinstance(ranges, str):
        full = list(range(1, num_of_pages + 1))
        if ranges == 'all':
            ranges = full
        elif ranges == 'odd':
            ranges = full[::2]
        elif ranges == 'even':
            ranges = full[1::2]
        else:
            raise RuntimeError('Invalid Range')
    for r in ranges:
        if r < 1 or r > num_of_pages:
            raise RuntimeError('Invalid Range')
        ret.append(reader.getPage(r - 1))
    return ret

def main(argc, argv):
    if argc <= 2 or argc % 2 == 1:
        print('usage: {} {{infile ranges}} ... outfile'.format(argv[0]), file=sys.stderr)
        sys.exit(1)
    num_of_files = argc // 2 - 1
    out_filename = argv[-1]
    writer = PyPDF2.PdfFileWriter()
    for i in range(num_of_files):
        for page in load_pdf(argv[i * 2 + 1], parse_ranges(argv[i * 2 + 2])):
            writer.addPage(page)
    with open(out_filename, 'wb') as f:
        writer.write(f)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
