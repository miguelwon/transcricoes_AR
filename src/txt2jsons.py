#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys,os
import io,json,glob
import re
from datetime import datetime
from collections import Counter,defaultdict
import unicodedata

# convert the txts to json format

mes2month = {'janeiro':'01',
    'fevereiro':'02',
    'março':'03',
    'abril':'04',
    'maio':'05',
    'junho':'06',
    'julho':'07',
    'agosto':'08',
    'setembro':'09',
    'outubro':'10',
    'novembro':'11',
    'dezembro':'12'
    }


correct_party = {'SPD':'PSD',
    'PCO':'PCP',
    'CD-PP':'CDS-PP',
    'CSDS-PP':'CDS-PP',
    'OPS Verdes':'PEV',
    'CDS-PPP':'CDS-PP',
    'O Verdes':'PEV',
    'CDSPP':'CDS-PP',
    'OCP':'PCP',
    'CEDS-PP':'CDS-PP',
    'Os Verde':'PEV',
    'PCVP':'PCP',
    'PCDP':'PCP',
    'PDS':'PSD',
    'CDS-PS':'CDS-PP',
    'OPCP':'PCP',
    'CSD-PP':'CDS-PP',
    'PASD':'PSD',
    'PSDF':'PSD',
    'CDP-PP':'CDS-PP',
    'PC P':'PCP',
    'os Verdes':'PEV',
    'CDS-':'CDS-PP',
    'CDS':'CDS-PP',
    'PCPP':'PCP',
    'PCPO':'PCP',
    'PCPC':'PCP',
    'Os Verdes':'PEV',
    'CDD-PP':'CDS-PP',
    'CDS-P':'CDS-PP',
    'CDS-CDS-PP':'CDS-PP',
    'Os Vedes':'PEV',
    'PE':'SIP',
    'N. Insc':'NI',
    'PC':'SIP',
    'PD':'SIP',
    'PBE':'SIP',
    'CP':'SIP',
    'PPC':'SIP',
    'PPD':'SIP',
    'PCFP':'SIP',
    'PCD':'SIP',
    'PSP':'SIP',
    'PP':'SIP',
    'N insc':'NI',
    'CDS.-PP':'CDS-PP',
    'N. insc.':'NI',
    'Indep.':'IND',
    'OS Verdes':'PEV',
    'Os verdes':'PEV',
    'N Insc':'NI',
    'N insc.':'NI'}

def check_names(nome):

    if nome in ['Alterações orçamentais no âmbito do Quadro de Referência Estratégico Nacional 2007-2013',
        'Sociedades gestoras de participações sociais',
        'Prédios situados nas áreas de localização empresarial',
        'pe',
        'Combate à desertificação e recuperação do desenvolvimento nas áreas abrangidas pelo Programa para a Recuperação das Áreas e Sectores Deprimidos',
        'TOTAL 13 247',
        'Uma voz do PSD',
        'Alteração ao Capítulo XIV',
        'se no fim do _Diário_',
        'reiro',
        'Taxa YQ',
        'e sociedades de capital de risco',
        'Votos do PCP']:
        return False

    if 'imposto' in nome.lower():
        return False
    return True




files =  sorted(glob.glob('../xml2txt/txt/XIII/*'))
print(len(files))

# discard comissões permamnentes e sessões comemorativas
main_list = []
for i,file_name in enumerate(files):
    # if '_XIII_2_' in file_name and not '_VII_' in file_name:
    #     continue

    if '_VII_' in file_name:
        continue

    with io.open(file_name,'r',encoding = 'utf8') as f_in:
        linhas = f_in.readlines()

    list_text_above    = []
    list_text = []
    count_president = 0
    for j,line in enumerate(linhas):

        # contar apenas depois do presidentes ter falado uma vezes
        if count_president <1:
            line_l = line.lower()
            temp1 = re.match(r'^o sr. \*presidente\*:',line_l)
            temp2 = re.match(r'^a sr. \*presidente\*:',line_l)
            temp3 = re.match(r'^o sr. \*presidente\* \([\w+’* \s]+\):',line_l)
            temp4 = re.match(r'^a sr. \*presidente\* \([\w+’* \s]+\):',line_l)
            temp5 = re.match(r'^sr. \*presidente\*:',line_l)
            temp6 = re.match(r'^sr. \*presidente\* \([\w+’* \s]+\):',line_l)
            if temp1 or temp2 or temp3 or temp4 or temp5 or temp6:
                count_president += 1
                if count_president == 1:
                    list_text.append(line)
                    continue
            list_text_above.append(line)
            continue
        list_text.append(line)

    ok = 1
    for line in list_text_above:
        line = line.lower()
        if '*REUNIÃO PLENÁRIA'.lower() in line:
            ok = 0
            continue
    if ok:
        continue
    else:
        date = ''
        for line in list_text_above:
            line = line.strip('\n')
            line = line.lower()

            date_match = re.search(r'^\*reunião plenária de (\d+) de (\w+) de (\d+)\s*\*$',line)
            if date_match:
                date_match = date_match.groups()
                mes = mes2month[date_match[1]]
                date = date_match[0]+'-'+mes+'-'+date_match[2]
                main_list.append([list_text,date,file_name])
                break

        if not date:
            print("Error! Can't find date.")
            print(file_name)
            print("--")

