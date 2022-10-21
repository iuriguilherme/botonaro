"""Personalidade ia.cecil: Botonaro"""

import logging
logger = logging.getLogger(__name__)

import aiohttp
import bs4
import datetime
import locale
import os
import random
import typing
from aiogram import (
    Dispatcher,
    filters,
    types,
)
from aiogram.utils import markdown
from aiogram.types import InputFile as URLInputFile
from importlib import import_module
from iacecil.controllers.aiogram_bot.callbacks import (
    command_callback,
    message_callback,
    error_callback,
)
from iacecil.controllers.util import (
    dice_high,
    dice_low,
)

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
    titulo: str
    fonte: str
    data: datetime.datetime
    metamemo: str
    url: str
    midia: list[str]
    def __repr__(self):
        return f"""<ResultMixin(\
link: {self.link}, \
titulo: {self.titulo}, \
fonte: {self.fonte}, \
data: {str(self.data)}, \
metamemo: {self.metamemo}, \
url: {self.url}, \
midia: {",".join(self.midia)}\
>"""

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
        columns: bs4.element.ResultSet = result_item.find_all('div', 's1')
        result.link: str = columns[0].find('a', 'icon-eye').get('href')
        result.titulo: str = result_item.find('div', 's5').text
        result.fonte: str = columns[1].find('i').get('class')[1].split('-'
            )[1].strip('1').capitalize()
        result.data: datetime.datetime = datetime.datetime.strptime(
            " ".join([columns[2].text, columns[3].text]), "%d/%m/%Y %H:%M")
        result.metamemo: str = columns[4].text
        result.url: str = columns[5].find('a').get('href')
        result.midia: list[str] = [a.get('href') for a in \
            columns[6].find_all('a')]
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
        soup: BeautifulSoup = await bytes_to_soup(await html_to_bytes(url))
        results: bs4.element.ResultSet = soup.find('div', 'search-results')
        results: bs4.element.ResultSet = results.find_all('div', 'result-item')
        retornos: list = [await parse_result(result) for result in results]
        logger.debug(f"Encontrados {len(retornos)} resultados")
        return retornos
    except Exception as e:
        logger.exception(e)
        # ~ logger.debug(f"""len(retornos) = {len(retornos)}\nretornos.titulo = {[
            # ~ retorno.titulo for retorno in retornos]}""")
        return []

