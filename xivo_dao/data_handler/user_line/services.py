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

from xivo_dao.data_handler.user_line import validator, dao, notifier
from xivo_dao.data_handler.user_line_extension import services as ule_service


def get_by_user_id_and_line_id(user_id, line_id):
    return dao.get_by_user_id_and_line_id(user_id, line_id)


def find_all_by_user_id(user_id):
    return dao.find_all_by_user_id(user_id)


def find_all_by_line_id(line_id):
    return dao.find_all_by_line_id(line_id)


def associate(user_line):
    validator.validate_association(user_line)

    _adjust_optional_parameters(user_line)
    ule_service.associate_user_line(user_line)

    notifier.associated(user_line)
    return user_line


def dissociate(user_line):
    validator.validate_dissociation(user_line)
    ule_service.dissociate_user_line(user_line)
    notifier.dissociated(user_line)


def _adjust_optional_parameters(user_line):
    user_line_main_user = dao.find_main_user_line(user_line.line_id)
    if user_line_main_user is not None:
        user_line.main_user = (user_line.user_id == user_line_main_user.user_id)
