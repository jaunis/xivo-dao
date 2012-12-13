# -*- coding: UTF-8 -*-

# XiVO CTI Server
# Copyright (C) 2009-2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Alternatively, XiVO CTI Server is available under other licenses directly
# contracted with Pro-formatique SARL. See the LICENSE file at top of the
# source tree or delivered in the installable package in which XiVO CTI Server
# is distributed for more details.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from xivo_dao.alchemy import dbconnection
from xivo_dao.alchemy.cel import CEL
from xivo_dao.helpers.cel_channel import CELChannel
from xivo_dao.helpers.cel_exception import CELException

logger = logging.getLogger(__name__)

_DB_NAME = 'asterisk'


def _session():
    connection = dbconnection.get_connection(_DB_NAME)
    return connection.get_session()


class UnsupportedLineProtocolException(Exception):
    pass


def caller_id_by_unique_id(unique_id):
    cel_events = (_session().query(CEL.cid_name, CEL.cid_num)
                  .filter(CEL.eventtype.in_(['APP_START', 'CHAN_START']))
                  .filter(CEL.uniqueid == unique_id)
                  .order_by(CEL.id.desc())
                  .first())

    if cel_events is None:
        raise CELException('no such CEL event with uniqueid %s' % unique_id)
    else:
        cid_name, cid_num = cel_events
        return '"%s" <%s>' % (cid_name, cid_num)


def channel_by_unique_id(unique_id):
    cel_events = (_session().query(CEL)
                  .filter(CEL.uniqueid == unique_id)
                  .all())
    if not cel_events:
        raise CELException('no such CEL event with uniqueid %s' % unique_id)
    else:
        return CELChannel(cel_events)


def channels_for_phone(phone, limit=None):
    channel_pattern = _channel_pattern_from_phone(phone)
    unique_ids = (_session().query(CEL.uniqueid)
                  .filter(CEL.channame.like(channel_pattern))
                  .filter(CEL.eventtype == 'CHAN_START')
                  .order_by(CEL.id.desc()))
    if limit is not None:
        fuzzy_limit = 2 * limit
        unique_ids = unique_ids.limit(fuzzy_limit)
    ret = []
    for unique_id, in unique_ids:
        try:
            channel = channel_by_unique_id(unique_id)
        except CELException as e:
            # this can happen in the case the channel is alive
            logger.info('could not create CEL channel %s: %s', unique_id, e)
        else:
            ret.append(channel)
    return ret


def _channel_pattern_from_phone(phone):
    protocol = phone['protocol']
    if protocol == 'sip':
        return _channel_pattern_from_phone_sip(phone)
    elif protocol == 'sccp':
        return _channel_pattern_from_phone_sccp(phone)
    else:
        raise UnsupportedLineProtocolException()


def _channel_pattern_from_phone_sip(phone):
    return "SIP/%s-%%" % phone['name']


def _channel_pattern_from_phone_sccp(phone):
    return "sccp/%s@%%" % phone['name']