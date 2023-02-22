"""
Personalidade ia.cecil: Botonaro

Copyright 2022 Iuri Guilherme <https://iuri.neocities.org/>  

Creative Commons 4.0 Attribution Share Alike  
"""

import logging
logger = logging.getLogger(__name__)

import io
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
from plugins.natural import dispersion_plot_1
# ~ from plugins.openai import get_aiogram_chatgpt_completion
from .buscamemo import (
    busca_callback,
    busca_quieta,
    busca_responde,
    ZeroResultsException,
)
from .natural import (
    context_all,
    concordance_all,
    count_all,
    generate_all,
    get_all_telegram_texts,
    similar_all,
    statistics_all,
)

async def add_instance_handlers(dispatcher: Dispatcher) -> None:
    """Registra handlers para aiogram.Dispatcher, lida com Telegram"""
    try:
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['nstats', 'nstatistics'],
        )
        async def nstatistics_callback(message: types.Message) -> None:
            """Estatísticas"""
            descriptions: list = [
                'botonaro',
                'natural',
                'statistics',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                await message.answer_chat_action("typing")
                reply: str = await statistics_all()
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro calculando estatísticas"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['ngen', 'ngenerate'],
        )
        async def ngenerate_callback(message: types.Message) -> None:
            """NLTK text.generate()"""
            descriptions: list = [
                'botonaro',
                'natural',
                'generate',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                generated: str = (await generate_all(
                    message.get_args()))
                if len(generated) > 0:
                    reply: str = generated
                else:
                    reply: str = "Nada gerado"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['ncon', 'nconcordance'],
        )
        async def nconcordance_callback(message: types.Message) -> None:
            """NLTK text.concordance()"""
            descriptions: list = [
                'botonaro',
                'natural',
                'concordance',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                if len(message.get_args()) > 0:
                    concordances: str = (await concordance_all(
                        message.get_args()))
                    if len(concordances) > 0:
                        reply: str = concordances
                    else:
                        reply: str = "Nenhuma concordância"
                else:
                    reply: str = "Que palavra?"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['ncom', 'ncontext'],
        )
        async def ncontext_callback(message: types.Message) -> None:
            """NLTK text.common_contexts()"""
            descriptions: list = [
                'botonaro',
                'natural',
                'context',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                if len(message.get_args()) > 0:
                    contexts: str = (await context_all(message.get_args()))
                    if len(contexts) > 0:
                        reply: str = contexts
                    else:
                        reply: str = "Nenhum contexto comum"
                else:
                    reply: str = "Que palavra?"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['nsim', 'nsimilar'],
        )
        async def nsimilar_callback(message: types.Message) -> None:
            """NLTK text.similar()"""
            descriptions: list = [
                'botonaro',
                'natural',
                'similar',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                if len(message.get_args()) > 0:
                    similars: str = (await similar_all(
                        message.get_args()))
                    if len(similars) > 0:
                        reply: str = similars
                    else:
                        reply: str = "Nenhuma termo similar"
                else:
                    reply: str = "Que palavra?"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['ncon', 'ncount'],
        )
        async def ncount_callback(message: types.Message) -> None:
            """Estatísticas: conta quantas vezes uma palavra foi dita"""
            descriptions: list = [
                'botonaro',
                'natural',
                'count',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            await message_callback(message, descriptions)
            reply: str = "Não consegui :("
            try:
                if len(message.get_args()) > 0:
                    counted: str = (await count_all(
                        message.get_args()))
                    reply: str = f"""{message.get_args()} já foi dito \
{counted.get('count')} vezes, sendo {counted.get('percentage'):.2f}% do que \
já foi dito."""
                else:
                    reply: str = "Que palavra?"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
        @dispatcher.message_handler(
            filters.IDFilter(
                user_id = dispatcher.config.telegram['users']['alpha'] + \
                dispatcher.config.telegram['users']['beta'],
            ),
            commands = ['nlex', 'ndispersion'],
        )
        async def ndispersion_callback(message: types.Message) -> None:
            """NLTK lexycal dispersion plot"""
            descriptions: list = [
                'botonaro',
                'natural',
                'lexical',
                dispatcher.config.personalidade,
                message.chat.type,
            ] # descriptions
            command: typing.Union[types.Message, None] = None
            reply: str = "Não consegui :("
            try:
                await message_callback(message, descriptions)
                if len(message.get_args()) > 0:
                    words: list = message.get_args().split(' ')
                    plot: io.BytesIO = io.BytesIO()
                    try:
                        plot.close()
                        texts: list[str] = [
                            text for texts in \
                            await get_all_telegram_texts() \
                            for text in texts
                        ]
                        plot: io.BytesIO = await dispersion_plot_1(texts,
                            words)
                        command: types.Message = await message.reply_photo(
                            plot.getbuffer(),
                            caption = f"""Dispersão léxica para os termos: \
{' '.join(words)}""",
                        )
                    except Exception as e2:
                        await erro_callback(
                            "Error trying to send graphic",
                            message,
                            e2,
                            ['exception'] + descriptions,
                        )
                    finally:
                        plot.close()
                else:
                    reply: str = "Que palavra?"
            except Exception as e1:
                logger.exception(e1)
                reply: str = "Erro buscando termos"
                await error_callback(reply, message, e1,
                    ['exception'] + descriptions)
            if command is None:
                command: types.Message = await message.reply(reply)
            await command_callback(command, descriptions)
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
        # ~ @dispatcher.message_handler(
            # ~ content_types = types.ContentTypes.TEXT,
            # ~ state = "*",
        # ~ )
        # ~ async def chance_gpt_callback(message: types.Message) -> None:
            # ~ """Responde como ChatGPT em uma chance aleatória"""
            # ~ try:
                # ~ if await dice_low(int(os.environ.get("CHANCE", 30))):
                    # ~ await get_aiogram_chatgpt_completion(
                        # ~ dispatcher = dispatcher,
                        # ~ message = message,
                    # ~ )
            # ~ except Exception as e1:
                # ~ logger.exception(e1)
                # ~ await error_callback("Erro buscando frase", message,
                    # ~ e1, ['exception'])
    except Exception as e:
        logger.exception(e)
        logger.error("Não consegui registrar os handlers de busca")
