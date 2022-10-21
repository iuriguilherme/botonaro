"""
Personalidade ia.cecil: Botonaro

Copyright 2022 Iuri Guilherme <https://iuri.neocities.org/>  

Creative Commons 4.0 Attribution Share Alike  
"""

import logging
logger = logging.getLogger(__name__)

import os
import random
import typing
from aiogram import (
    Dispatcher,
    filters,
    types,
)
from iacecil.controllers.aiogram_bot.callbacks import (
    command_callback,
    message_callback,
    error_callback,
)
from iacecil.controllers.util import (
    dice_high,
    dice_low,
)
from .buscamemo import (
    busca_callback,
    busca_quieta,
    busca_responde,
    ZeroResultsException,
)

async def add_instance_handlers(dispatcher: Dispatcher) -> None:
    """Registra handlers para aiogram.Dispatcher, lida com Telegram"""
    try:
        @dispatcher.message_handler(commands = ['start', 'help', 'info'])
        async def start_callback(message: types.Message) -> None:
            """Resposta específica para comando /start"""
            descriptions: list = [
                'botonaro',
                'start',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            command: types.Message = await message.reply("""Pode mandar \
qualquer termo ou frase que eu vou tentar achar na internet o que é que a \
minha família disse sobre isso aí ta ok""")
            await command_callback(command, descriptions)
        @dispatcher.message_handler(is_reply_to_id = dispatcher.bot.id)
        async def reply_callback(message: types.Message) -> None:
            """Resposta específica para mensagens como respostas"""
            descriptions: list = [
                'botonaro',
                'reply',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            command: types.Message = await message.reply(random.choice([
                u"\U0001f44d",
                "ta ok",
                "talquei",
                "tem que ver isso daí",
                "forte abraço! (hétero)",
                u"\U0001f4f5" + f""" Comentário removido pelo Supremo \
Tribunal {random.choice(["Federal", "Eleitoral"])}""",
            ]))
            await command_callback(command, descriptions)
        @dispatcher.message_handler(commands = ['sobre', 'm'])
        async def busca_comando_callback(message: types.Message) -> None:
            """Busca através dos argumentos do comando"""
            try:
                descriptions: list = [
                    'botonaro',
                    'buscamemo',
                    'buscacomando',
                    dispatcher.config.personalidade,
                    message.chat.type,
                ] # descriptions
                await message_callback(message, descriptions)
                try:
                    command: types.Message = await busca_callback(
                        message,
                        message.get_args().split(' '),
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
                await error_callback("Erro buscando frase", message, e1, 
                    ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\bfala sobre\b'),
            content_types = types.ContentTypes.TEXT,
        )
        async def busca_natural_callback(message: types.Message) -> None:
            await busca_responde(message)
        @dispatcher.message_handler(
            filters.ChatTypeFilter(types.ChatType.PRIVATE),
            content_types = types.ContentTypes.TEXT,
        )
        async def busca_private_callback(message: types.Message) -> None:
            await busca_responde(message)
        @dispatcher.message_handler(
            content_types = types.ContentTypes.TEXT,
            state = "*",
        )
        async def chance_busca_callback(message: types.Message) -> None:
            """Responde em uma chance aleatória"""
            try:
                if await dice_low(int(os.environ.get("CHANCE", 30))):
                    await busca_quieta(message)
                else:
                    logger.debug("sem resposta")
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro buscando frase", message,
                    e1, ['exception'])
    except Exception as e:
        logger.error("Não consegui registrar os handlers de busca")
        logger.exception(e)