async def add_instance_handlers(dispatcher: Dispatcher) -> None:
    """Registra handlers para aiogram.Dispatcher, lida com Telegram"""
    try:
        ## Estes módulos são gerados por outros scripts em tempo de execução,
        ## não tem como manter o código em versionamento (ou tem?)
        async def palavras_callback(
            message: types.Message,
            geracao: str,
            gatilho: str,
            respostas: object,
        ) -> None:
            """
            Retorna palavra gerada associada a gatilho de uma geração 
            específica  
            """
            try:
                descriptions: list = ['botonaro', geracao, gatilho,
                    dispatcher.config.personalidade, message.chat.type]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        geracoes: list = []
        for g in range(1, 1):
            try:
                geracao[g]: object = import_module('geracao_' + str(g))
                for n in range(1, geracao[g].gatilhos):
                    try:
                        dispatcher.register_message_handler(
                            palavras_callback,
                            filters.Regexp(
                                r"\b({})\b".format(
                                    "|".join(
                                        await getattr(
                                            geracao[g],
                                            'gatilhos_' + str(n),
                                        )()
                                    )
                                )
                            ),
                            filters.ChatTypeFilter([
                                types.ChatType.GROUP,
                                types.ChatType.SUPERGROUP,
                            ]),
                            geracao = str(g),
                            gatilhos = str(n),
                            respostas = getattr(
                                geracao[g],
                                "respostas_" + str(n),
                            ),
                        ) # register_message_handler
                    except Exception as e2:
                        logger.exception(e2)
                ## FIXME Robô desgraçado não tá respondendo nada
                @dispatcher.message_handler(
                    filters.ChatTypeFilter(
                        types.ChatType.PRIVATE,
                        types.ChatType.GROUP,
                        types.ChatType.SUPERGROUP,
                    ),
                    is_reply_to_id = dispatcher.bot.id,
                )
                async def reply_callback(message: types.Message) -> None:
                    """Resposta específica para mensagens como respostas"""
                    return await palavras_callback(
                        message,
                        geracao = str(g),
                        gatilhos = "4",
                        respostas = getattr(geracao[g], "respostas_" + "4"),
                    )
                ## FIXME: Robô desgraçado responde /start com busca_natural
                ## (handler registrado no final deste arquivo)
                ## Eu quase quebrei a mesa tentando descobrir porquê, esse
                ## método aqui pelo jeito não faz bosta nenhuma
                @dispatcher.message_handler(
                    filters.ChatTypeFilter(
                        types.ChatType.PRIVATE,
                        types.ChatType.GROUP,
                        types.ChatType.SUPERGROUP,
                    ),
                    commands = ['start'],
                )
                async def start_callback(message: types.Message) -> None:
                    """Resposta específica para comando /start"""
                    return await palavras_callback(
                        message,
                        geracao = str(g),
                        gatilhos = "9",
                        respostas = getattr(geracao[g], "respostas_" + "9"),
                    )
            except Exception as e1:
                logger.exception(e1)
            else:
                logger.debug("Carregado geracao_" + str(g))
    except Exception as e:
        logger.error("Arquivos não foram gerados corretamente")
        logger.exception(e)
    try:
        async def busca_callback(
            message: types.Message,
            palavras: str,
            descriptions: list,
        ) -> typing.Union[types.Message, None]:
            """Busca frase de acordo com palavras chave"""
            try:
                frases: list[ResultMixin] = [
                    frase for frase in \
                    await busca_frase(palavras) \
                    if hasattr(frase, 'link')
                ]
                if len(frases) < 1:
                    raise ZeroResultsException()
                else:
                    item: ItemMixin = await busca_item(random.choice(
                        frases).link)
                    formato_data: str = "em %d/%m/%Y às %H:%M"
                    if locale.getlocale()[0] == "pt_BR":
                        formato_data: str = "%A, %d/%m/%Y às %H:%M"
                    captions: list = [f"""Publicado por {item.metamemo} \
{item.data.strftime(formato_data)}."""]
                    if int(item.apoios) + int(item.comentarios) > 0:
                        captions.append(f"{item.apoios} " + u"\U0001f44d" + \
                            f"{item.comentarios} " + u"\U0001f4ac")
                    if item.link not in [None, '', ' ']:
                        captions.append(f"Link: {item.link}")
                    caption: str = markdown.spoiler("\n".join(captions))
                    texto: str = "\n".join([markdown.escape_md(item.texto),
                        "", caption])
                    if len(texto) < 24+1e3:
                        caption: str = texto
                if item.video is not None:
                    try:
                        return await message.reply_video(
                            video = URLInputFile.from_url(item.video),
                            caption = caption,
                            parse_mode = "MarkdownV2",
                            disable_notification = True,
                            # ~ disable_web_page_preview = True,
                            allow_sending_without_reply = True,
                        )
                    except Exception as e2:
                        logger.exception(e2)
                        await error_callback("Erro tentando mandar vídeo",
                            message, e2, ['exception'] + descriptions)
                elif item.imagem is not None:
                    try:
                        return await message.reply_photo(
                            photo = URLInputFile.from_url(item.imagem),
                            caption = caption,
                            parse_mode = "MarkdownV2",
                            disable_notification = True,
                            # ~ disable_web_page_preview = True,
                            allow_sending_without_reply = True,
                        )
                    except Exception as e2:
                        logger.exception(e2)
                        await error_callback("Erro tentando mandar imagem",
                            message, e2, ['exception'] + descriptions)
                return await message.reply(
                    text = texto,
                    parse_mode = "MarkdownV2",
                    disable_notification = True,
                    disable_web_page_preview = True,
                    allow_sending_without_reply = True,
                )
            except ZeroResultsException:
                ## TODO: Mover para comandos onde está se aguardando
                ## de fato uma resposta
                return None
                # ~ return await message.reply(
                    # ~ text = """não me recordo de nada no tocante a essa \
# ~ qüestão aí talquei""",
                    # ~ disable_notification = True,
                    # ~ allow_sending_without_reply = True,
                # ~ )
            except Exception as e1:
                logger.exception(e1)
                return None
        @dispatcher.message_handler(commands = ['sobre', 'm'])
        async def busca_comando_callback(message: types.Message) -> None:
            """Busca através dos argumentos do comando"""
            descriptions: list = [
                'botonaro',
                'buscamemo',
                'buscacomando',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            try:
                await command_callback(
                    await busca_callback(
                        message,
                        message.get_args().split(' '),
                        descriptions,
                    ),
                    descriptions,
                ) # command_callback
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro buscando frase", message,
                    e1, ['exception'] + descriptions)
        async def busca_natural(message: types.Message) -> None:
            """Busca através de palavras na mensagem"""
            try:
                descriptions: list = [
                    'botonaro',
                    'buscamemo',
                    'buscanatural',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ] # descriptions
                await message_callback(message, descriptions)
                await command_callback(
                    await busca_callback(
                        message,
                        [
                            termo \
                            for termo in \
                            message.text.split(' ') \
                            if termo not in \
                            ['fala', 'sobre', '/start', '/sobre', '/m']
                        ],
                        descriptions,
                    ),
                    descriptions,
                ) # command_callback
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro buscando frase", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\bfala sobre\b'),
            content_types = types.ContentTypes.TEXT,
        )
        async def busca_natural_callback(message: types.Message) -> None:
            await busca_natural(message)
        @dispatcher.message_handler(
            filters.ChatTypeFilter(types.ChatType.PRIVATE),
            content_types = types.ContentTypes.TEXT,
        )
        async def busca_private_callback(message: types.Message) -> None:
            await busca_natural(message)
        @dispatcher.message_handler(
            content_types = types.ContentTypes.TEXT,
            state = "*",
        )
        async def chance_busca_callback(message: types.Message) -> None:
            """Responde em uma chance aleatória"""
            try:
                if await dice_low(int(os.environ.get("CHANCE", 30))):
                    await busca_natural(message)
                else:
                    logger.debug("sem resposta")
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro buscando frase", message,
                    e1, ['exception'])
    except Exception as e:
        logger.error("Não consegui registrar os handlers de busca")
        logger.exception(e)
