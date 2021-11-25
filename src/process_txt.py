#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import io,json,glob
import re
from datetime import datetime
import unicodedata
import argparse

#parse the txt generated from xml2txt


def correccoes_manuais(list_text,file_name):

    new_text_2 = []
    for line in list_text:
        if 'dar_serie_I_XIII_1_065' in file_name:
            if 'O Sr. *Ministro da Educação* - Insisto: cumprimos e cumpriremos os contratos, ainda que tenham sido' in line:
                line = line.replace('O Sr. *Ministro da Educação* - Insisto: cumprimos e cumpriremos os contratos, ainda que tenham sido','O Sr. *Ministro da Educação*: - Insisto cumprimos e cumpriremos os contratos, ainda que tenham sido')

        if 'dar_serie_I_XII_1_035' in file_name:
            if 'O Sr. *Ministro da Economia e do Emprego* - Neste sentido, urge perguntar: como é que vamos sair' in line:
                line = line.replace('O Sr. *Ministro da Economia e do Emprego* - Neste sentido, urge perguntar: como é que vamos sair','O Sr. *Ministro da Economia e do Emprego*: - Neste sentido, urge perguntar como é que vamos sair')

        if 'dar_serie_I_XII_1_130' in file_name:
            if "O Sr. *Secretário de Estado da Administração Interna* (Filipe Lobo d´Ávila): - Sr. Presidente, Sr." in line:
                line = line.replace("(Filipe Lobo d´Ávila)","(Filipe Lobo d'Ávila)")

        if 'dar_serie_I_XII_2_061' in file_name:
            if 'O Sr. *Ministro de Estado e dos Negócios Estrangeiros* - Sr. Presidente, Sr.as e Srs. Deputados:' in line:
                line = line.replace('O Sr. *Ministro de Estado e dos Negócios Estrangeiros* - Sr. Presidente, Sr.as e Srs. Deputados:','O Sr. *Ministro de Estado e dos Negócios Estrangeiros*: - Sr. Presidente, Sr.as e Srs. Deputados')

        if 'dar_serie_I_XII_2_076' in file_name:
            if 'O Sr. *Secretário de Estado da Administração Interna* - Sr. Presidente, Sr.as e Srs. Deputados:' in line:
                line = line.replace('O Sr. *Secretário de Estado da Administração Interna* - Sr. Presidente, Sr.as e Srs. Deputados:','O Sr. *Secretário de Estado da Administração Interna*: - Sr. Presidente, Sr.as e Srs. Deputados')

        if 'dar_serie_I_XII_3_050' in file_name:
            if 'O Sr. *Primeiro-Ministro*. - Segundo: Sr. Deputado, acrescento, para poderemos ter um termo de' in line:
                line = line.replace('O Sr. *Primeiro-Ministro*. - Segundo: Sr. Deputado, acrescento, para poderemos ter um termo de','O Sr. *Primeiro-Ministro*: - Segundo Sr. Deputado, acrescento, para poderemos ter um termo de')

        if 'dar_serie_I_XII_4_064' in file_name:
            if 'O Sr. *Ministro do Ambiente, Ordenamento do Território e Energia* - Sr. Presidente, Srs. Deputados:' in line:
                line = line.replace('O Sr. *Ministro do Ambiente, Ordenamento do Território e Energia* - Sr. Presidente, Srs. Deputados:','O Sr. *Ministro do Ambiente, Ordenamento do Território e Energia*: - Sr. Presidente, Srs. Deputados')

        if 'dar_serie_I_X_1_023' in file_name:
            if 'O Sr. *Ministro de Estado e da Administração Interna:-* Sr. Presidente, Sr. Deputado Luís Montenegro,' in line:
                line = line.replace('O Sr. *Ministro de Estado e da Administração Interna:-* Sr. Presidente, Sr. Deputado Luís Montenegro,','O Sr. *Ministro de Estado e da Administração Interna*: - Sr. Presidente, Sr. Deputado Luís Montenegro,')

        if 'dar_serie_I_X_1_049' in file_name:
            if 'O Sr. *Sr. Ministro da Saúde*: - Sr. Presidente, Sr. Deputada Helena Pinto, agradeço-lhe as suas' in line:
                line = line.replace('O Sr. *Sr. Ministro da Saúde*: - Sr. Presidente, Sr. Deputada Helena Pinto, agradeço-lhe as suas','O Sr. *Ministro da Saúde*: - Sr. Presidente, Sr. Deputada Helena Pinto, agradeço-lhe as suas')

        if 'dar_serie_I_X_2_031' in file_name:
            if 'O Sr. *Sr. Primeiro-Ministro*: - Já fez!' in line:
                line = line.replace('O Sr. *Sr. Primeiro-Ministro*: - Já fez!','O Sr. *Primeiro-Ministro*: - Já fez!')

        if 'dar_serie_I_X_2_081' in file_name:
            if 'O Sr. *Ministro da Ciência; Tecnologia e Ensino Superior*: - Sr. Presidente, Srs. Deputados, Sr.' in line:
                line = line.replace('O Sr. *Ministro da Ciência; Tecnologia e Ensino Superior*: - Sr. Presidente, Srs. Deputados, Sr.','O Sr. *Ministro da Ciência, Tecnologia e Ensino Superior*: - Sr. Presidente, Srs. Deputados, Sr.')

        if 'dar_serie_I_X_3_003' in file_name:
            if 'Vamos a outra questão, Sr. *Primeiro-Ministro*: a reforma da Administração Pública.' in line:
                line = line.replace('Vamos a outra questão, Sr. *Primeiro-Ministro*: a reforma da Administração Pública.','Vamos a outra questão, Sr. Primeiro-Ministro, a reforma da Administração Pública.')

        if 'dar_serie_I_X_3_014' in file_name:
            if 'O Sr. *Ministro de Estado e das Finança*s: - O Sr. Deputado sabe muito bem que estamos aqui a discutir' in line:
                line = line.replace('O Sr. *Ministro de Estado e das Finança*s: - O Sr. Deputado sabe muito bem que estamos aqui a discutir','O Sr. *Ministro de Estado e das Finanças*: - O Sr. Deputado sabe muito bem que estamos aqui a discutir')

        if 'dar_serie_I_X_3_019' in file_name:
            if 'O Sr*. Ministro dos Assuntos Parlamentares*: - E não pode ser mais de metade? O PCP não deixa, é?…' in line:
                line = line.replace('O Sr*. Ministro dos Assuntos Parlamentares*: - E não pode ser mais de metade? O PCP não deixa, é?…','O Sr. *Ministro dos Assuntos Parlamentares*: - E não pode ser mais de metade? O PCP não deixa, é?…')

        if 'dar_serie_I_X_4_016' in file_name:
            if 'Gostava de lhe dizer, como homem de direita, o seguinte, Sr. *Primeiro-Ministro*: quanto ao salário mínimo' in line:
                line = line.replace('Gostava de lhe dizer, como homem de direita, o seguinte, Sr. *Primeiro-Ministro*: quanto ao salário mínimo','Gostava de lhe dizer, como homem de direita, o seguinte, Sr. Primeiro-Ministro, quanto ao salário mínimo')

        if 'dar_serie_I_X_4_016' in file_name:
            if 'subsídio de desemprego cresceram 440%. Prejudicados primeiros desta situação, Sr. *Primeiro-Ministro*: os' in line:
                line = line.replace('subsídio de desemprego cresceram 440%. Prejudicados primeiros desta situação, Sr. *Primeiro-Ministro*: os','subsídio de desemprego cresceram 440%. Prejudicados primeiros desta situação, Sr. Primeiro-Ministro, os')

        if 'dar_serie_I_X_4_094' in file_name:
            if 'A Sr. *Maria Ofélia Moleiro* (PSD: - Eu tentei ler, mas, Sr. Ministro, esta é mais uma edição de uma' in line:
                line = line.replace('A Sr. *Maria Ofélia Moleiro* (PSD: - Eu tentei ler, mas, Sr. Ministro, esta é mais uma edição de uma','A Sr. *Maria Ofélia Moleiro* (PSD): - Eu tentei ler, mas, Sr. Ministro, esta é mais uma edição de uma')

        if 'dar_serie_I_VII_3_069' in file_name:
            if 'O Sr. *Presidente* (*Mota Amaral)*:' in line:
                line = line.replace('O Sr. *Presidente* (*Mota Amaral)*:','O Sr. *Presidente* (Mota Amaral):')

        if 'dar_serie_I_VII_4_011' in file_name:
            if 'O Sr. *Presidente* (João Amaral)*:*' in line:
                line = line.replace('O Sr. *Presidente* (João Amaral)*:*','O Sr. *Presidente* (João Amaral):')

        if 'dar_serie_I_VII_4_078' in file_name:
            if 'O Sr. *Ministro Adjunto do Sr. Primeiro-Ministro*' in line:
                line = line.replace('O Sr. *Ministro Adjunto do Sr. Primeiro-Ministro*','O Sr. *Ministro Adjunto do Sr. Primeiro-Ministro* (José Sócrates): - Sr. Presidente, Srs. Deputados: Tenho o')
            if '(José Sócrates): - Sr. Presidente, Srs. Deputados: Tenho o' in line:
                continue

        if 'dar_serie_I_XII_3_088' in file_name:
            if 'O Sr. *Secretário de Estado do Ordenamento do Território e da Conservação da Natureza* (Miguel de' in line:
                line = line.replace('O Sr. *Secretário de Estado do Ordenamento do Território e da Conservação da Natureza* (Miguel de','O Sr. *Secretário de Estado do Ordenamento do Território e da Conservação da Natureza* (Miguel de Castro Neto): - ')
            if 'Castro Neto) - Sr. Presidente, caros Srs. Deputados:' in line:
                line = line.replace('Castro Neto) - Sr. Presidente, caros Srs. Deputados:','Sr. Presidente, caros Srs. Deputados:')

        if 'dar_serie_I_XI_1_067' in file_name:
            if ' -* … ' in line:
                line = line.replace(' -* … ','*: - … ')

        if 'dar_serie_I_XII_3_054' in file_name:
            if 'A Sr.* Presidente*:' in line:
                line = line.replace('A Sr.* Presidente*:','A Sr. *Presidente*:')

        if 'dar_serie_I_XII_2_008' in file_name:
            if 'A Sr.* Presidente*:' in line:
                line = line.replace('A Sr.* Presidente*:','A Sr. *Presidente*:')

        if 'dar_serie_I_VII_1_044' in file_name:
            if 'O Sr. *Presidente *: -' in line:
                line = line.replace('O Sr. *Presidente *: -','O Sr. *Presidente*: -')

        if 'dar_serie_I_VII_1_079' in file_name:
            if 'O Sr. *Presidente* (Mota Amaral)): - Tem a palavra,' in line:
                line = line.replace('O Sr. *Presidente* (Mota Amaral)): - Tem a palavra,','O Sr. *Presidente* (Mota Amaral): - Tem a palavra,')

        if 'dar_serie_I_XII_1_098' in file_name:
            if '(António Filipe),' in line:
                line = line.replace('(António Filipe),','(António Filipe):')

        if 'dar_serie_I_XII_3_100' in file_name:
            if '(António Filipe);' in line:
                line = line.replace('(António Filipe);','(António Filipe):')

        if 'dar_serie_I_VIII_2_020' in file_name:
            if '*Paulo Portas* (diz quando lhe convém):' in line:
                line = line.replace('*Paulo Portas* (diz quando lhe convém):','O Sr. *Paulo Portas* (CDS-PP):')


        new_text_2.append(line)
    return new_text_2


