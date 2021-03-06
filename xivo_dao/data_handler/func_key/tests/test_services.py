# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

from mock import patch, Mock
from hamcrest import assert_that, equal_to

from xivo_dao.tests.test_case import TestCase
from xivo_dao.data_handler.func_key import services
from xivo_dao.data_handler.func_key.model import FuncKey


class TestFuncKeyService(TestCase):

    @patch('xivo_dao.data_handler.func_key.dao.search')
    def test_search(self, dao_search):
        search_result = dao_search.return_value = Mock()
        search = 'search'
        limit = 2
        skip = 1
        order = 'order'
        direction = 'desc'

        result = services.search(search=search, limit=limit, skip=skip, order=order, direction=direction)

        dao_search.assert_called_once_with(search=search, limit=limit, skip=skip, order=order, direction=direction)
        assert_that(result, equal_to(search_result))

    @patch('xivo_dao.data_handler.func_key.dao.get')
    def test_get(self, dao_get):
        func_key_id = 1
        func_key = dao_get.return_value = Mock(FuncKey)

        result = services.get(func_key_id)

        dao_get.assert_called_once_with(func_key_id)
        assert_that(result, equal_to(func_key))

    @patch('xivo_dao.data_handler.func_key.validator.validate_create')
    @patch('xivo_dao.data_handler.func_key.notifier.created')
    @patch('xivo_dao.data_handler.func_key.dao.create')
    def test_create(self, func_key_dao_create, func_key_notifier_created, validate_create):
        func_key = FuncKey(type='speeddial',
                           destination='user',
                           destination_id=1)

        func_key_dao_create.return_value = func_key

        result = services.create(func_key)

        self.assertEquals(type(result), FuncKey)
        validate_create.assert_called_once_with(func_key)
        func_key_dao_create.assert_called_once_with(func_key)
        func_key_notifier_created.assert_called_once_with(func_key)
