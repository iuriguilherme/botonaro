Botonaro
===

Chatbot que interage com material do Bolsodata do 
[Metamemo](https://metamemo.info/).  

Instruções
---

Atualmente a única interface é um bot de telegram usando uma biblioteca 
externa apropriada para esta finalidade.  

Crie um arquivo `.env` com um par chave = valor:  

    TELEGRAM_TOKEN = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11  

```sh
$ python -m venv venv  
$ source venv/bin/activate # No Windows, Power Shell: .\venv\Scripts\activate  
(venv) $ pip install -e git+https://github.com/iuriguilherme/botonaro.git@stable#egg=botonaro  
(venv) $ pip install -e git+https://github.com/iuriguilherme/iacecil.git@stable#egg=iacecil  
(venv) $ python -m botonaro  
```

Para usar a funcionalidade de log e feedback em grupos do telegram, adicionar 
ao arquivo `.env`:  

```
ADMIN_CHATS = [1]
INFO_CHAT = -1
DEBUG_CHAT = -1
FEEDBACK_CHAT = -1
```

Substituindo 1s e -1s com os ids de usuário ou grupo pra quem o bot deve 
mandar mensagens de erro e etc.  

Para usar a funcionalidade principal de busca no metamemo, adicionar ao 
arquivo `.env`:  

```
BASE_URL = http://metamemo.info
LIST_ROUTE = /lista
ITEM_ROUTE = /metamemo
SOURCES_BUSCA = Facebook,Twitter,Youtube,Instagram,Telegram,Blog
START_DATE_BUSCA = 2022-01-01
CHANCE = 30
```

Adaptar **SOURCES_BUSCA** para o tipo de busca pertinente.  

Licença
---

Copyright 2022 Iuri Guilherme <https://iuri.neocities.org/>  

[Creative Commons 4.0 Attribution Share Alike](LICENSE.markdown)  