def common_erros(f_in):
        ## correct commong error with '*' and  '-' positions
        texto  = []
        for line in f_in:
            line = line.replace('\u2014','-')
            line = line.replace('\u2013','-')
            line = line.replace('’',"'")
            line = line.replace('´',"'")


            line = line.replace('ª','')
            line = line.replace('º','')
            line = line.replace(' Sr ',' Sr. ')
            line = line.replace('Sra.','Sr.')
            line = line.replace('Sr.a ','Sr. ')


            if line.count('*') == 2:
                line = line.replace(' (*','* (')
                if 'Presidente' in line:
                    line = line.replace('*Presidente:*','*Presidente*:')
                    line = line.replace('*Presidente: -*','*Presidente*: -')
                if 'Orador' in line:
                    line = line.replace('*Oradora:*','*Oradora*:')
                    line = line.replace('*Orador:*','*Orador*:')
                    line = line.replace('*Oradora: -*','*Oradora*: -')
                    line = line.replace('*Orador: -*','*Orador*: -')
                    line = line.replace('A *Orador*:','O *Orador*:')
                    line = line.replace('O *Oradora*:','O *Orador*:')



                line = line.replace(':* -','*: -')
                line = line.replace(':-*','*: -')
                line = line.replace('* -','*: -')

                line = line.replace('*: -*','*: -')
                line = line.replace(': -*','*: -')
                line = line.replace(':* -','*: -')
                line = line.replace('* : -','*: -')
                line = line.replace(':*\n','*:\n')
                line = line.replace(': - ...*','*: - ...')
                line = line.replace('O *Presidente*:','O Sr. *Presidente*:')
                line = line.replace('*O Sr. ','O Sr. *')
                line = line.replace('O *Sr. ','O Sr. *')
                line = line.replace('*A Sr. ','A Sr. *')
                line = line.replace('A *Sr. ','A Sr. *')
                line = line.replace('Sr. *Sr.','Sr. *')
                line = line.replace('O Sr, *','O Sr. *')


            # if 'O Sr. *Secretário de Estado dos Assuntos Parlamenta-*' in line:
            #     print "1 ",line

            # print line

            # if '*)*: -' in line:
            #     print "aqui",[line]
            line = line.replace('*)*: -','): -')
            line = line.replace(')*: -*','): —')
            line = line.replace('* (*PS)*','* (PS)')
            line = line.replace('* (*PCP)*','* (PCP)')

            line = line.replace('(PCP:','(PCP):')
            line = line.replace('(BE:','(BE):')
            line = line.replace('(PS:','(PS):')
            line = line.replace('(PSD:','(PSD):')
            line = line.replace('(CDS-PP:','(CDS-PP):')
            line = line.replace('(Os Verdes:','(Os Verdes):')


            line = line.replace('(B E)','(BE)')


            line = line.replace(' (*PCP*)*','* (PCP)')
            line = line.replace(' (*PSD*)*','* (PSD)')
            line = line.replace(' (*PSD)','* (PSD)')
            line = line.replace(' (*PCP)','* (PCP)')

            line = line.replace('* PCP):','* (PCP):')
            line = line.replace('* BE):','* (BE):')
            line = line.replace('* PS):','* (PS):')
            line = line.replace('* PSD):','* (PSD):')
            line = line.replace('* CDS-PP):','* (CDS-PP):')
            line = line.replace('* Os Verdes):','* (Os Verdes):')


            line = line.replace('*Presidente* (Narana Coissoró:','*Presidente* (Narana Coissoró):')

            line = line.replace('O Sr. *Pedro Mota Soares* (CDS-PP9:','O Sr. *Pedro Mota Soares* (CDS-PP):')
            line = line.replace('O Sr. *Presidente* (Guilherme Silva:','O Sr. *Presidente* (Guilherme Silva):')
            line = line.replace('O Sr. *Presidente* Guilherme Silva):','O Sr. *Presidente* (Guilherme Silva):')


            line = line.replace('*-*','-')

            texto.append(line)
        return texto


