import requests
from bs4 import BeautifulSoup
import zipfile
import os
import time

def zipPasta(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def main():
    anexo1 = "Anexo I - Lista completa de procedimentos (.pdf)"
    anexo2 = "Anexo I - Lista completa de procedimentos (.xlsx)"
    anexo3 = "Anexo II - Diretrizes de utilização (.pdf)"
    anexo4 = "Anexo III - Diretrizes clínicas (.pdf)"
    anexo5 = "Anexo IV - Protocolo de utilização (.pdf)"

    site = requests.get("https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude")
    htmlDoSite = BeautifulSoup(site.content, 'html.parser')

    exemplo = htmlDoSite.findAll("a",{"class": "internal-link"})
    listaLinks = []
    for element in exemplo:
        if((anexo1) in element.text or anexo2 in element.text or anexo3 in element.text or anexo4 in element.text or anexo5 in element.text ):
            linkPDF = element.get("href")
            listaLinks.append(linkPDF)
        
            
    for index, link in enumerate(listaLinks):
        extensaoArquivo = link.split(".")[-1]
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
        requestPdf = requests.get(link, headers=headers)

        with open('Teste-1/pdfs_salvos/anexo'+str(index)+'.'+extensaoArquivo, 'wb') as f:
            f.write(requestPdf.content)
    

    criarZip = zipfile.ZipFile( 'Teste-1/Teste_Intuitive_Care'+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zipPasta('Teste-1/pdfs_salvos/',criarZip)
    criarZip.close()    

if __name__ == '__main__':
    try:
        os.makedirs("Teste-1/pdfs_salvos")
    except:
        print("O diretorio ja existe")


    intervalo = 10
    setWebscrappingTimes = 0
    while setWebscrappingTimes <= 5:
        main()
        time.sleep(intervalo*1)
        print("Executando novamente")
        setWebscrappingTimes =+ 1
    
