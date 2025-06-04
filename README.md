# Perfilador

Reconstrução de identidades brasileiras a partir de dados públicos.


## Sobre

Este repositório contém os experimentos e implementações desenvolvidos para o Projeto Final intitulado:

**"Uma Abordagem para Elaboração de Identidades de Brasileiros baseada em Dados Públicos"**  
João Gabriel Hartmann – Curso Superior de Tecnologia em Segurança da Informação – UNISINOS  
Orientador: Dr. Luciano Ignaczak

O projeto investiga como dados pessoais expostos em fontes públicas (registros governamentais, redes sociais, etc.) 
podem ser processados e estruturados para reconstrução de identidades, utilizando técnicas como **OSINT** e 
**Processamento de Linguagem Natural (PLN)**.


## Objetivos

- Utilizar Open Source Intelligence (OSINT) e Extração de Informações (Information Extraction - IE) para identificação 
de pessoas a partir de dados públicos.
- Demonstrar como entidades nomeadas e relações podem ser extraídas automaticamente com **NER** e **Relation Extraction**.
- Avaliar a capacidade de um sistema automatizado de reconstruir perfis reais com alta precisão.
- Conscientizar sobre riscos relacionados à privacidade e uso indevido de dados públicos.


## Tecnologias e Ferramentas

* Python 3.10.12


## Pipeline do Projeto

```text
1. Coleta de dados      → Identificação de fontes confiáveis e coleta de informações
2. Pré-processamento    → Limpeza, normalização e quebra em páginas de textos
3. Extração de dados    → Named Entity Recognition and Classification (NERC) e Relation Extraction
4. Avaliações           → Avaliação do Modelo e Avaliação de Remontagem de Identidade
```


## Instalação

Recomenda-se o uso de um ambiente virtual. Para instalar as dependências:

```bash
pip install -r requirements.txt
```

> Importante: o projeto utiliza a biblioteca `nltk`. Na primeira execução, será necessário baixar o pacote `punkt`:
```python
import nltk
nltk.download('punkt')
```

## Execução

Para executar o pipeline principal:

```bash
python main.py
```

---


## Aviso Legal

Este projeto é exclusivamente acadêmico e educativo. 
Nenhum dado pessoal real é exposto ou utilizado com finalidades indevidas.
Uso inadequado do código é de inteira responsabilidade do usuário.


---

