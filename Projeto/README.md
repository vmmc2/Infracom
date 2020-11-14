## Pasta que contém o projeto de Infracom

* O projeto consiste em fazer um chat para uma rede local usando o protocolo TCP

## Dependências
* ansicolors: Deve ser instalado por meio do comando "pip install ansicolors" (https://pypi.org/project/ansicolors/)
* Windows Terminal: Deve ser utilizado para rodar os scripts, pois não é possível visualzar as mensagens em cores diferentes caso seja usado o cmd do Windows.

## Execução
* Primeiramente, entre na pasta do projeto.
* Abra 1 janela do Windows Terminal na qual o servidor será executado e abra quantas outras desejar para que os clientes sejam executadas.
* Em seguida, comece ligando o servidor por meio do seguinte comando no Windows Terminal:
```powershell
python server.py
```
* Feito isso, ligue quantos clientes desejar por meio do seguinte comando:
```powershell
python client.py
```
