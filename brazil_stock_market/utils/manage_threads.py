#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import threading
from ..utils import logging


def create_threads(thread_id, args, method_target):

    t = threading.Thread(name=thread_id, target=method_target, args=args)
    logging.debug('{} created!!'.format(t.name))
    return t
