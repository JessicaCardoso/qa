# IQA

## Executando

Realizar download dos modelos e colocar nas pastas [RE_Models]()  e [models]() na raiz do projeto.

* **Python**

Instalar as bibliotecas contidas no requirements.txt

```bash
$ pip install -r requirements.txt
```

Realizar download dos modelos do spaCy

```bash
$ python -m spacy download pt_core_news_sm
$ python -m spacy download pt
```

Executar arquivo `run.sh`, o IQA vai ser executado no seguinte endereço http://127.0.0.1:5000/.

```bash
$ bash run.sh
```