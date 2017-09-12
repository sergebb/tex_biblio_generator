#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import bibtexparser

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

def load_bibtex(bibtex_file_path):
    with open(bibtex_file_path) as bibtex_file:
        bibtex_database = bibtexparser.load(bibtex_file)

    return bibtex_database.entries_dict

def prepare_authors(bibtex_author):
    result_line = ''
    bibtex_names = bibtex_author.split(' and ')
    for bib_name in bibtex_names:
        if bib_name.find(',') >= 0:
            first_name, second_name = bib_name.split(',')
            short_second_name = ''.join([part[0]+'.' for part in second_name.split()])
            result_line += first_name + ' ' + short_second_name + ', '
        else:
            result_line += bib_name + ', '

    result_line = result_line[:-2] #Remove last comma

    result_line = result_line.replace(", others"," и др.")

    return result_line

def fill_pattern(entry):

#     pattern = """\\bibitem{%id}
# {%author}. %title 
# \\textit{%journal}. 
# \\newblock %year. 
# \\newblock V.~%vol, №~%num. 
# \\newblock P.~%pages."""

    item_id = entry['ID']
    author = entry.get('author','').encode('utf8')
    title = entry.get('title','').encode('utf8')
    journal = entry.get('journal','').encode('utf8')
    year = int(entry.get('year',0))
    volume = int(entry.get('volume',0))
    number = int(entry.get('number',0))
    pages = entry.get('pages','').encode('utf8')

    author = prepare_authors(author)

    result = '\\bibitem{%(item_id)s}\n{%(author)s} %(title)s.\n' % locals()
    if journal:
        result += '\\textit{%(journal)s}.\n' % locals()
    if year:
        result += '\\textit{%(year)d}.\n' % locals()
    if volume or number:
        result += '\\newblock '
        if volume:
            result += 'Т.~%(volume)d.' % locals()
        if volume and number:
            result += ' '
        if number:
            result += '№~%(number)d.' % locals()
        result += '\n'
    if pages:
        result += '\\newblock С.~%(pages)s.\n' % locals()

    return result


def main():
    parser = argparse.ArgumentParser(description='Generate bibliograpy by citations in tex file and bibtex file')
    parser.add_argument("tex_file", help="Input tex file")
    parser.add_argument("bibtex_file", help="Bibtex file")
    parser_args = parser.parse_args()

    tex_file = parser_args.tex_file
    bibtex_file = parser_args.bibtex_file

    if not os.path.exists(tex_file):
        parser.error('Input file do not exist')
    elif not os.path.isfile(tex_file):
        parser.error('Not a file')
    elif tex_file.split('.')[-1] != 'tex':
        parser.error('Wrong tex file type: '+ tex_file.split('.')[-1])

    if not os.path.exists(bibtex_file):
        parser.error('Bibtex file do not exist')
    elif not os.path.isfile(bibtex_file):
        parser.error('Bibtex is not a file')
    elif bibtex_file.split('.')[-1] != 'bib':
        parser.error('Wrong bibtex file type: '+ bibtex_file.split('.')[-1])

    citations = get_citations(tex_file)

    bibtex_dict = load_bibtex(bibtex_file)

    for cite in citations:
        if cite in bibtex_dict:
            print fill_pattern(bibtex_dict[cite])
        else:
            sys.stderr.write('Missing BIBtex entry: %s\n' % cite)

if __name__ == '__main__':
    main()