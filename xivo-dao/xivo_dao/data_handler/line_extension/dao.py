# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from xivo_dao.helpers.db_manager import daosession
from xivo_dao.alchemy.user_line import UserLine
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_dao.data_handler.line_extension.exception import LineExtensionNotExistsError
from xivo_dao.data_handler.line_extension.model import db_converter


@daosession
def associate(session, line_extension):
    session.begin()
    _update_ule(session, line_extension)
    session.commit()


def _update_ule(session, line_extension):
    (session.query(UserLine)
     .filter(UserLine.line_id == line_extension.line_id)
     .update({'extension_id': line_extension.extension_id}))


@daosession
def get_by_line_id(session, line_id):
    user_line_row = (session.query(UserLine)
                     .filter(UserLine.line_id == line_id)
                     .first())

    if not user_line_row:
        raise ElementNotExistsError('Line', id=line_id)

    if not user_line_row.extension_id:
        raise LineExtensionNotExistsError.from_line_id(line_id)

    return db_converter.to_model(user_line_row)
