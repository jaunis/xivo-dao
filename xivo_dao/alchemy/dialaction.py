# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Enum

from xivo_dao.helpers.db_manager import Base


class Dialaction(Base):
    __tablename__ = 'dialaction'

    event = Column(Enum('answer',
                        'noanswer',
                        'congestion',
                        'busy',
                        'chanunavail',
                        'inschedule',
                        'outschedule',
                        'qwaittime',
                        'qwaitratio',
                        name='dialaction_event',
                        metadata=Base.metadata),
                   primary_key=True)
    category = Column(Enum('callfilter',
                           'group',
                           'incall',
                           'queue',
                           'schedule',
                           'user',
                           'outcall',
                           name='dialaction_category',
                           metadata=Base.metadata),
                      primary_key=True)
    categoryval = Column(String(128), server_default='', primary_key=True)
    action = Column(Enum('none',
                         'endcall:busy',
                         'endcall:congestion',
                         'endcall:hangup',
                         'user',
                         'group',
                         'queue',
                         'meetme',
                         'voicemail',
                         'trunk',
                         'schedule',
                         'voicemenu',
                         'extension',
                         'outcall',
                         'application:callbackdisa',
                         'application:disa',
                         'application:directory',
                         'application:faxtomail',
                         'application:voicemailmain',
                         'application:password',
                         'sound',
                         'custom',
                         name='dialaction_action',
                         metadata=Base.metadata),
                    nullable=False)
    actionarg1 = Column(String(255), nullable=True)
    actionarg2 = Column(String(255), nullable=True)
    linked = Column(Integer, nullable=False, server_default='0')