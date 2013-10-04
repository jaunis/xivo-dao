# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013 Avencall
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

import unittest

from hamcrest import *
from hamcrest.core import equal_to
from xivo_dao.helpers.abstract_model import AbstractModels
from xivo_dao.data_handler.exception import InvalidParametersError


class TestModel(AbstractModels):

    _RELATION = {}

    MANDATORY = [
        'field1'
    ]

    FIELDS = [
        'field1',
        'field2',
    ]


class TestModelsAbstract(unittest.TestCase):

    def test_instance_of_new_class(self):
        value1 = 'value1'
        value2 = 'value2'
        model = TestModel(field1=value1, field2=value2)

        assert_that(model, all_of(
            has_property('field1', value1),
            has_property('field2', value2)
        ))

    def test_equal_type_mismatch(self):
        model1 = TestModel(field1='a')
        astring = "a string"

        self.assertRaises(TypeError, lambda: model1 == astring)

    def test_equal_same(self):
        model1 = TestModel(field1='a', field2='b')
        model2 = TestModel(field1='a', field2='b')

        assert_that(model1, equal_to(model2))

    def test_not_equal(self):
        model1 = TestModel(field1='a', field2='a')
        model2 = TestModel(field1='a', field2='b')
        model3 = TestModel(field1='b', field2='b')

        self.assertNotEquals(model1, model2)
        self.assertNotEquals(model1, model3)
        self.assertNotEquals(model2, model3)

    def test_from_user_data(self):
        user_data = {
            'field1': 'value1',
            'field2': 'value2'
        }

        model1 = TestModel.from_user_data(user_data)

        assert_that(model1, all_of(
            has_property('field1', 'value1'),
            has_property('field2', 'value2')
        ))

    def test_to_user_data(self):
        model = TestModel(field1='value1')
        user_data = model.to_user_data()

        assert_that(user_data, has_entries({
            'field1': 'value1',
            'field2': None,
        }))

    def test_invalid_parameters(self):
        self.assertRaises(InvalidParametersError, TestModel, blabla='HOWDY')

    def test_missing_parameters(self):
        model = TestModel(field2='value2')
        missing = model.missing_parameters()

        assert_that(missing, has_length(1))
