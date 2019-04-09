#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file implements Vaultify Consumer classes
"""

import logging
import typing as t
import os
import json
from subprocess import run, PIPE  # nosec
from . import util

from .base import Consumer

__all__ = (
    'DotEnvWriter',
    'JsonWriter',
    'EnvRunner'
)

logger = logging.getLogger(__name__)


class DotEnvWriter(Consumer):
    """
    This Consumer will write secrets as a set of sourceable `export KEY=value`
    lines
    """
    def __init__(self, path: str = './secrets.env'):
        self.path = os.environ.get("VAULTIFY_DESTFILE", path)

    def consume_secrets(self, data: dict):
        """
        Write data as `export K=V` pairs into self.path, but die if self.path
        already exists.

        That file can be sourced or evaluated with the unix shell
        """
        if os.path.exists(self.path):
            raise RuntimeError(f'{self.path} already exists')

        with open(self.path, 'w') as secrets_file:
            logger.info(
                f"consuming {self}",
            )

            secrets_file.write(
                "\n".join(
                    util.dict2env(data)
                )
            )
            secrets_file.write('\n')


class JsonWriter(Consumer):
    """
    This Consumer will write secrets as a JSON dictionary
    """
    def __init__(self, path='./secrets.json'):
        self.path = os.environ.get("VAULTIFY_DESTFILE", path)

    def __str__(self):
        return f'{self.__class__}->{self.path}'

    def consume_secrets(self, data: dict):
        """
        Write data as json into fname
        That file can be evaluated by any json-aware application.
        """
        if os.path.exists(self.path):
            raise RuntimeError(f'{self.path} already exists')

        with open(self.path, 'w') as json_file:
            logger.info(
                "%s is writing to %s",
                self, self.path
            )

            json.dump(data, json_file, indent=2)
            json_file.write('\n')


class EnvRunner(Consumer):
    """
    This Consumer will update the environment and then run a subprocess in that
    altered environment.
    """
    def __init__(self, path: str = 'env'):
        self.path = os.environ.get(
            "VAULTIFY_TARGET", path
        ).split()

    def consume_secrets(self, data: dict):
        """
        This consumer does not write a file, but updates its own environment
        with the secret values and calls any subprocess inside that.
        """
        prepared_env = dict(os.environ)

        for key, value in data.items():
            prepared_env.update(
                {key: value}
            )
        logger.info(
            f'{self} enriched the environment')

        try:
            proc = run(
                self.path,
                stdout=PIPE,
                stderr=PIPE,
                env=prepared_env
            )
            logger.info(
                f'running the process "{self.path}"')

        except Exception as error:
            logger.critical(
                f'encountered error in {self} executing "{self.path}"')
            raise error

        print(
            proc.stdout.decode()
        )
