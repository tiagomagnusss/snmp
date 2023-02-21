import tkinter as tk
from tkinter import messagebox
import easysnmp

def coletar_dados(endereco_ip, usuario_snmp):
    # Realizar consulta SNMP para obter informações de contabilização
    try:
        session = easysnmp.Session(hostname=endereco_ip, security_level="auth_with_privacy", security_username=usuario_snmp, privacy_password='des1234567', auth_protocol='MD5', auth_password='md51234567', privacy_protocol='DES', version=3)
        contabilizacao = session.get('sysUpTime.0')
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao obter dados de contabilização de {endereco_ip} para o usuário {usuario_snmp}: {str(e)}")
        return contabilizacao

    return contabilizacao

def analisar_dados(endereco_ip, usuario_snmp):
    dados = coletar_dados(endereco_ip, usuario_snmp['nome'])
    if int(dados.value) > 10000000:
        messagebox.showwarning("Alerta", f"Foi detectado um evento anômalo na contabilização de {endereco_ip} para o usuário {usuario_snmp['nome']}")
    else:
        messagebox.showinfo("Informação", f"Não foram encontrados eventos anômalos na contabilização de {endereco_ip} para o usuário {usuario_snmp['nome']}")



def verificar_eventos():
    # Lista de endereços IP ou nomes de host dos dispositivos a serem verificados
    dispositivos = ['localhost']

    for dispositivo in dispositivos:
        for usuario_snmp in usuarios_snmp:
            analisar_dados(dispositivo, usuario_snmp)


if __name__ == '__main__':
    
    usuarios_snmp = [
        {'nome': 'MD5DESUser', 'auth_protocol': 'MD5', 'auth_password': 'md51234567', 'privacy_protocol': 'DES', 'privacy_password': 'des1234567'},
    ]

    # Criar interface gráfica com tkinter
    root = tk.Tk()
    root.title("Ferramenta de Contabilização")

    # Adicionar botão para verificar eventos anômalos
    verificar_button = tk.Button(root, text="Verificar Eventos Anômalos", command=verificar_eventos)
    verificar_button.pack()

    # Iniciar o loop principal da interface gráfica
    root.mainloop()
