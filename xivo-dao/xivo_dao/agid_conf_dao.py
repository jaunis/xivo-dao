# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Avencall
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


from xivo_dao.helpers.db_manager import daosession
from xivo_dao.alchemy.groupfeatures import GroupFeatures
from xivo_dao.alchemy.queue import Queue
from sqlalchemy.sql.expression import and_
from xivo_dao.alchemy.agent_login_status import AgentLoginStatus
from xivo_dao.alchemy.agentfeatures import AgentFeatures
from xivo_dao.alchemy.extension import Extension


@daosession
def get_group_settings(session, group_id):
    row = (session.query(GroupFeatures,
                         Queue.musicclass)
           .join(Queue, (GroupFeatures.name == Queue.name))
           .filter(and_(GroupFeatures.id == group_id,
                        GroupFeatures.deleted == 0,
                        Queue.category == 'group',
                        Queue.commented == 0))
           .first())

    if not row:
        raise LookupError("Unable to find group (id: %s)" % (group_id))

    group, musicclass = row
    res = {}
    res.update(group.todict())
    res['musicclass'] = musicclass

    return res


@daosession
def get_agent_device(session, agent_id):
    row = (session.query(AgentLoginStatus.state_interface)
           .filter(AgentLoginStatus.agent_id == int(agent_id))
           .first())

    if not row:
        raise LookupError("'Unable to find agent (id: %s)" % (agent_id))

    return row[0]


@daosession
def get_agent(session, agent_id):
    row = (session.query(AgentFeatures)
           .filter(AgentFeatures.id == int(agent_id))
           .first())

    if not row:
        raise LookupError("'Unable to find agent (id: %s)" % (agent_id))

    return row.todict()


@daosession
def get_agent_with_number(session, agent_number):
    row = (session.query(AgentFeatures)
           .filter(AgentFeatures.number == str(agent_number))
           .first())

    if not row:
        raise LookupError("'Unable to find agent (number: %s)" % (agent_number))

    return row.todict()


@daosession
def get_extensions_enabled_in(session, features):
    rows = (session.query(Extension.typeval)
            .filter(Extension.typeval.in_(features))
            .filter(Extension.commented == 0)
            .all())

    if not rows:
        raise LookupError("'Unable to find extensions in list (%s)" % ','.join(features))

    return [row[0] for row in rows]
