#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
import os
import gnupg
from redis import StrictRedis

DEFAULT_GPG_HOME = os.path.expanduser('~/.ssh')


class GPGRedis(StrictRedis):
    def __init__(self, *args, **kw):
        self.gpg_home = kw.pop('gpg_home', DEFAULT_GPG_HOME)
        self.gpg_email = kw.pop('gpg_email', None)
        if not self.gpg_email:
            raise TypeError('Please pass the `gpg_email` attribute')

        self.gpg = gnupg.GPG(gnupghome=self.gpg_home)
        self.gpg.encoding = 'utf-8'
        self.key = self.ensure_key()
        super(GPGRedis, self).__init__(*args, **kw)

    def ensure_key(self):
        existing = self.gpg.search_keys(self.gpg_email)
        if not existing:
            ipt = self.gpg.gen_key_input(
                name_real='{0} Redis-GPG key'.format(self.gpg_email),
                name_email=self.gpg_email,
            )
            existing = [self.gpg.gen_key(ipt)]

        return existing[-1]

    def encrypt(self, value):
        return self.gpg.encrypt(value, self.key.fingerprint).data

    def decrypt(self, value):
        return self.gpg.decrypt(value).data

    def set(self, name, value):
        value = self.encrypt(value)
        return super(GPGRedis, self).set(name, value)
