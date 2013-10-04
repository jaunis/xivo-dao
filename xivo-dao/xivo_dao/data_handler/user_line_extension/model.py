# -*- coding: utf-8 -*-

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

from xivo_dao.alchemy.user_line import UserLine as UserLineExtensionSchema
from xivo_dao.converters.database_converter import DatabaseConverter
from xivo_dao.helpers.abstract_model import AbstractModels


DB_TO_MODEL_MAPPING = {
    'id': 'id',
    'user_id': 'user_id',
    'line_id': 'line_id',
    'extension_id': 'extension_id',
    'main_user': 'main_user',
    'main_line': 'main_line'
}


class UserLineExtension(AbstractModels):

    MANDATORY = [
        'user_id',
        'line_id',
        'extension_id',
    ]

    FIELDS = [
        'id',
        'user_id',
        'line_id',
        'extension_id',
        'main_user',
        'main_line',
    ]

    _RELATION = {}


db_converter = DatabaseConverter(DB_TO_MODEL_MAPPING, UserLineExtensionSchema, UserLineExtension)
