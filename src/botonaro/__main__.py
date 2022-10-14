"""
Botonaro  

Copyright 2022 Iuri Guilherme <https://iuri.neocities.org/>  

Creative Commons 4.0 Attribution Share Alike  
"""
import logging, sys
logging.basicConfig(level = "DEBUG")
logger = logging.getLogger(__name__)
try:
    from iacecil.controllers._iacecil import production
except Exception as e:
    logger.exception(e)
    sys.exit("Talquei")

