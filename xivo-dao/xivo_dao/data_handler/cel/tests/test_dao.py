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

import datetime
from hamcrest import assert_that, contains, has_property

from xivo_dao.alchemy.call_log import CallLog as CallLogSchema
from xivo_dao.alchemy.cel import CEL as CELSchema
from xivo_dao.data_handler.call_log.model import CallLog
from xivo_dao.data_handler.cel import dao as cel_dao
from xivo_dao.tests.test_dao import DAOTestCase


class TestCELDAO(DAOTestCase):

    tables = [
        CallLogSchema,
        CELSchema
    ]

    def setUp(self):
        self.empty_tables()

    def tearDown(self):
        pass

    def test_find_last_unprocessed_no_cels(self):
        limit = 10

        result = cel_dao.find_last_unprocessed(limit)

        assert_that(result, contains())

    def test_find_last_unprocessed_over_limit(self):
        limit = 2
        _, cel_id_2, cel_id_3 = self.add_cel(), self.add_cel(), self.add_cel()

        result = cel_dao.find_last_unprocessed(limit)

        assert_that(result, contains(has_property('id', cel_id_2),
                                     has_property('id', cel_id_3)))

    def test_find_last_unprocessed_under_limit(self):
        limit = 10
        cel_id_1, cel_id_2 = self.add_cel(), self.add_cel()

        result = cel_dao.find_last_unprocessed(limit)

        assert_that(result, contains(has_property('id', cel_id_1),
                                     has_property('id', cel_id_2)))

    def test_find_last_unprocessed_with_only_processed(self):
        limit = 10
        self._add_processed_cel()
        self._add_processed_cel()

        result = cel_dao.find_last_unprocessed(limit)

        assert_that(result, contains())

    def test_find_last_unprocessed_with_processed_and_unprocessed(self):
        limit = 10
        self._add_processed_cel()
        self._add_processed_cel()
        cel_id_3, cel_id_4 = self.add_cel(), self.add_cel()

        result = cel_dao.find_last_unprocessed(limit)

        assert_that(result, contains(has_property('id', cel_id_3),
                                     has_property('id', cel_id_4)))

    def _add_processed_cel(self):
        call_log_id = self._add_call()
        cel_id = self.add_cel()
        self._link_call_to_cel(call_log_id, cel_id)

    def _add_call(self, duration=datetime.timedelta(seconds=5)):
        call_log = CallLog(date=datetime.datetime.now(), duration=duration)
        call_log_row = call_log.to_data_source(CallLogSchema)
        self.add_me(call_log_row)
        return call_log_row.id

    def _link_call_to_cel(self, call_log_id, cel_id):
        self.session.begin()
        cel_row = self.session.query(CELSchema).get(cel_id)
        cel_row.call_log_id = call_log_id
        self.session.commit()
