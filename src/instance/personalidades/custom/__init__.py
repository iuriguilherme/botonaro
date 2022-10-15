"""Personalidade: Botonaro"""

import logging
logger = logging.getLogger(__name__)

import aiohttp
import datetime
import os
from aiogram import (
    Dispatcher,
    filters,
    types,
)
from typing import Union
from iacecil.controllers.aiogram_bot.callbacks import (
    command_callback,
    message_callback,
    error_callback,
)
from iacecil.controllers.util import (
    dice_high,
    dice_low,
)

async def busca_frase(
    palavras: list[str],
    message: types.Message,
) -> None:
    try:
        fonte_url: str = os.environ.get('FONTE_URL')
        sources: list = os.environ.get('SOURCES_BUSCA').split(',')
        start_date: str = os.environ.get('START_DATE_BUSCA')
        end_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
        async with aiohttp.ClientSession() as session:
            url: str = f"{fonte_url}/?" + "&".join([
                f"source={source}" for source in sources
            ]) + "&".join([
                f"content={'%20'.join(palavras)}",
                f"start_date={start_date}",
                f"end_date={end_date}",
            ])
            logger.debug(url)
            async with session.get(url) as response:
                metamemo = await response
                logger.debug(str(metamemo))
                await message.reply(str(metamemo))
    except Exception as e:
        logger.exception(e)
        await error_callback("Erro buscando frase", message, e,
            ['exception', 'botonaro', 'buscafrase'],
        )
        await message.reply("""não me recordo de nada no tocante a essa \
qüestão aí talquei""")

async def add_instance_handlers(dispatcher: Dispatcher) -> None:
    """Registra handlers para aiogram.Dispatcher, lida com Telegram"""
    try:
        @dispatcher.message_handler(commands = ['sobre', 'm'])
        async def busca_comando_callback(message: types.Message) -> None:
            logger.debug("busca_comando")
            descriptions: list = [
                'botonaro',
                'buscamemo',
                'buscacomando',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            await message_callback(message, descriptions)
            await command_callback(
                await busca_frase(message.get_args().split(' '), message),
                descriptions,
            )
        @dispatcher.message_handler(filters.Regexp(r'\bfala sobre\b'))
        async def busca_natural_callback(message: types.Message) -> None:
            logger.debug("busca_natural")
            descriptions: list = [
                'botonaro',
                'buscamemo',
                'buscacomando',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            await message_callback(message, descriptions)
            await command_callback(
                await busca_frase(
                    [
                        termo \
                        for termo in \
                        message.get_args().split(' ') \
                        if termo not in \
                        ['fala', 'sobre']
                    ],
                    message,
                ),
                descriptions,
            )
    except Exception as e:
        logger.debug("Não consegui registrar os handlers de busca")
        logger.exception(e)
    try:
        ## TODO compreensão de lista e import_module URGENTE
        from geracao_1 import (
            gatilhos_1,
            gatilhos_2,
            gatilhos_3,
            gatilhos_5,
            gatilhos_6,
            gatilhos_7,
            gatilhos_8,
            respostas_1,
            respostas_2,
            respostas_3,
            respostas_4,
            respostas_5,
            respostas_6,
            respostas_7,
            respostas_8,
        )
        @dispatcher.message_handler(is_reply_to_id = dispatcher.bot.id)
        async def palavras_4_callback(message: types.Message) -> None:
            descriptions: list = [
                'botonaro',
                'geracao1',
                'gatilho4',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            try:
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_4()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro treplicando", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_1()))),
            # ~ is_reply_to_id = dispatcher.bot.id,
        )
        async def palavras_1_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 1"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho1',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                # ~ command: Union[types.Message, None] = None
                # ~ if (await dice_low(15)):
                    # ~ command = await message.reply(await respostas_1())
                # ~ if command is not None:
                    # ~ await command_callback(command, descriptions)
                await command_callback(await message.reply(
                    await respostas_1()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_2()))),
            is_reply_to_id = dispatcher.bot.id,
        )
        async def palavras_2_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 2"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho2',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_2()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_3()))),
        )
        async def palavras_3_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 3"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho3',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_3()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_5()))),
        )
        async def palavras_5_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 5"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho5',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_5()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_6()))),
        )
        async def palavras_6_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 6"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho6',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_6()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_7()))),
        )
        async def palavras_7_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 7"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho7',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_7()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_8()))),
        )
        async def palavras_8_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 8"""
            try:
                descriptions: list = [
                    'botonaro',
                    'geracao1',
                    'gatilho8',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ]
                await message_callback(message, descriptions)
                await command_callback(await message.reply(
                    await respostas_8()), descriptions)
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
    except Exception as e:
        logger.error("Arquivos não foram gerados corretamente")
        logger.exception(e)
