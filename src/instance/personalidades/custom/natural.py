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
    concordance_1,
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

async def concordance_chat(chat_id: str, word: str) -> object:
    """NLTK text.concordance() (um chat)"""
    try:
        return await concordance_1(await get_telegram_texts(chat_id), word)
    except Exception as e:
        logger.exception(e)

async def concordance_all(word: str) -> object:
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
