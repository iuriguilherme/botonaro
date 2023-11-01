"""
Personalidade ia.cecil: Botonaro

Copyright 2022-2023 Iuri Guilherme <https://iuri.neocities.org/>  

Creative Commons 4.0 Attribution Share Alike  
"""

import logging
logger = logging.getLogger(__name__)

import aiohttp
import bs4
import csv
import datetime
from io import StringIO
import locale
import os
import random
import typing
from aiogram import (
    Dispatcher,
    # ~ filters,
    types,
)
## FIXME engambelada enquanto ia.cecil não migra pra aiogram 3
from aiogram.types import InputFile as URLInputFile
from aiogram.utils import markdown
from iacecil.controllers.aiogram_bot.callbacks import (
    command_callback,
    message_callback,
    error_callback,
)
# ~ from iacecil.controllers.util import (
    # ~ dice_high,
    # ~ dice_low,
# ~ )

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except Exception as e:
    logger.debug("Locale brasileira não instalada no sistema")
    logger.exception(e)

class ZeroResultsException(Exception):
    pass

class ItemMixin(object):
    """Modelo para item individual de busca"""
    link: typing.Union[str, None] = None
    fonte: str = "Internet"
    metamemo: str = "Alguém"
    texto: str = "Nada"
    video: typing.Union[str, None] = None
    imagem: typing.Union[str, None] = None
    apoios: str = "0"
    comentarios: str = "0"
    data: datetime.datetime = datetime.datetime.min
    def __repr__(self):
        return f"""<ItemMixin(\
link: {str(self.link)}, \
fonte: {self.fonte}, \
metamemo: {self.metamemo}, \
texto: {self.texto}, \
video: {str(self.video)}, \
imagem: {str(self.imagem)}, \
apoios: {self.apoios}, \
comentarios: {self.comentarios}, \
data: {str(data)}\
>"""

class ResultMixin(object):
    """Modelo para resultado da busca"""
    link: str
    # ~ titulo: str
    # ~ fonte: str
    data: datetime.datetime
    # ~ metamemo: str
    # ~ url: str
    # ~ midia: list[str]
    autor: str
    texto: str
    def __repr__(self):
        return f"""<ResultMixin(\
link: {self.link}, \
data: {str(self.data)}, \
autor: {self.autor}, \
texto: {self.texto}, \
>"""

async def get_csv(url: str) -> typing.Union[object, None]:
    """Performs async HTTP GET on URL and returns csv file"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logger.debug(f"Request to {url}")
                logger.debug(f"Status: {response.status}")
                return await response.read()
    except Exception as e:
        logger.exception(e)
        return None

async def html_to_bytes(url: str) -> typing.Union[bytes, None]:
    """Performs async HTTP GET on URL and returns bytes for parsing"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
    except Exception as e:
        logger.exception(e)
        return None

