import io,sys,os,glob

# download pdfs from the urls file (that contains each DAR link)
# example: http://app.parlamento.pt/darpages/dardoc.aspx?doc=6148523063446f764c324679626d56304c334e706447567a4c31684a53556c4d5a576376524546535353394551564a4a51584a7864576c326279387a4c734b714a5449775532567a63384f6a627955794d45786c5a326c7a6247463061585a684c3052425569314a4c5445774f4335775a47593d&nome=DAR-I-108.pdf

with io.open("URLs.csv",'r') as f:
    for line in f:
        line = line.strip('\n')
        nome = line.split('&nome=')[1]
        nome = nome.split('-')[2]
        comando = 'curl \"'+line+'\" > pdfs/'+nome
        print(comando)
        os.system(comando)
        # break
