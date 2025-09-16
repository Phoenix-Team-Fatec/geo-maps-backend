# 📌 *GeoMaps Backend — Visiona*

*Este repositório contém a implementação do **backend** do projeto **GeoMaps (Visiona)**,*

*O objetivo é fornecer uma API robusta para gerenciamento de propriedades rurais, endereçamento digital (Plus Codes), roteirização rural e registro colaborativo de condições de vias.*

## 📂 *Estrutura de Arquivos*

```bash
├── app/ 
    ├── core/ 
    ├── main.py 
    ├── models/
    ├── repositories/ 
    ├── routes/ 
    ├── schemas/ 
    ├── services/ 
    ├── utils/ 
├── requirements.txt 
├── main.py
```


### 📁 Descrição das Pastas

- **core/** → Configurações principais da aplicação, como conexão com o MongoDB e middlewares globais.  
- **main.py** → Arquivo inicial que executa a aplicação FastAPI.  
- **models/** → Estruturas que representam os documentos do banco (camada mais próxima do Mongo).  
- **schemas/** → Estruturas de validação Pydantic para entrada e saída de dados (camada exposta da API).  
- **repositories/** → Responsáveis por interagir com o banco de dados (CRUD).  
- **services/** → Contêm as regras de negócio que utilizam os repositórios e modelos.  
- **routes/** → Definem os endpoints expostos pela API.  
- **utils/** → Funções auxiliares reutilizáveis (ex.: formatação de datas, geração de hashes).  

---

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**  
  Framework web moderno e de alto desempenho para construção de APIs em Python.  
  Recursos principais:
  - Validação automática com Pydantic.
  - Documentação interativa (Swagger e ReDoc).
  - Suporte nativo a async/await.


- **[MongoDB](https://www.mongodb.com/)**  
  Banco de dados NoSQL orientado a documentos, ideal para dados geoespaciais.  
  - Armazenamento flexível em formato JSON-like (BSON).  
  - Suporte a índices geoespaciais para consultas rápidas.  


- **[PyMongo](https://pymongo.readthedocs.io/)**  
  Driver oficial do MongoDB para Python.  
  - Útil para operações síncronas.  
  - Mais próximo da API nativa do MongoDB.  
  

- **[Motor](https://motor.readthedocs.io/)**  
  Driver assíncrono do MongoDB para Python.  
  - Baseado em `asyncio`.  
  - Integração perfeita com o FastAPI, permitindo operações de I/O sem bloqueio.  


---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/api5-api
cd api5-api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
uvicorn main:app --reload
```

#### A API estará disponível em:

>  http://127.0.0.1:8000


### 5. Documentação da API
- Swagger: `http://127.0.0.1:8000/docs`

- ReDoc: `http://127.0.0.1:8000/redoc`
