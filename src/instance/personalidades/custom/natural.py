"""
Personalidade ia.cecil: Botonaro

Copyright 2022 Iuri Guilherme <https://iuri.neocities.org/>  

Creative Commons 4.0 Attribution Share Alike  
"""

import logging
logger = logging.getLogger(__name__)

import glob
from aiogram import (
    Dispatcher,
    types,
)
from iacecil.controllers.persistence.zodb_orm import (
    get_aiogram_messages,
    get_aiogram_messages_texts,
    get_messages_texts_list,
)
from plugins.natural import (
    common_contexts_1,
    concordance_1,
    count_1,
    dispersion_plot_1,
    generate,
    similar_1,
)

async def get_telegram_texts(chat_id: str) -> list[str]:
    """Retorna todos textos de chat_id"""
    bot_id: str = Dispatcher.get_current().bot.id
    texts: list[str] = []
    try:
        logger.debug(f"Recuperando textos de {chat_id}")
        cursors: tuple[int, list[str]] = await get_aiogram_messages_texts(
            bot_id = bot_id,
            chat_id = chat_id,
            offset = 0,
            limit = None,
        )
        logger.debug(f"Encontrados {cursors[0]}")
        if cursors[0] > 0:
            texts: list[str] = cursors[1]
    except Exception as e:
        logger.exception(e)
    return texts

async def get_telegram_messages(chat_id: str) -> list[dict]:
    """Retorna todas mensagens de chat_id"""
    bot_id: str = Dispatcher.get_current().bot.id
    messages: list[dict] = []
    try:
        logger.debug(f"Recuperando mensagens de {chat_id}")
        cursors: tuple[int, list[dict]] = await get_aiogram_messages(
            bot_id = bot_id,
            chat_id = chat_id,
            offset = 0,
            limit = None,
        )
        logger.debug(f"Encontradas {cursors[0]}")
        if cursors[0] > 0:
            messages: list[dict] = cursors[1]
    except Exception as e:
        logger.exception(e)
    return messages

async def get_all_telegram_texts() -> list[list[str]]:
    """Retorna todos textos de todos chats"""
    bot_id: str = Dispatcher.get_current().bot.id
    texts: list[list[str]] = []
    try:
        for chat in glob.glob(f"instance/zodb/bots/{bot_id}/chats/*.fs"):
            cursors: list[dict] = await get_telegram_texts(
                chat.split('/')[-1].split('.')[0])
            if len(cursors) > 0:
                texts.append(cursors)
    except Exception as e:
        logger.exception(e)
    return texts

async def get_all_telegram_messages() -> list[list[dict]]:
    """Retorna todas mensagens de todos chats"""
    messages: list[list[dict]] = []
    try:
        for chat in glob.glob(f"instance/zodb/bots/{bot_id}/chats/*.fs"):
            cursors: list[dict] = await get_telegram_messages(
                chat.split('/')[-1].split('.')[0])
            if len(cursors) > 0:
                messages.append(cursors)
    except Exception as e:
        logger.exception(e)
    return messages

async def concordance_chat(chat_id: str, word: str) -> str:
    """NLTK text.concordance() (um chat)"""
    try:
        return await concordance_1(await get_telegram_texts(chat_id), word)
    except Exception as e:
        logger.exception(e)

async def concordance_all(word: str) -> str:
    """NLTK text.concordance() (todos chats)"""
    try:
        texts: list[str] = [
            text for texts in \
            await get_all_telegram_texts() \
            for text in texts
        ]
        concordances: str = await concordance_1(texts, word)
        return concordances
    except Exception as e:
        logger.exception(e)

async def similar_all(word: str) -> str:
    """NLTK text.similar() (todos chats)"""
    try:
        texts: list[str] = [
            text for texts in \
            await get_all_telegram_texts() \
            for text in texts
        ]
        similars: str = await similar_1(texts, word)
        return similars
    except Exception as e:
        logger.exception(e)

async def generate_all(word: str) -> str:
    """NLTK text.generate() (todos chats)"""
    try:
        texts: list[str] = [
            text for texts in \
            await get_all_telegram_texts() \
            for text in texts
        ]
        generated: str = await generate(texts)
        return generated
    except Exception as e:
        logger.exception(e)

async def context_all(word: str) -> str:
    """NLTK text.context() (todos chats)"""
    try:
        texts: list[str] = [
            text for texts in \
            await get_all_telegram_texts() \
            for text in texts
        ]
        contexts: str = await common_contexts_1(texts, word)
        return contexts
    except Exception as e:
        logger.exception(e)

async def count_all(word: str) -> dict:
    """Estatísticas: contagem (todos chats)"""
    try:
        texts: list[str] = [
            text for texts in \
            await get_all_telegram_texts() \
            for text in texts
        ]
        counted: str = await count_1(texts, word)
        return counted
    except Exception as e:
        logger.exception(e)

# ~ async def dispersion_all(word: str) -> object:
    # ~ """Estatísticas: dispersão léxica (todos chats)"""
    # ~ try:
        # ~ texts: list[str] = [
            # ~ text for texts in \
            # ~ await get_all_telegram_texts() \
            # ~ for text in texts
        # ~ ]
        # ~ dispersions: str = await dispersion_plot_1(texts, word)
        # ~ return dispersions
    # ~ except Exception as e:
        # ~ logger.exception(e)

async def statistics_all() -> str:
    """Estatísticas: várias estatísticas"""
    return "nada"
    # ~ dataframe_messages = [{
        # ~ 'date': message['date'],
        # ~ 'text': message.get('text', ''),
        # ~ 'message_id': message['message_id'],
        # ~ 'from_id': message['from']['id'],
        # ~ 'from_is_bot': message['from']['is_bot'],
        # ~ 'from_first_name': message['from']['first_name'],
        # ~ 'from_last_name': message['from'].get('last_name', ''),
        # ~ 'from_username': message['from'].get('username', ''),
        # ~ 'from_language_code': message['from'].get(
            # ~ 'language_code', ''),
        # ~ } for message in messages[1]]
    # ~ df = pandas.DataFrame(dataframe_messages)
    # ~ texts = [message.get('text', '') for message in messages[1]]
    # ~ words = await text_from_list(texts)
    # ~ series = pandas.Series(words)
    # ~ reply_text = f"""
# ~ Estatísticas para {message.chat.mention}:

# ~ Mensagens pesquisadas: últimas {len(messages[1])} de um total de \
# ~ {messages[0]}
# ~ Total de palavras: {len(words)}
# ~ Diversidade léxica (porcentagem de palavras únicas): \
# ~ {(len(set(words)) / len(words)):.2f}% ({len(set(words))} palavras única\
# ~ s)
# ~ Palavra mais usada: {words.vocab().most_common(1)[0][0]} (\
# ~ {words.vocab().most_common(1)[0][1]} vezes)
# ~ Pessoa que escreve mais: \
# ~ {df['from_first_name'].value_counts().idxmax()} \
# ~ ({len([message for message in dataframe_messages if 
# ~ message['from_first_name'] == df['from_first_name'
# ~ ].value_counts().idxmax()])} mensagens)
# ~ """