print(len(main_list))


partidos_dict = defaultdict(int)
nomes_dict = defaultdict(int)

for i,(linhas,date,file_name) in enumerate(main_list):


    texto_original = ''.join(linhas)
    texto_original = [x for x in texto_original.split('\n\n') if x.strip('\n').strip()]

    count = 0
    new_text = []
    for j,textblock in enumerate(texto_original):
        textblock =  textblock.split('\n')
        line_1 = textblock[0].lower()

        if '*vozes' in line_1:
            continue
        if 'vozes' in line_1 and line_1.count(':') == 1 and line_1.count('-') and len(line_1.split()) <= 5:
            continue
        if line_1.startswith('ozes') or line_1.startswith('*ozes'):
            continue
        if '*uma voz do cds-pp*' in line_1 or '*uma voz do pcp*' in line_1 or '*uma voz do ps*' in line_1:
            continue

        if line_1.startswith('_') and line_1.endswith('_'):
            continue

        temp1 = re.match(r'^[\w+\.*\s*]*\*\s*presidente\s*\*\s*[:.]{1}',line_1)
        temp2 = re.match(r'^[\w+\.*\s*]*\*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*[:.]{1}',line_1)
        temp3 = re.match(r'^o sr. \*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*-',line_1)
        temp4 = re.match(r'^a sr. \*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*-',line_1)
        if temp1 or temp2 or temp3 or temp4:
            ultimo = count

        count += 1
        new_text.append(textblock)

    new_text2 = new_text[:ultimo+1]

    new_text = []
    for j,textblock in enumerate(new_text2):
        line_1 = textblock[0].lower()

        temp1 = re.match(r'^[\w+\.*\s*]*\*\s*presidente\s*\*\s*[:.]{1}',line_1)
        temp2 = re.match(r'^[\w+\.*\s*]*\*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*[:.]{1}',line_1)
        temp3 = re.match(r'^o sr. \*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*-',line_1)
        temp4 = re.match(r'^a sr. \*\s*presidente\s*\* \([\w+\.*\s*]+\)\s*-',line_1)
        if temp1 or temp2 or temp3 or temp4:
            temp_match = [t  for t in [temp1,temp2,temp3,temp4] if t][0]
            remove = len(temp_match.group())
            new_line = textblock[0][remove:].strip()
            if new_line.startswith('-'):
                new_line = new_line[1:].strip()
            temp_textblock = [new_line] + textblock[1:]

            new_text.append(('President','President','MESA',temp_textblock))
            continue


        match = re.match(r"^[\w+\.*\s*]*\*[\w+\-*,*'* \s*]+\*\s*\([\w+\-*,*'*\.* \s]+\)\s*[:.]*\s*-*",line_1)
        if match:
            to_remove = textblock[0][match.start():match.end()]
            new_line = textblock[0][match.end():].strip()
            entre_aste = re.search(r"\*[\w+\-*,*'* \s*]+\*",to_remove).group().strip()
            entre_paren= re.search(r"\([\w+\-*,*'*\.* \s]+\)",to_remove).group().strip()
            entre_aste = entre_aste[1:-1].strip()
            entre_paren = entre_paren[1:-1].strip()
            new_textblock = [new_line] + textblock[1:]

            if not entre_aste.strip():
                new_text.append(('Cont','Cont','Cont',textblock))
                continue

            if 'orador' in entre_aste.lower():
                new_text.append(('Orador','Orador','Orador',new_textblock))
                continue

            if entre_aste.lower() == 'secretário' or entre_aste.lower() == 'secretária' or entre_aste.lower() == 'secretario' or entre_aste.lower() == 'secretaria':
                new_text.append((entre_aste,entre_paren,'MESA',new_textblock))
            elif 'ministr' in entre_aste.lower() or 'secretári' in entre_aste.lower() or 'secretari' in entre_aste.lower():
                new_text.append((entre_aste,entre_paren,'GOV',new_textblock))
            elif 'presidente' in entre_aste.lower()  or 'Rei' in entre_aste:
                new_text.append((entre_aste,entre_paren,'EXT',new_textblock))

                # print file_name
                # print "1 ",entre_aste
                # print textblock[0]
                # print "---"


            elif entre_paren.lower() == 'secretário' or entre_paren.lower() == 'secretária' or entre_paren.lower() == 'secretario' or entre_paren.lower() == 'secretaria':
                new_text.append((entre_paren,entre_aste,'MESA',new_textblock))
            elif 'ministr' in entre_paren.lower() or 'secretári' in entre_paren.lower() or 'secretari' in entre_paren.lower():
                new_text.append((entre_paren,entre_aste,'GOV',new_textblock))
            elif 'presidente' in entre_paren.lower():
                new_text.append((entre_paren,entre_aste,'EXT',new_textblock))

            else:
                try:
                    entre_paren = correct_party[entre_paren]
                except KeyError:
                    pass


                nome = entre_aste.replace('*','')


                if check_names(nome):
                    if len(entre_paren) == 1 or entre_paren == 'em euros':
                        new_text.append(('Cont','Cont','Cont',textblock))
                        continue

                    if entre_paren == '1 João Tiago Silveira':
                        print(file_name)

                    new_text.append((entre_paren,nome,'MP',new_textblock))
                else:
                    new_text.append(('Orador','Orador','Orador',textblock))


            continue


        match = re.match(r"^[\w+\.*\s*]*\*[\w+\-*,*'* \s*]+\*\s*[:.]\s*-*",line_1)
        if match:
            to_remove = textblock[0][match.start():match.end()]
            new_line = textblock[0][match.end():].strip()
            entre_aste = re.search(r"\*[\w+\-*,*'* \s*]+\*",to_remove).group().strip()
            entre_aste = entre_aste[1:-1].strip()
            new_textblock = [new_line] + textblock[1:]


            if 'orador' in entre_aste.lower():
                new_text.append(('Orador','Orador','Orador',new_textblock))
                continue

            if entre_aste.lower() == 'secretário' or entre_aste.lower() == 'secretária' or entre_aste.lower() == 'secretario' or entre_aste.lower() == 'secretaria':
                new_text.append((entre_aste,entre_aste,'MESA',new_textblock))
            elif 'ministr' in entre_aste.lower() or 'secretári' in entre_aste.lower() or 'secretari' in entre_aste.lower():
                new_text.append((entre_aste,'SI','GOV',new_textblock))
            elif 'presidente' in entre_aste.lower():
                new_text.append((entre_aste,'SI','EXT',new_textblock))
            else:
                nome = entre_aste.replace('*','')

                if check_names(nome):


                    new_text.append(('SI',nome,'MP',new_textblock))
                else:
                    new_text.append(('Orador','Orador','Orador',textblock))

            continue

        match1 = re.match(r"^o sr\.\s*[\w+\-*,*'* \s*]+\s*\([\w+\-*,*'*\.* \s]+\)\s*:\s*-*",line_1)
        match2 = re.match(r"^a sr\.\s*[\w+\-*,*'* \s*]+\s*\([\w+\-*,*'*\.* \s]+\)\s*:\s*-*",line_1)
        if match1 or match2:
            match = [x for x in [match1,match2] if x][0]

            to_remove = textblock[0][match.start():match.end()]
            to_remove = to_remove[2:]
            new_line = textblock[0][match.end():].strip()
            entre_aste = re.search(r"^Sr\.\s*[\w+\-*,*'* \s*]+",to_remove).group().strip()
            entre_paren= re.search(r"\([\w+\-*,*'*\.* \s]+\)",to_remove).group().strip()
            entre_aste = entre_aste[3:].strip()
            entre_paren = entre_paren[1:-1].strip()
            new_textblock = [new_line] + textblock[1:]

            if 'orador' in entre_aste.lower():
                new_text.append(('Orador','Orador','Orador',new_textblock))
                continue

            if entre_aste.lower() == 'secretário' or entre_aste.lower() == 'secretária' or entre_aste.lower() == 'secretario' or entre_aste.lower() == 'secretaria':
                new_text.append((entre_aste,entre_paren,'MESA',new_textblock))
            elif 'ministr' in entre_aste.lower() or 'secretári' in entre_aste.lower() or 'secretari' in entre_aste.lower():
                new_text.append((entre_aste,entre_paren,'GOV',new_textblock))
            elif 'presidente' in entre_aste.lower()  or 'Rei' in entre_aste:
                new_text.append((entre_aste,entre_paren,'EXT',new_textblock))
            elif entre_paren.lower() == 'secretário' or entre_paren.lower() == 'secretária' or entre_paren.lower() == 'secretario' or entre_paren.lower() == 'secretaria':
                new_text.append((entre_paren,entre_aste,'MESA',new_textblock))
            elif 'ministr' in entre_paren.lower() or 'secretári' in entre_paren.lower() or 'secretari' in entre_paren.lower():
                new_text.append((entre_paren,entre_aste,'GOV',new_textblock))
            elif 'presidente' in entre_paren.lower():
                new_text.append((entre_paren,entre_aste,'EXT',new_textblock))
            else:
                try:
                    entre_paren = correct_party[entre_paren]
                except KeyError:
                    pass

                nome = entre_aste.replace('*','')

                if check_names(nome):
                    if len(entre_paren) == 1 or entre_paren == 'em euros':
                        new_text.append(('Orador','Orador','Orador',textblock))
                        continue

                    if entre_paren == 'como, de resto, a Sr. Deputada Catarina Martins':
                        print("1 ",file_name)
                    new_text.append((entre_paren,nome,'MP',new_textblock))
                else:
                    new_text.append(('Orador','Orador','Orador',textblock))

            continue


        match1 = re.match(r"^o sr\.\s*[\w+\-*,*'* \s*]+\s*:\s*-*",line_1)
        match2 = re.match(r"^a sr\.\s*[\w+\-*,*'* \s*]+\s*:\s*-*",line_1)
        if match1 or match2:
            match = [x for x in [match1,match2] if x][0]
            to_remove = textblock[0][match.start():match.end()]
            to_remove = to_remove[2:]
            new_line = textblock[0][match.end():].strip()
            entre_aste = re.search(r"^Sr\.\s*[\w+\-*,*'* \s*]+",to_remove).group().strip()
            entre_aste = entre_aste[3:].strip()
            new_textblock = [new_line] + textblock[1:]

            if 'orador' in entre_aste.lower():
                new_text.append(('Orador','Orador','Orador',new_textblock))
                continue

            if entre_aste.lower() == 'secretário' or entre_aste.lower() == 'secretária' or entre_aste.lower() == 'secretario' or entre_aste.lower() == 'secretaria':
                new_text.append((entre_aste,entre_aste,'MESA',new_textblock))
            elif 'ministr' in entre_aste.lower() or 'secretári' in entre_aste.lower() or 'secretari' in entre_aste.lower():
                new_text.append((entre_aste,'SI','GOV',new_textblock))
            elif 'presidente' in entre_aste.lower():
                new_text.append((entre_aste,'SI','EXT',new_textblock))
            else:
                nome = entre_aste.replace('*','')

                if check_names(nome):
                    new_text.append(('SI',nome,'MP',new_textblock))
                else:
                    new_text.append(('Orador','Orador','Orador',textblock))

            continue



        # restante
        new_text.append(('Cont','Cont','Cont',textblock))


    new_text2 = []
    temp_dict = {}
    for p,n,_,_ in new_text:
        if p != 'SI' and p != 'SIP':
            temp_dict[n] = p
    for p,n,t,s in new_text:
        if p != 'SI' and p != 'SIP':
            new_text2.append((p,n,t,s))
        else:
            try:
                new_text2.append((temp_dict[n],n,t,s))
            except KeyError:
                new_text2.append(('SI',n,t,s))

    # os.system('rm extract_json/'+os.path.basename(file_name)+'.clean_step2.json')
    with io.open('extract_json/'+os.path.basename(file_name)+'.clean_step2.json','a') as f_temp:

        for k,x in  enumerate(new_text2):
            if k == 0:
                f_temp.write(date)
                f_temp.write('\n')
            party = x[0]

            if party == 'ALRAA':
                print(os.path.basename(file_name))
            # if party == 'SI':
            #     print(os.path.basename(file_name))


            name = x[1]
            tipo = x[2]
            text = '\n'.join(x[3])
            temp_dict = {}
            temp_dict['party'] = party
            temp_dict['name'] = name
            temp_dict['tipo'] = tipo
            temp_dict['text'] = text
            f_temp.write(json.dumps(temp_dict,ensure_ascii =False))
            f_temp.write('\n')
            # f_temp.write(name+' ('+party+'): - '+text)
            # f_temp.write('\n\n')


    for x in new_text2:
        if x[2] == 'MP':
            party = x[0]
            name = x[1]
            partidos_dict[party] += 1
            nomes_dict[name] += 1

for x,n in partidos_dict.items():
    print(n,x)
print(partidos_dict)