async def html_to_json(url: str) -> typing.Union[str, None]:
    """Performs async HTTP GET on URL and returns JSON string"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    except Exception as e:
        logger.exception(e)
        return None

async def bytes_to_soup(html: bytes) -> typing.Union[bs4.BeautifulSoup, None]:
    """Parse bytes to beautiful soup"""
    try:
        return bs4.BeautifulSoup(html, "lxml")
    except bs4.FeatureNotFound:
        logger.debug("python-lxml not installed, falling back to html.parser")
        return bs4.BeautifulSoup(html, "html.parser")
    except Exception as e:
        logger.exception(e)
        return None

async def parse_item(rows: bs4.element.ResultSet) -> ItemMixin:
    """Parse HTML into Python Object"""
    try:
        item: ItemMixin = ItemMixin()
        try:
            item.link: str = rows[0].find('a', {'title': "Link original"}
                ).get('href')
        except Exception as e:
            logger.debug("Item provavelmente não tem link")
            logger.exception(e)
        try:
            item.fonte: str = rows[0].find('span').get('class')[0].split('-'
                )[1].strip('1').capitalize()
        except Exception as e:
            logger.debug("Item provavelmente não tem fonte")
            logger.exception(e)
        try:
            item.metamemo: str = rows[0].find('b').text
        except Exception as e:
            logger.debug("Item provavelmente não tem metamemo")
            logger.exception(e)
        try:
            item.texto: str = rows[1].find('p').text
        except Exception as e:
            logger.debug("Item provavelmente não tem texto")
            logger.exception(e)
        try:
            item.video: str = rows[2].find('video', 'metavideo').find('source'
                ).get('src')
        except Exception as e:
            logger.debug("Item provavelmente não tem vídeo")
            logger.exception(e)
        try:
            item.imagem: str = rows[2].find('img').get('src')
        except Exception as e:
            logger.debug("Item provavelmente não tem imagem")
            logger.exception(e)
        try:
            item.apoios: str = rows[3].find_all('b')[1].text
        except Exception as e:
            logger.debug("Item provavelmente não tem curtidas")
            logger.exception(e)
        try:
            item.comentarios: str = rows[3].find_all('b')[2].text
        except Exception as e:
            logger.debug("Item provavelmente não tem comentários")
            logger.exception(e)
        try:
            item.data: datetime.datetime = datetime.datetime.strptime(
                " ".join([
                    b.text.strip('\xa0 ') \
                    for b in \
                    rows[3].find('div', 'data-tempo').find_all('b')
                ]), "%H:%M %d/%m/%Y"
            ) # item.data
        except Exception as e:
            logger.debug("Item provavelmente não tem data")
            logger.exception(e)
        return item
    except Exception as e:
        logger.exception(e)
        return None

async def parse_result(result_item: bs4.element.Tag) -> ResultMixin:
    """Parse HTML into Python Object"""
    try:
        result: ResultMixin = ResultMixin()
        ## Nota do desenvolvedor: eu ODEIO isto. Isso é a coisa mais feia, 
        ## chata e imbecil que existe no mundo da programação. É muito fácil 
        ## editar o HTML que é gerado e quebrar totalmente o modelo que 
        ## esta função cria, me forçando a abrir o navegador, o terminal do 
        ## python e a IDE pra reescrever tudo de novo, do zero. Este aqui é o 
        ## melhor exemplo de porque é que uma coisa que "está funcionando" não 
        ## significa sob hipótese alguma que daqui a alguns segundos ainda vai 
        ## estar "funcionando". Isso aqui não é programar, isso aqui é brincar 
        ## de ficar fazendo gambiarra. No pior sentido. Isso aqui NÃO presta, 
        ## NÃO funciona, NÃO resolve, NÃO soluciona. Só causa problemas e toma 
        ## tempo desnecessariamente. O nome das tags mudou pelo menos uma vez 
        ## durante a fase de testes desse conjunto de subrotinas. 
        ## RESTful API or GTFO. </rant>
        columns: bs4.element.ResultSet = result_item.find_all(
          'td',
          'n-data-table-td',
        )
        result.autor: str = columns[0].find('div').text
        result.link: str = columns[1].find('button').get('title')
        result.data: datetime.datetime = datetime.datetime.strptime(
            columns[2].text, "%d/%m/%Y às %H:%M:%S")
        result.autor: str = columns[3].text
        # ~ result.url: str = ""
        # ~ result.titulo: str = ""
        # ~ result.fonte: str = ""
        # ~ result.midia: list[str] = [""]
        # ~ result.metamemo: str = ""
        return result
    except Exception as e:
        logger.exception(e)
        return None

async def busca_item(link: str) -> ItemMixin:
    """Retorna os dados de um dos itens de uma busca a partir de link"""
    try:
        fonte_url: str = os.environ.get("BASE_URL", "http://example.com")
        url: str = f"{fonte_url}/" + f"{link}"
        logger.debug(f"Buscando item em {url}")
        soup: BeautifulSoup = await bytes_to_soup(await html_to_bytes(url))
        results: bs4.element.ResultSet = soup.find('div', 'memoitem-container',
            ).find_all('div', 'row')
        return await parse_item(results)
    except Exception as e:
        logger.exception(e)
        item: ItemMixin = ItemMixin()
        item.texto: str = ""
        return item

async def busca_frase(
    palavras: list[str],
) -> typing.Union[list, list[ResultMixin]]:
    """Retorna o resultado de uma busca em BASE_URL"""
    try:
        logger.debug("Busca frase")
        fonte_url: str = "/".join([
            os.environ.get("BASE_URL", "http://example.com"),
            os.environ.get("LIST_ROUTE", "/"),
        ])
        sources: list = os.environ.get("SOURCES_BUSCA").split(',')
        start_date: str = os.environ.get("START_DATE_BUSCA")
        end_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
        url: str = f"{fonte_url}/?" \
            + "&".join([f"source={source}" for source in sources]) \
            + f"&content={'%20'.join(palavras)}" \
            + f"&start_date={start_date}" \
            + f"&end_date={end_date}"
        logger.debug(f"Buscando em {url}")
        logger.debug(await html_to_bytes(url))
        soup: BeautifulSoup = await bytes_to_soup(
            await html_to_bytes(url))
        logger.debug(soup)
        results: bs4.element.ResultSet = soup.find(
            'table',
            'n-data-table-tbody',
        )
        results: bs4.element.ResultSet = results.find_all(
            'tr',
            'n-data-table-tr',
        )
        logger.debug(f"Encontrados {len(results)} resultados")
        retornos: list = [await parse_result(result) \
            for result in results]
        logger.debug(f"Processados {len(retornos)} resultados")
        return retornos
    except Exception as e:
        logger.exception(e)
        return []

async def busca_frase_csv(
    palavras: list[str],
) -> typing.Union[list, list[ResultMixin]]:
    """Faz requisição para API com csv"""
    try:
        logger.debug("Busca frase")
        fonte_url: str = "/".join([
            os.environ.get("BASE_URL", "http://example.com"),
            os.environ.get("CSV_ROUTE", "/"),
        ])
        sources: list = os.environ.get("SOURCES_BUSCA").split(',')
        start_date: str = os.environ.get("START_DATE_BUSCA")
        end_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
        url: str = f"{fonte_url}/?format=csv&" \
            + "&".join([f"source={source}" for source in sources]) \
            + f"&content={'%20'.join(palavras)}" \
            + f"&start_date={start_date}" \
            + f"&end_date={end_date}"
        logger.debug(f"Buscando em {url}")
        csv_response: bytes = await get_csv(url)
        with StringIO(csv_response.decode()) as csv_file:
            csv_data: object = csv.reader(csv_file, delimiter = ",")
            # ~ logger.debug(type(csv_data))
            # ~ logger.debug(random.choice(list(csv_data))[6])
            # ~ for l in csv_data:
                # ~ logger.info("teste")
                # ~ logger.info(l)
                # ~ logger.info("fim do teste")
            return [r[6] for r in list(csv_data)]
    except Exception as e:
        logger.exception(e)
        return []

async def busca_callback(
    message: types.Message,
    palavras: str,
    descriptions: list,
) -> typing.Union[types.Message, None]:
    """Busca frase de acordo com palavras chave"""
    try:
        # ~ frases: list[ResultMixin] = [
            # ~ frase for frase in \
            # ~ await busca_frase(palavras) \
            # ~ if hasattr(frase, 'link')
        # ~ ]
        frases: list[str] = await busca_frase_csv(palavras)
        if len(frases) < 1:
            raise ZeroResultsException("Nenhum resultado")
        else:
            # ~ item: ItemMixin = await busca_item(random.choice(
                # ~ frases).link)
            item: str = random.choice(frases)
            # ~ formato_data: str = "em %d/%m/%Y às %H:%M"
            # ~ if locale.getlocale()[0] == "pt_BR":
                # ~ formato_data: str = "%A, %d/%m/%Y às %H:%M"
            # ~ captions: list = [f"""Publicado por {item.autor} \
