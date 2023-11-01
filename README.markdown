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

Para obter um token de Bot de Telegram, fale com o 
[@BotFather](https://t.me/botfather).  

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

Para usar a funcionalidade de integração com ChatGPT, adicionar ao 
arquivo `.env`:  

    OPENAI_API_KEY = sk-1234567890abcdef  

Para obter uma chave de API, acesse 
<https://platform.openai.com/account/api-keys>  

Roadmap
---

### [Pre-alpha v0.2](https://github.com/iuriguilherme/botonaro/releases/tag/pre-alpha)

Protótipo para apresentação para o Bolsodata  

### [Alpha v0.3](https://github.com/iuriguilherme/botonaro/releases/tag/alpha)

Chatbot de telegram, extensão de personalidade de 
[ia.cecil](https://github.com/iuriguilherme/iacecil)  

1. Lê quatro tipos de mensagem:
  1. Aquelas que contém o gatilho "fala sobre"
  1. Aquelas que começam com o comando "/sobre"
  1. Todas aquelas que foram enviadas para um chat particular
  1. 1:30 chance das que forem enviadas para um grupo
1. Usa o texto da mensagem para buscar na fonte de frases
1. Responde a mensagem com a frase, incluindo a referência

### [Alpha v0.4](https://github.com/iuriguilherme/botonaro/releases/tag/v0.4.0)

_(em desenvolvimento)_  

1. Funcionalidadas herdadas da versão 0.3
1. Registra reações a mensagens
1. Interface web com gráficos e estatísticas de reações
1. A cada mensagem, uma chance de responder usando ChatGPT

Licença
---

Copyright 2022-2023 Iuri Guilherme <https://iuri.neocities.org/>  

[Creative Commons 4.0 Attribution Share Alike](LICENSE.markdown)  
