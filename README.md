# Catálogo de Produtos de Informática

## Definição do projeto

Este é um projeto de um catálogo de produtos de informática desenvolvido com fins didáticos para ilustrar o funcionamento de uma aplicação web baseada em **Python** e **Flask**.

### Objetivo

Mostrar ao usuário externo um catálogo de produtos cadastrados.

### Funcionalidades planejadas

1. O usuário externo pode visualizar os produtos por categoria (processadores, memórias, HDs, SSDs, placas-mãe, fontes de alimentação, monitores, mouses, teclados);
2. O usuário externo pode filtrar os produtos de mesma categoria pelas características mais importantes;
3. O usuário externo pode ordenar os produtos por nome (A-Z e Z-A) e preço (menor-maior e maior-menor);
4. Apenas o usuário interno (requer login) tem as opções de editar e remover o produto (na página do próprio produto) e inserir novos produtos.

## Como usar este repositório

1. Crie em seu computador uma pasta para o repositório;
2. Clone este repositório dentro da pasta criada: 
```
git clone https://github.com/LCavalini/Catalogo.git
```
3. Crie um ambiente virtual dentro da pasta:
```
virtualenv venv
```
4. Ative o ambiente virtual:
```
venv\Scripts\activate
```
5. Instale as dependências com o ambiente virtual ativado (deve mostrar (venv) na linha de comando):
```
pip install -r requirements.txt
```
6. Execute o servidor:
```
flask run
```