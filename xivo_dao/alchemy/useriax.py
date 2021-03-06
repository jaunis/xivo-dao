# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint, \
    Index
from sqlalchemy.types import Integer, String, Text, Enum

from xivo_dao.helpers.db_manager import Base
from xivo_dao.alchemy import enum


class UserIAX(Base):

    __tablename__ = 'useriax'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('name'),
        Index('useriax__idx__category', 'category'),
        Index('useriax__idx__mailbox', 'mailbox'),
    )

    id = Column(Integer, nullable=False)
    name = Column(String(40), nullable=False)
    type = Column(Enum('friend', 'peer', 'user',
                       name='useriax_type',
                       metadata=Base.metadata),
                  nullable=False)
    username = Column(String(80))
    secret = Column(String(80), nullable=False, server_default='')
    dbsecret = Column(String(255), nullable=False, server_default='')
    context = Column(String(39))
    language = Column(String(20))
    accountcode = Column(String(20))
    amaflags = Column(Enum('default', 'omit', 'billing', 'documentation',
                           name='useriax_amaflags',
                           metadata=Base.metadata),
                      server_default='default')
    mailbox = Column(String(80))
    callerid = Column(String(160))
    fullname = Column(String(80))
    cid_number = Column(String(80))
    trunk = Column(Integer, nullable=False, server_default='0')
    auth = Column(Enum('plaintext', 'md5', 'rsa', 'plaintext,md5', 'plaintext,rsa', 'md5,rsa', 'plaintext,md5,rsa',
                       name='useriax_auth',
                       metadata=Base.metadata),
                  nullable=False, server_default='plaintext,md5')
    encryption = Column(Enum('no', 'yes', 'aes128',
                             name='useriax_encryption',
                             metadata=Base.metadata))
    forceencryption = Column(Enum('no', 'yes', 'aes128',
                                  name='useriax_encryption',
                                  metadata=Base.metadata))
    maxauthreq = Column(Integer)
    inkeys = Column(String(80))
    outkey = Column(String(80))
    adsi = Column(Integer)
    transfer = Column(Enum('no', 'yes', 'mediaonly',
                           name='useriax_transfer',
                           metadata=Base.metadata))
    codecpriority = Column(Enum('disabled', 'host', 'caller', 'reqonly',
                                name='useriax_codecpriority',
                                metadata=Base.metadata))
    jitterbuffer = Column(Integer)
    forcejitterbuffer = Column(Integer)
    sendani = Column(Integer, nullable=False, server_default='0')
    qualify = Column(String(4), nullable=False, server_default='no')
    qualifysmoothing = Column(Integer, nullable=False, server_default='0')
    qualifyfreqok = Column(Integer, nullable=False, server_default='60000')
    qualifyfreqnotok = Column(Integer, nullable=False, server_default='10000')
    timezone = Column(String(80))
    disallow = Column(String(100))
    allow = Column(Text)
    mohinterpret = Column(String(80))
    mohsuggest = Column(String(80))
    deny = Column(String(31))
    permit = Column(String(31))
    defaultip = Column(String(255))
    sourceaddress = Column(String(255))
    setvar = Column(String(100), nullable=False, server_default='')
    host = Column(String(255), nullable=False, server_default='dynamic')
    port = Column(Integer)
    mask = Column(String(15))
    regexten = Column(String(80))
    peercontext = Column(String(80))
    ipaddr = Column(String(255), nullable=False, server_default='')
    regseconds = Column(Integer, nullable=False, server_default='0')
    immediate = Column(Integer)
    keyrotate = Column(Integer)
    parkinglot = Column(Integer)
    protocol = Column(enum.trunk_protocol, nullable=False, server_default='iax')
    category = Column(Enum('user', 'trunk',
                           name='useriax_category',
                           metadata=Base.metadata),
                      nullable=False)
    commented = Column(Integer, nullable=False, server_default='0')
    requirecalltoken = Column(String(4), nullable=False, server_default='no')
