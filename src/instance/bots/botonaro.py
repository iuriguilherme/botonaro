"""t.me/botonarobot"""

import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from iacecil.config import DefaultBotConfig

default_config = DefaultBotConfig()
load_dotenv()

class BotConfig(BaseSettings):
    coinmarketcap: dict = default_config.coinmarketcap
    discord: dict = default_config.discord
    donate: dict = default_config.donate
    furhat: dict = default_config.furhat
    info: dict = default_config.info
    jobs: list = default_config.jobs
    quart: dict = default_config.quart
    serpapi: dict = default_config.serpapi
    tecido: dict = default_config.tecido
    timezone: str = default_config.timezone
    tropixel: dict = default_config.tropixel
    web3: dict = default_config.web3

    personalidade: str = 'custom'
    plugins: dict = dict(
        enable = [
            'admin',
        ], # enable
        disable = [
            'default',
            'archive',
            'cryptoforex',
            'donate',
            'feedback',
            'hashes',
            'mate_matica',
            'qr',
            'storify',
            'tropixel',
            'tts',
            'web3_wrapper',
            'ytdl',
            'natural',
            'welcome',
            'garimpo',
            'echo',
            'greatful',
            'portaria',
            'totalvoice',
        ], # disable
    ) # plugins
    telegram: dict = dict(
        default_config.telegram.copy(),
        token = os.environ.get(
            'TELEGRAM_TOKEN',
            default_config.telegram.get('token'),
        ), # token
        users = dict(
            default_config.telegram.get('users', {}).copy(),
            alpha = os.environ.get(
                'ADMIN_CHAT',
                default_config.telegram.get(
                    'users',
                    {'alpha': []},
                ).get(
                    'alpha',
                    [],
                ),
            ), # alpha
            special = dict(
                default_config.telegram.get(
                    'users',
                    {'special': {}},
                ).get(
                    'special',
                    {},
                ).copy(),
                debug = os.environ.get(
                    'DEBUG_CHAT',
                    default_config.telegram.get(
                        'users',
                        {'special': {'debug': 0}},
                    ).get(
                        'special',
                        {'debug': 0},
                    ).get(
                        'debug',
                        0,
                    ),
                ), # debug
                info = os.environ.get(
                    'DEBUG_CHAT',
                    default_config.telegram.get(
                        'users',
                        {'special': {'info': 0}},
                    ).get(
                        'special',
                        {'info': 0},
                    ).get(
                        'info',
                        0,
                    ),
                ), # info
                # ~ feedback = dict(
                # ~ ), # feedback
            ), # special
        ), # users
    ) # telegram