# ~ {item.data.strftime(formato_data)}."""]
            # ~ if int(item.apoios) + int(item.comentarios) > 0:
                # ~ captions.append(f"{item.apoios} " + u"\U0001f44d" + \
                    # ~ f"{item.comentarios} " + u"\U0001f4ac")
            # ~ if item.link not in [None, '', ' ']:
                # ~ captions.append(f"Link: {item.link}")
            # ~ caption: str = markdown.spoiler("\n".join(captions))
            # ~ texto: str = "\n".join([markdown.escape_md(item.texto),
                # ~ "", caption])
            texto: str = markdown.escape_md(item)
            if len(texto) < 24+1e3:
                caption: str = texto
        # ~ if item.video is not None:
            # ~ try:
                # ~ command: types.Message = await message.reply_video(
                    # ~ video = URLInputFile.from_url(item.video),
                    # ~ caption = caption,
                    # ~ parse_mode = "MarkdownV2",
                    # ~ disable_notification = True,
                    ## disable_web_page_preview = True,
                    # ~ allow_sending_without_reply = True,
                # ~ )
                # ~ try:
                    # ~ logger.debug(command.get('ok'))
                # ~ except Exception as e3:
                    # ~ logger.exception(e3)
                # ~ try:
                    # ~ logger.debug(getattr(command, 'ok'))
                # ~ except Exception as e3:
                    # ~ logger.exception(e3)
                # ~ return command
            # ~ except Exception as e2:
                # ~ logger.exception(e2)
                # ~ await error_callback("Erro tentando mandar vídeo",
                    # ~ message, e2, ['exception'] + descriptions)
        # ~ elif item.imagem is not None:
            # ~ try:
                # ~ command: types.Message = await message.reply_photo(
                    # ~ photo = URLInputFile.from_url(item.imagem),
                    # ~ caption = caption,
                    # ~ parse_mode = "MarkdownV2",
                    # ~ disable_notification = True,
                    # ~ ## disable_web_page_preview = True,
                    # ~ allow_sending_without_reply = True,
                # ~ )
                # ~ try:
                    # ~ logger.debug(command.get('ok'))
                # ~ except Exception as e3:
                    # ~ logger.exception(e3)
                # ~ try:
                    # ~ logger.debug(getattr(command, 'ok'))
                # ~ except Exception as e3:
                    # ~ logger.exception(e3)
                # ~ return command
            # ~ except Exception as e2:
                # ~ logger.exception(e2)
                # ~ await error_callback("Erro tentando mandar imagem",
                    # ~ message, e2, ['exception'] + descriptions)
        command: types.Message = await message.reply(
            text = texto,
            parse_mode = "MarkdownV2",
            disable_notification = True,
            disable_web_page_preview = True,
            allow_sending_without_reply = True,
        )
        try:
            logger.debug(command.get('ok'))
        except Exception as e2:
            logger.exception(e2)
        try:
            logger.debug(getattr(command, 'ok'))
        except Exception as e2:
            logger.exception(e2)
        return command
    except Exception as e1:
        logger.exception(e1)
        raise

