#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys,os
import io,json,glob
import re
from collections import defaultdict
from itertools import groupby

# join all jsons in a single file 


partidos = ['PS','BE','PEV','PSD','PCP','PAN','CDS-PP','SI','NI','IND']

roman2arab = {'VIII':'8','IX':'9','X':'10','XI':'11','XII':'12','XIII':'13'}

def agregar(new_main):
    party_main = []
    for p,_,_,_ in new_main:
        if p == 'President':
            party_main.append('President')
        else:
            party_main.append('Other')


    posicoes = []
    count = 0
    for _,gen in groupby(party_main):
        temp = []
        count_2 = 0
        for x in gen:
            temp.append(count)
            count += 1
            count_2 += 1
        posicoes.append(temp)

    new_main2 = []
    for j,serie in enumerate(posicoes):
        ind_1 = serie[0]
        if new_main[ind_1][0] == u'President':
            textos = u'\n'.join([new_main[ind][3] for ind in serie])
            new_main2.append(('President','President','MESA',textos))
        else:
            for k in serie:
                new_main2.append(new_main[k])

    party_main = []
    for p,_,_,_ in new_main2:
        if p == 'President':
            party_main.append('President')
        else:
            party_main.append('Other')

    posicoes = []
    count = 0
    for _,gen in groupby(party_main):
        temp = []
        count_2 = 0
        for x in gen:
            temp.append(count)
            count+=1
            count_2 += 1
        if x == 'President' and count_2 > 1:
            print("aqui!")
            print(file_name)
        posicoes.append(temp)

    return posicoes,new_main2



files =  sorted(glob.glob('extract_json/*'))
print(len(files))


