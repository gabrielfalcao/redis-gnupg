#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

from .base import specification
from redisgpg import GPGRedis

@specification
def test_set(context):
    ("GPGRedis#set should encrypt value")

    context.redis.set("gabriel", "falcao")

    result = context.redis.get('gabriel')
    result.should_not.equal('falcao')
    context.redis.decrypt(result).should.equal('falcao')
