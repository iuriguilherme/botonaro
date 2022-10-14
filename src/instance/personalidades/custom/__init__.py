"""Personalidade: Botonaro"""

import logging
logger = logging.getLogger(__name__)

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

async def add_instance_handlers(dispatcher: Dispatcher) -> None:
    """Registra handlers para aiogram.Dispatcher, lida com Telegram"""
    try:
        from geracao_1 import (
            gatilhos_1,
            gatilhos_2,
            gatilhos_3,
            respostas_1,
            respostas_2,
            respostas_3,
        )
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_1()))),
            # ~ is_reply_to_id = dispatcher.bot.id,
        )
        async def palavras_1_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 1"""
            descriptions: list = [
                'botonaro',
                'geracao1',
                'gatilho1',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            try:
                await message_callback(message, descriptions)
                # ~ command: Union[types.Message, None] = None
                # ~ if (await dice_low(15)):
                    # ~ command = await message.reply(await respostas_1())
                # ~ if command is not None:
                    # ~ await command_callback(command, descriptions)
                command: types.Message = await message.reply(
                    await respostas_1())
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_2()))),
        )
        async def palavras_2_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 2"""
            descriptions: list = [
                'botonaro',
                'geracao1',
                'gatilho2',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            try:
                await message_callback(message, descriptions)
                command: types.Message = await message.reply(
                    await respostas_2())
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
        @dispatcher.message_handler(
            filters.Regexp(r'\b({})\b'.format('|'.join(await gatilhos_3()))),
        )
        async def palavras_3_callback(message: types.Message) -> None:
            """Geração 1 de gatilhos e respostas, gatilhos 3"""
            descriptions: list = [
                'botonaro',
                'geracao1',
                'gatilho3',
                dispatcher.config.personalidade,
                message.chat.type,
            ]
            try:
                await message_callback(message, descriptions)
                command: types.Message = await message.reply(
                    await respostas_3())
            except Exception as e1:
                logger.exception(e1)
                await error_callback("Erro respondendo gatilho", message,
                    e1, ['exception'] + descriptions)
    except Exception as e:
        logger.error("Arquivos não foram gerados corretamente")
        logger.exception(e)
