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

    print res

    return res