def correct_italics(texto):
    new_text = []
    for j,line in enumerate(texto):
        if j < 2:
            new_text.append(line)
            continue

        if line.startswith('_') and (line.endswith('_\n') or line.endswith('_.\n') or line.endswith('_,\n') or  line.endswith('_...\n') or line.endswith('_!\n') or line.endswith('_:\n')):
            line = line.replace('_.\n','._\n')
            line = line.replace('_,\n',',_\n')
            line = line.replace('_...\n','..._\n')
            line = line.replace('_!\n','!_\n')
            line = line.replace('_:\n',':_\n')

            if texto[j-1] != '\n':
                new_text.append('\n')

            new_text.append(line)
            new_text.append('\n')
        new_text.append(line)
    return     new_text

def correct_breaks(texto,file_name):
    new_text = []
    for j,line in enumerate(texto):
        if j < 2:
            new_text.append(line)
            continue

        # if '-* ' in line:
        #     print line
        # continue

        line_prev = new_text[-1]
        line_prev2 = new_text[-2]

        if line.startswith('_') and (line.endswith('_\n') or line.endswith('_.\n') or line.endswith('_,\n') or  line.endswith('_...\n') or line.endswith('_!\n') or line.endswith('_:\n')):
            line = line.replace('_.\n','._\n')
            line = line.replace('_,\n',',_\n')
            line = line.replace('_...\n','..._\n')
            line = line.replace('_!\n','!_\n')
            line = line.replace('_:\n',':_\n')

            if texto[j-1] != '\n':
                new_text.append('\n')
            new_text.append(line)
            try:
                if texto[j+1] != '\n':
                    new_text.append('\n')
            except IndexError:
                new_text.append('\n')
            continue

        # ... *...-*
        # *...*
        if re.match(r"[\w+\.*\s*]+\*[\w+\-*,*’*'\s*]+-*\*$",line_prev) and re.match(r"^\*[\w+\-*,*’*':*-*\s*]+\*",line):
            if line_prev.endswith('-*\n'):
                newline =  line_prev[:-3] + line[1:]
            else:
                newline =  line_prev[:-2] + ' ' +line[1:]
            new_text = new_text[:-1]
            new_text.append('\n')
            new_text.append(newline)
            continue


        if  re.match(r"[\w+\.*\s*]+\*[\w+\-*,*’*'\s*]+-*\*$",line_prev2) and re.match(r"^\*[\w+\-*,*’*':*-*\s*]+\*",line) and line_prev == '\n':
            if line_prev2.endswith('-*\n'):
                newline =  line_prev2[:-3] + line[1:]
            else:
                newline =  line_prev2[:-2] + ' ' +line[1:]
            new_text = new_text[:-2]
            new_text.append('\n')
            new_text.append(newline)
            continue


        # *...-*
        # *...*
        if  re.match(r"^\*[\w+\-*,*’*'\s*]+-*\*$",line_prev) and re.match(r"^\*[\w+\-*,*’*':*-*\s*]+\*",line):
            if line_prev.endswith('-*\n'):
                newline =  line_prev[:-3] + line[1:]
            else:
                newline =  line_prev[:-2] + ' ' +line[1:]
            new_text = new_text[:-1]
            new_text.append('\n')
            new_text.append(newline)
            continue


        if  re.match(r"^\*[\w+\-*,*’*'\s*]+-*\*$",line_prev2) and re.match(r"^\*[\w+\-*,*’*':*-*\s*]+\*",line) and line_prev == '\n':
            if line_prev2.endswith('-*\n'):
                newline =  line_prev2[:-3] + line[1:]
            else:
                newline =  line_prev2[:-2] + ' ' +line[1:]
            new_text = new_text[:-2]
            new_text.append('\n')
            new_text.append(newline)
            continue

        # ... *...*
        # (...):
        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'*\s*]+\*$",line_prev) and re.match(r"^\([\w+\-*,*’*'*\s*]+\):",line):
            newline =  line_prev[:-1] + ' ' + line
            new_text = new_text[:-1]
            new_text.append('\n')
            new_text.append(newline)
            continue

        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'*\s*]+\*$",line_prev2) and re.match(r"^\([\w+\-*,*’*'*\s*]+\):",line) and line_prev == '\n':
            newline =  line_prev2[:-1] + ' ' + line
            new_text = new_text[:-2]
            new_text.append('\n')
            new_text.append(newline)
            continue

        # ... *...* (...
        # ...):
        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'\s*]+\*\s*\([\w+\-*,*’*'\s*]+-*$",line_prev) and re.match(r"^[\w+\-*,*’*'\s*]+\):",line):
            if line_prev.endswith('-\n'):
                newline =  line_prev[:-2] + line
            else:
                newline =  line_prev[:-1] + ' ' +line
            new_text = new_text[:-1]
            new_text.append('\n')
            new_text.append(newline)
            continue

        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'\s*]+\*\s*\([\w+\-*,*’*'\s*]+-*$",line_prev2) and re.match(r"^[\w+\-*,*’*'\s*]+\):",line) and line_prev == '\n':
            if line_prev2.endswith('-\n'):
                newline =  line_prev2[:-2] + line
            else:
                newline =  line_prev2[:-1] + ' ' +line
            new_text = new_text[:-2]
            new_text.append('\n')
            new_text.append(newline)
            continue


        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'\s*]+\*:",line) and new_text[-1] != '\n':
            new_text.append('\n')

        if re.match(r"[\w+\.*\s*]*\*[\w+\-*,*’*'* \s]+\*\s*\([\w+\-*,*’*'*\.* \s]+\)\s*[:\.]*\s*-*",line) and line_prev != '\n':
            new_text.append('\n')


        new_text.append(line)

    return new_text



def add_n(list_text):
    new_text = []
    for line in list_text:
        if re.match(r"^[\w+\.*\s*]*\*[\w+\-*,*’*'* \s*]+\*\s*\([\w+\-*,*’*'*\.* \s]+\)\s*[:.]*\s*-*",line):
            new_text.append('\n')
            new_text.append(line)
            continue

        if re.match(r"^[\w+\.*\s*]*\*[\w+\-*,*’*'* \s*]+\*\s*[:.]\s*-*",line):
            new_text.append('\n')
            new_text.append(line)
            continue
        new_text.append(line)
    return new_text


def remove_n(lista):
        texto = []
        for j,line in enumerate(lista):
            if j == 0:
                texto.append(line)
                continue
            if not line.strip('\n').strip():
                continue
            if line.strip().strip('\n') and not lista[j-1].strip().strip('\n'):
                texto.append('\n')
            texto.append(line)
        return texto





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pre_f', help='file int')
    parser.add_argument('--out_f', help='file out')
    args = parser.parse_args()
    file_name = args.pre_f
    print(file_name)



    with io.open(file_name,'r',encoding = 'utf8') as f_in:


        texto = common_erros(f_in)
        for line in texto:
            match1 = re.match(r"^o sr. \*[\w+\-*,*’*'\s*]+\*\s+[\w+\-*,*’*'*\.* \s]+\):",line.lower())
            match2 = re.match(r"^a sr. \*[\w+\-*,*’*'\s*]+\*\s+[\w+\-*,*’*'*\.* \s]+\):",line.lower())
            if match1 or match2:
                match = [x for x in [match1,match2] if x][0]
                print(match.group())



        # separate before and after the second presidente speaks
        list_text_above    = []
        list_text = []
        count_president = 0
        for j,line in enumerate(texto):

            # contar apenas depois do presidentes ter falado duas vezes
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


        # correccoes_manuais
        list_text = correccoes_manuais(list_text,file_name)

        # correct italics
        new_text = correct_italics(list_text)

        # remove multiple \n
        new_text = remove_n(new_text)

        ####   join actor name when separated
        new_text = correct_breaks(new_text,file_name)

        ## additional corrections
        new_text_temp = []
        for line in new_text:
            if re.match(r"^O Sr. \*[\w+\-*,*’*'\s*]+\*\n$",line) or re.match(r"^A Sr. \*[\w+\-*,*’*'\s*]+\*\n$",line):
                line = line.replace('*\n','*: -\n')
                new_text_temp.append('\n')
                new_text_temp.append(line)
                continue
            if re.match(r"^O Sr. \*[\w+\-*,*’*'\s*]+\*\s-",line) or re.match(r"^A Sr. \*[\w+\-*,*’*'\s*]+\*\s-",line):
                line = line.replace('* -','*: -')
                new_text_temp.append('\n')
                new_text_temp.append(line)
                continue
            if re.match(r"^O Sr. \*[\w+\-*,*’*'\s*]+\*-",line) or re.match(r"^A Sr. \*[\w+\-*,*’*'\s*]+\*-",line):
                line = line.replace('*-','*: -')
                new_text_temp.append('\n')
                new_text_temp.append(line)
                continue

            match1 = re.match(r"^O Sr. \*[\w+\-*,*’*'* \s*]+\s\([\w+\-*,*’*'*\.* \s]+\)\*:",line)
            match2 = re.match(r"^A Sr. \*[\w+\-*,*’*'* \s*]+\s\([\w+\-*,*’*'*\.* \s]+\)\*:",line)
            if match1 or match2:
                match = [x for x in [match1,match2] if x][0]
                match = re.search(r"\([\w+\-*,*’*'*\.* \s]+\)",match.group()).group()
                line = line.replace(' '+match+'*','* '+match)
                new_text_temp.append('\n')
                new_text_temp.append(line)
                continue

            new_text_temp.append(line)
        new_text = new_text_temp

        new_text = correccoes_manuais(new_text,file_name)

        new_text = add_n(new_text)
        # remove multiple \n
        new_text = remove_n(new_text)

    texto = ''.join(list_text_above+new_text)
    file_out = args.out_f
    with io.open(file_out,'w',encoding = 'utf8') as f_out:
        f_out.write(texto)
