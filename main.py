# Projeto desenvolvido para plataforma windows. Compatível apenas com GMAIL.

import os
from random import choice
from datetime import datetime
from zipfile import ZipFile
from string import digits
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main() -> None:
    __path: str = f'{os.environ["USERPROFILE"]}\\Downloads\\arqs\\'
    gerar_pasta(__path)
    limpar_diretorios(__path)
    gerar_arquivos(__path)
    renomear_arquivos(__path)
    compactar(__path)
    send_mail(__path)


def gerar_pasta(l_path: str):
    try:
        os.makedirs(l_path)
    except FileExistsError:
        pass


def limpar_diretorio(l_path):
    for arquivo in get_flist(l_path):
        os.remove(l_path + arquivo)


def limpar_diretorios(l_path):
    diretorio = os.listdir(l_path)
    i_path: str
    for item in diretorio:
        i_path = os.path.join(l_path, item)
        if os.path.isfile(i_path):
            os.remove(i_path)
        if os.path.isdir(i_path):
            limpar_diretorios(i_path)
            os.rmdir(i_path)


def get_flist(l_path):
    return [arquivo for arquivo in os.listdir(l_path) if os.path.isfile(l_path+arquivo)]


def gerar_arquivos(l_path):
    limpar_diretorio(l_path)
    hexdigits: str = digits + 'ABCDEF'
    for i in range(100):
        nome: str = f'{l_path}' + ''.join(([choice(hexdigits) for i in range(8)]))
        conteudo: str = ''.join(([choice(hexdigits) for i in range(4096)]))

        with open(f'{nome}.txt', 'w') as arq:
            arq.write(conteudo)


def renomear_arquivos(l_path):
    arquivos = get_flist(l_path)
    for arquivo in arquivos:
        os.rename(f'{l_path}{arquivo}', f'{l_path}{str(arquivos.index(arquivo)).zfill(3)}_{arquivo}')


def date_path(l_path) -> str:
    date = str(datetime.now()).split('.')
    date.pop(-1)
    date = date[0].split()
    date[1] = date[1].split(':')
    date[1].pop(-1)
    date[0] = date[0].split('-')
    for vect in date:
        for val in vect:
            l_path = os.path.join(l_path, val)
    gerar_pasta(l_path)
    return l_path


def compactar(l_path):
    diretorio = get_flist(l_path)
    for i in range(10):
        nome = os.path.join(date_path(l_path), f'arquivos{i}.zip')
        with ZipFile(nome, 'w') as arqzip:
            for j in range(10):
                arquivo = diretorio.pop(0)
                with open(f'{l_path}{arquivo}') as dados:
                    arqzip.writestr(arquivo, dados.read())
    limpar_diretorio(l_path)


def send_mail(l_path):

    usuario: str = input('Digite o endereço de envio do e-mail:\n')
    senha: str = input('Digite a senha do e-mail:\n')
    destinatario: str = input('Digite o e-mail do destinatário:\n')

    msg: MIMEMultipart = scan_dir(l_path)
    msg['to'] = destinatario
    msg['from'] = usuario
    msg['subject'] = 'Arquivos'

    servidor = SMTP_SSL('smtp.gmail.com', 465)
    servidor.login(usuario, senha)
    servidor.sendmail(msg['from'], msg['to'], msg.as_string())
    servidor.quit()


def scan_dir(l_path) -> MIMEMultipart:
    msg = MIMEMultipart()
    diretorio = os.listdir(l_path)
    i_path: str
    for item in diretorio:
        i_path = os.path.join(l_path, item)
        if os.path.isfile(i_path):
            anexo = MIMEText(open(i_path, 'rb').read(), 'base64', 'gb2312')
            anexo["Content-Type"] = 'application / octet-stream'
            anexo["Content-Disposition"] = f'attachment; filename = {item}'
            msg.attach(anexo)
        if os.path.isdir(i_path):
            msg.attach(scan_dir(i_path))
    return msg


if __name__ == '__main__':
    main()
