import io,sys,os,glob

# parse each pdf and convert to a xml file

files = sorted(glob.glob('pdfs/*.pdf'))
for file in files:
    f_name = os.path.basename(file)
    f_name = f_name.replace('pdfs/','')
    comando =  'pdf2txt.py -t xml -o xmls/'+f_name.replace('.pdf','.pdf.xml ')+file
    print(comando)
    os.system(comando)