legislaturas = defaultdict(lambda:defaultdict(list))
for i,file_name in enumerate(files):

    main = []
    with io.open(file_name,'r',encoding = 'utf8') as f_in:
        for j,line in enumerate(f_in):
            if j == 0:
                date = line.strip(u'\n')
                continue
            try:
                main.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                print(j,file_name)
                sys.exit()

    # remove apartes
    new_main = []
    for i,block in enumerate(main):

        block_prev = main[i-1]

        party_prev = block_prev['party']

        party = block['party']
        name = block['name']
        tipo = block['tipo']
        text = block['text']

        # remove apartes

        if len(text.replace(u'\n',u' ').split()) <= 5 and text.endswith(u'!') and  party not in ['Orador','Count','President'] and party_prev != 'President':
            continue
        new_main.append((party,name,tipo,block['text']))

    # agregar Presidents
    posicoes,new_main = agregar(new_main)


    # transformar Cont dos Presidente em Presidente e colar
    for j,serie in enumerate(posicoes):
        if j == 0:
            ind_1 = serie[0]
            if new_main[ind_1][0] != u'President':
                print("Erro! Primeiro não é o Presidente")
                print(file_name)
                sys.exit()
                continue
        if j == len(posicoes)-1:
            ind_1 = serie[0]
            if new_main[ind_1][0] != u'President':
                print("Erro! Último não é o Presidente")
                print(file_name)
                sys.exit()
                continue

        ind_1 = serie[0]
        temp = []
        if new_main[ind_1][0] == 'Cont':
            for k in serie:
                if new_main[k][0] != 'Cont':
                    break
                temp.append(k)
        if temp:

            for k in temp:
                texto = new_main[k][3]
                new_main[k] = ('President','President','MESA',texto)

    posicoes,new_main = agregar(new_main)

    # identificar os blocos
    # nesta fase identificar os blocos a partir da primeira ocurrência
    ident = []
    for j,serie in enumerate(posicoes):
        ind_1 = serie[0]
        party = new_main[ind_1][0]
        name = new_main[ind_1][1]
        tipo = new_main[ind_1][2]
        if party == 'Orador':
            ident.append(('Orador','Orador','Orador'))
        else:
            ident.append((party,name,tipo))

    # identificar os blocos de Orador. Se Orador a identidade é igual à anterior
    for j,_ in enumerate(posicoes):
        if ident[j][0] == 'Orador':
            temp = 'President'
            k = 0
            while temp == 'President':
                k+=1
                anterior = ident[j-k][0]
                temp = anterior
            ident[j] = ident[j-k]

    # print [(x,ident[j][0]) for j,x in enumerate(posicoes)]
    # print new_main[8]

    # transformar Cont e Oradores
    main_final = []
    for j,serie in enumerate(posicoes):
        if j == 0:
            ind_1 = serie[0]
            if new_main[ind_1][0] != u'President':
                print("Erro! Primeiro não é o Presidente")
                print(file_name)
                sys.exit()
                continue
        if j == len(posicoes)-1:
            ind_1 = serie[0]
            if new_main[ind_1][0] != u'President':
                print("Erro! Último não é o Presidente")
                print(file_name)
                sys.exit()
                continue

        # transformar os Orador na identidade do bloco
        party_ident = ident[j][0]
        name_ident = ident[j][1]
        tipo_ident = ident[j][2]
        texto_full = []


        for k in serie:
            if new_main[k][0] == party_ident and new_main[k][1] == name_ident and new_main[k][2] == tipo_ident:
                texto_full.append(new_main[k][3])
            elif new_main[k][0] == 'Orador' or new_main[k][0] == 'Cont':
                texto_full.append(new_main[k][3])
            else:
                continue
        block = (party_ident,name_ident,tipo_ident,u'\n'.join(texto_full))

        if party_ident == 'Orador' or party_ident == 'Cont':
            print("ERRO!")
        main_final.append(block)

    #  grava o texto corrido
    with io.open('final_txt/'+os.path.basename(file_name)+'.final.txt','w',encoding = 'utf8') as f_out:
        for block in main_final:
            f_out.write(block[1]+u' | '+block[0]+u'\n')
            f_out.write(block[3])
            f_out.write(u'\n')
            f_out.write(u"\n")


    final_json = []
    for k,block in enumerate(main_final):

        temp = {}
        temp['party'] = block[0]
        temp['name'] = block[1]
        temp['type'] = block[2]
        texto = block[3]
        texto = texto.replace(u'-\n',u'').replace(u'\n',u' ').strip(u'_').strip()
        temp['text'] = texto
        final_json.append(temp)

    #  grava em json todas as interveções, incluindo presidente e governo
    final_json.append({"session-date":date})
    with io.open('jsons/'+os.path.basename(file_name)+'.json','w', encoding='utf8') as f_out:
        data = json.dumps(final_json,ensure_ascii=False,indent=2,sort_keys=True)
        f_out.write(data)

    MP_jsons = []
    for block in final_json:
        try:
            if block['type'] == 'MP' or block['type'] == 'GOV':
                MP_jsons.append(block)
        except KeyError:
            continue
        # try:
        #     if block['type'] == 'GOV' or block['type'] == 'MESA' or block['type'] == 'EXT':
        #         continue
        # except KeyError:
        #     continue


    temp = [block['name'] for block in MP_jsons]
    posicoes = []
    count = 0
    for _,gen in groupby(temp):
        temp = []
        count_2 = 0
        for x in gen:
            temp.append(count)
            count += 1
            count_2 += 1
        posicoes.append(temp)

    final_MP = []
    for serie in posicoes:
        texto = []
        for k in serie:
            texto.append(MP_jsons[k]['text'])
        temp = {}
        temp['party'] = MP_jsons[serie[0]]['party']
        temp['name'] = MP_jsons[serie[0]]['name']
        temp['type'] = MP_jsons[serie[0]]['type']
        temp['text'] = u' '.join(texto)
        final_MP.append(temp)
    final_MP.append({"session-date":date})

    #  grava em json todas as interveções de deputados

    with io.open('jsons_joined/'+os.path.basename(file_name)+'.json','w', encoding='utf8') as f_out:
        data = json.dumps(final_MP,ensure_ascii=False,indent=2,sort_keys=True)
        f_out.write(data)

    for leg in ['VIII','IX','X','XI','XII','XIII']:
        if leg in file_name:
            for block in final_MP:
                try:
                    if block['type'] == 'MP':
                        legislaturas[roman2arab[leg]][block['party']].append((date,block['text']))
                except KeyError:
                    continue
#  grava em json as intervenções por partido e legislatura

for leg in ['13']:
    print([len(legislaturas[leg][x]) for x in legislaturas[leg].keys()])
    with io.open('legislaturas/dar_'+leg+'_partidos_only.json','w', encoding='utf8') as f_out:
        data = json.dumps(legislaturas[leg],ensure_ascii=False,indent=2,sort_keys=True)
        f_out.write(data)
