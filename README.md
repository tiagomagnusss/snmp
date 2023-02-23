# snmp
Ferramenta gráfica para gerenciamento de contabilização de redes.

### Dependências
Bibliotecas necessárias para o funcionamento do programa:
* python3 >= 3.10
* libsnmp-dev
* snmp-mibs-downloader


### Instalação
Para instalar as dependências, execute o seguinte comando:
```
sudo apt install python3 libsnmp-dev snmp-mibs-downloader
```jhnu

Caso ainda não possua as dependências do Python instaladas, execute o seguinte comando:
```
pip3 install -r requirements.txt
```

### Execução
Para executar o programa, execute o seguinte comando:
```
python3 main.py
```

### Compilação
O programa pode ser compilado em um arquivo executável com o seguinte comando:
```
python setup.py build
```