async def busca_quieta(message: types.Message) -> None:
    """
    Busca através de palavras na mensagem, não responde se não achar 
    nada
    """
    descriptions: list = [
        'botonaro',
        'buscamemo',
        'buscanatural',
        Dispatcher.get_current().config.personalidade,
        message.chat.type,
    ] # descriptions
    try:
        await message_callback(message, descriptions)
        try:
            command: types.Message = await busca_callback(
                message,
                [
                    termo \
                    for termo in \
                    message.text.split(' ') \
                    if termo not in \
                    ["fala", "Fala", "sobre", "start"]
                ],
                descriptions,
            ) # command
        except ZeroResultsException:
            logger.debug("sem resultados")
        else:
            await command_callback(command, descriptions)
    except Exception as e1:
        logger.exception(e1)
        await error_callback("Erro buscando frase", message,
            e1, ['exception'] + descriptions)

async def busca_responde(message: types.Message) -> None:
    """
    Busca através de palavras na mensagem e informa se não achar nada
    """
    descriptions: list = [
        'botonaro',
        'buscamemo',
        'buscanatural',
        Dispatcher.get_current().config.personalidade,
        message.chat.type,
    ] # descriptions
    try:
        await message_callback(message, descriptions)
        try:
            command: types.Message = await busca_callback(
                message,
                [
                    termo \
                    for termo in \
                    message.text.split(' ') \
                    if termo not in \
                    ["fala", "Fala", "sobre", "start"]
                ],
                descriptions,
            ) # command
        except ZeroResultsException:
            command: types.Message = await message.reply(
                text = """não me recordo de nada no tocante a essa \
qüestão aí talquei""",
                disable_notification = True,
                allow_sending_without_reply = True,
            ) # command
        await command_callback(command, descriptions)
    except Exception as e1:
        logger.exception(e1)
        await error_callback("Erro buscando frase", message,
            e1, ['exception'] + descriptions)
