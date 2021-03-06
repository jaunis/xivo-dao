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

from xivo_dao.data_handler.exception import ElementNotExistsError


class LineExtensionNotExistsError(ElementNotExistsError):

    @classmethod
    def from_line_id(cls, line_id):
        return cls('LineExtension', line_id=line_id)

    @classmethod
    def from_extension_id(cls, extension_id):
        return cls('LineExtension', extension_id=extension_id)
