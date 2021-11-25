import sys
from bs4 import BeautifulSoup
from collections import Counter
import codecs,re


# convert the xml to txt (one column scenario)

def bbox_coords(value):
    # these might be in the wrong order, but it's indeed xyxy order
    left, bottom, right, top = [float(x) for x in value.split(',')]
    return (left, bottom, right, top)

def has_vertical_line(page):
    # vertical lines are actually rects
    rects = page.findAll('rect')
    for rect in rects:
        x0, y0, x1, y1 = bbox_coords(rect.get('bbox'))
        if x1 - x0 < 3:
            return True
    return False


# def extract_xy(coord):
#     temp = [float(i) for i in coord.split(',')]
#     return (temp[3],-temp[2])


def extract_xy(coord):
    x1,y1,x2,y2  = [float(i) for i in coord.split(',')]
    return y1+(y2-y1)/2.

import time
start_time = time.time()

xml = open(sys.argv[1], 'r')
# soup = BeautifulSoup.BeautifulStoneSoup(xml)
soup = BeautifulSoup(xml, 'xml')

pagestag = soup.findAll('pages')
assert len(pagestag) == 1
pages = pagestag[0].findAll('page')
# we'll store the output here


### check bold mediana
fontes_size = []
for page in pages:
    textboxes = page.findAll('textbox')
    for textbox in textboxes:
        textlines = []
        for textline in textbox.findAll('textline'):
            line = ''
            left_pos = bbox_coords(textline.get('bbox'))[0]
            textbits = textline.findAll('text')
            for textbit in textbits:
                if not textbit.text:
                    continue
                if not textbit.get('font'):
                    continue
                if 'Bold' in textbit['font']:
                    fontes_size.append(textbit.get('size'))



font_max = sorted(Counter(fontes_size).items(),key = lambda x:x[1],reverse = True)[:2]
font_max = float(font_max[-1][0])

txt = ''
for pp,page in enumerate(pages):

    textboxes = page.findAll('textbox')
    col_left = []
    for i,textbox in enumerate(textboxes):
        col_left.append((i,textbox))


    col_left = sorted(col_left,key= lambda x:(extract_xy(x[1].get('bbox')),-[float(p) for p in x[1].get('bbox').split(',')][0],-x[0]),reverse = True)

    for i,(_,textbox) in enumerate(col_left):
        # txt += '\n'
        # we'll store tuples for storing the text and position, since sometimes PDFminer
        # gets the word order wrong -- FIXME NOT WORKING
        textlines = []
        for textline in textbox.findAll('textline'):
            line = ''
            textbits = textline.findAll('text')
            for textbit in textbits:
                if not textbit.text:
                    # check for non-breaking spaces since they happen,
                    # for this we check for the font attribute
                    if not textbit.get('font'):
                        continue
                    # avoid double spaces, only output if last char wasn't a space
                    if line and not line[-1] == ' ':
                        line += ' '
                # also, most useless metadata is at specific small sizes, let's weed that out too
                # isto ajuda pra remover os sumários!
                # elif 'Bold' not in textbit['font'] and float(textbit.get('size')) <= 10.613:
                #     continue
                # elif 'Bold' in textbit['font'] and float(textbit.get('size')) < font_max:
                #     continue
                else:
                    if not textbit.get('font'):
                        continue
                    # add the text to the line string, and mark it up if necessary
                    if 'Italic' in textbit['font']:
                        # remove last emphasis marker, watching for spaces
                        if line.endswith('_ '):
                            line = line[:-2] + ' ' + textbit.text + '_'
                        elif line.endswith('_'):
                            line = line[:-1] + textbit.text + '_'
                        else:
                            line += '_' + textbit.text + '_'
                    elif 'Bold' in textbit['font']:
                        # remove last strong marker, watching for spaces
                        if line.endswith('* '):
                            line = line[:-2] + ' ' + textbit.text + '*'
                        elif line.endswith('*'):
                            line = line[:-1] + textbit.text + '*'
                        else:
                            line += '*' + textbit.text + '*'
                    else:
                        line += textbit.text

            textlines.append(line)

        for j,line in enumerate(textlines):
            line = line.strip()
            temp = line.lower()
            if re.match(r'^\*(\d+) de (\w+) de (\d+)\s*\*$',temp):
                txt += '\n'
                continue
            if re.match(r'^\*(\d+)\s*\*$',temp):
                txt += '\n'
                continue
            if line.isdigit() or line.strip('*').isdigit():
                txt += '\n'
                continue
            if re.match(r'i série (.*) (\d+)$',line.replace('*','').lower().strip()) and len(line.split()) <= 6:
                txt += '\n'
                continue
            if '________________________________________________________' in line:
                txt += '\n'
                continue

            txt += line + '\n'
        # txt += '\n'



import codecs
outfile = codecs.open(sys.argv[2], 'w', 'utf-8')
outfile.write(txt)
outfile.close()
