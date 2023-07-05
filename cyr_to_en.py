#!/usr/bin/python3

import iuliia
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--input', '-i', type=argparse.FileType('r'), required=True,
    metavar='PATH',
    help="Input file (default: standard input).")
parser.add_argument(
    '--output', '-o', type=argparse.FileType('w'), required=True,
    metavar='PATH',
    help="Output file (default: standard output)")
parser.add_argument(
    '--schema', '-s', default='mosmetro',
    help="Transliteration schema (default: mosmetro). Possible options: ala_lc, ala_lc_alt, bgn_pcgn, bgn_pcgn_alt, bs_2979, bs_2979_alt, gost_16876, gost_16876_alt, gost_52290, gost_52535, gost_7034, gost_779, gost_779_alt, icao_doc_9303, iso_9_1954, iso_9_1968, iso_9_1968_alt, mosmetro, mvd_310, mvd_310_fr, mvd_782, scientific, telegram, ungegn_1987, wikipedia, yandex_maps, yandex_money")

args = parser.parse_args()

schema = iuliia.Schemas.get(args.schema)


EN = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?!@#$%^&"""
RU = """ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,!"№;%:?"""

EN_RU = str.maketrans(EN, RU)
RU_EN = str.maketrans(RU, EN)
RU_CHARS = frozenset(RU[:33])

def is_RU(word):
    for char in word.lower():
        if char in RU_CHARS:
            return True
    return False

def translate(text):
    text_ = text.rstrip(' ')
    if not text_:
        return

    trailing_spaces_num = len(text) - len(text_)
    iwords = iter(text_.split(' '))
    words = [''.join([' ', next(iwords)]) if not w else w for w in iwords]

    if not words:
        return

    result = [word.translate(RU_EN) for word in words if is_RU(word)]

    if trailing_spaces_num:
        result.append(' ' * trailing_spaces_num)

    return ' '.join(result)

with open(args.input.name) as input_file:
    with open(args.output.name, 'w') as out_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            out_file.write(iuliia.translate(line, schema) + '\n') # translit
            out_file.write(translate(line) + '\n') # layout
        out_file.truncate(out_file.tell()-1) # remove last newline