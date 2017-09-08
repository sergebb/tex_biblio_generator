#! /usr/bin/env python

import argparse
import os
import re

def get_citations(tex_file):
    result = []
    with open(tex_file, 'r') as file_data:
        for line in file_data:
            citations = re.findall(r'cite\{.*?\}', line)
            for cite in citations:
                cite_names = [cn.strip() for cn in cite.replace('cite{','').replace('}','').split(',')]
                for cn in cite_names:
                    if cn not in result:
                        result.append(cn)

    return result


def main():
    parser = argparse.ArgumentParser(description='Extract all citation from tex file')
    parser.add_argument("tex_file", help="Input tex file")
    parser_args = parser.parse_args()

    tex_file = parser_args.tex_file
    if not os.path.exists(tex_file):
        parser.error('Input file do not exist')
    elif not os.path.isfile(tex_file):
        parser.error('Not a file')
    elif tex_file.split('.')[-1] != 'tex':
        parser.error('Wrong file type')

    citations = get_citations(tex_file)

    for cite in citations:
        print cite


if __name__ == '__main__':
    main()
