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

from hamcrest import *

from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.data_handler.exception import ElementNotExistsError, ElementCreationError
from xivo_dao.data_handler.user_line import dao as user_line_dao
from xivo_dao.data_handler.user_line.model import UserLine
from xivo_dao.tests.test_dao import DAOTestCase


class TestUserLineGetByUserIdAndLineId(DAOTestCase):

    def test_get_by_user_id_no_users_or_line(self):
        self.assertRaises(ElementNotExistsError, user_line_dao.get_by_user_id_and_line_id, 1, 1)

    def test_get_by_user_id_with_line(self):
        user_line = self.add_user_line_without_exten(firstname='King')

        result = user_line_dao.get_by_user_id_and_line_id(user_line.user_id, user_line.line_id)

        assert_that(result, instance_of(UserLine))
        assert_that(result,
                    has_property('user_id', user_line.user_id),
                    has_property('line_id', user_line.line_id)
                    )

    def test_get_by_user_id_with_line_and_secondary_user(self):
        main_user = self.add_user()
        secondary_user = self.add_user()
        line = self.add_line()
        main_user_line = self.add_user_line(user_id=main_user.id,
                                            line_id=line.id,
                                            main_user=True,
                                            main_line=False)
        self.add_user_line(user_id=secondary_user.id,
                           line_id=line.id,
                           main_user=False,
                           main_line=False)

        result = user_line_dao.get_by_user_id_and_line_id(main_user_line.user_id, main_user_line.line_id)

        assert_that(result, instance_of(UserLine))
        assert_that(result,
                    all_of(
                        has_property('user_id', main_user_line.user_id),
                        has_property('line_id', main_user_line.line_id),
                        has_property('main_user', True),
                        has_property('main_line', False)
                    )
                    )


class TestUserLineFindByUserIdAndLineId(DAOTestCase):

    def test_find_by_user_id_no_users_or_line(self):
        result = user_line_dao.find_by_user_id_and_line_id(1, 1)
        assert_that(result, none())

    def test_find_by_user_id_with_line(self):
        user_line = self.add_user_line_without_exten(firstname='King')

        result = user_line_dao.find_by_user_id_and_line_id(user_line.user_id, user_line.line_id)

        assert_that(result, instance_of(UserLine))
        assert_that(result,
                    has_property('user_id', user_line.user_id),
                    has_property('line_id', user_line.line_id)
                    )

    def test_find_by_user_id_with_line_and_secondary_user(self):
        main_user = self.add_user()
        secondary_user = self.add_user()
        line = self.add_line()
        main_user_line = self.add_user_line(user_id=main_user.id,
                                            line_id=line.id,
                                            main_user=True,
                                            main_line=False)
        self.add_user_line(user_id=secondary_user.id,
                           line_id=line.id,
                           main_user=False,
                           main_line=False)

        result = user_line_dao.find_by_user_id_and_line_id(main_user_line.user_id, main_user_line.line_id)

        assert_that(result, instance_of(UserLine))
        assert_that(result,
                    all_of(
                        has_property('user_id', main_user_line.user_id),
                        has_property('line_id', main_user_line.line_id),
                        has_property('main_user', True),
                        has_property('main_line', False)
                    )
                    )


class TestUserLineFindAllByUserId(DAOTestCase):

    def test_find_all_by_user_id_no_user_line(self):
        expected_result = []
        result = user_line_dao.find_all_by_user_id(1)

        assert_that(result, equal_to(expected_result))

    def test_find_all_by_user_id(self):
        user_line = self.add_user_line_without_exten()

        result = user_line_dao.find_all_by_user_id(user_line.user_id)

        assert_that(result, has_items(
            all_of(
                has_property('user_id', user_line.user_id),
                has_property('line_id', user_line.line_id))
        ))

    def test_find_all_by_user_id_two_users(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        self.add_user_line(user_id=user.id,
                           line_id=line1.id,
                           main_user=True,
                           main_line=True)
        self.add_user_line(user_id=user.id,
                           line_id=line2.id,
                           main_user=False,
                           main_line=True)

        result = user_line_dao.find_all_by_user_id(user.id)

        assert_that(result, has_items(
            all_of(
                has_property('user_id', user.id),
                has_property('line_id', line2.id)),
            all_of(
                has_property('user_id', user.id),
                has_property('line_id', line1.id))
        ))


class TestUserLineFindMainUserLine(DAOTestCase):

    def test_find_main_user_line_no_user(self):
        line_id = 33

        result = user_line_dao.find_main_user_line(line_id)

        assert_that(result, equal_to(None))

    def test_find_main_user_line_no_line(self):
        self.add_user()
        line_id = 2

        result = user_line_dao.find_main_user_line(line_id)

        assert_that(result, equal_to(None))

    def test_find_main_user_line_one_user(self):
        user_line = self.add_user_line_without_exten()

        result = user_line_dao.find_main_user_line(user_line.line_id)

        assert_that(result.user_id, equal_to(user_line.user_id))

    def test_find_main_user_line_one_line_no_user(self):
        user_line = self.add_user_line_without_user()

        result = user_line_dao.find_main_user_line(user_line.line_id)

        assert_that(result, none())

    def test_find_main_user_line(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        main_user_line = self.add_user_line(user_id=user.id,
                                            line_id=line1.id,
                                            main_user=True,
                                            main_line=True)
        self.add_user_line(user_id=user.id,
                           line_id=line2.id,
                           main_user=False,
                           main_line=True)

        result = user_line_dao.find_main_user_line(line1.id)

        assert_that(result, instance_of(UserLine))
        assert_that(result,
                    has_property('user_id', main_user_line.user_id),
                    has_property('line_id', main_user_line.line_id)
                    )


class TestAssociateUserLine(DAOTestCase):

    def test_associate_user_with_line(self):
        user = self.add_user()
        line = self.add_line()

        user_line = UserLine(user_id=user.id,
                             line_id=line.id)

        expected_user_line = user_line_dao.associate(user_line)

        result = (self.session.query(UserLineSchema)
                  .filter(UserLineSchema.id == expected_user_line.id)
                  .first())

        assert_that(result.user_id, equal_to(user_line.user_id))
        assert_that(result.line_id, equal_to(user_line.line_id))
        assert_that(result.extension_id, none())
        assert_that(result.main_user, equal_to(True))
        assert_that(result.main_line, equal_to(True))

    def test_associate_main_user_with_line(self):
        main_user = self.add_user()
        line = self.add_line()

        user_line = UserLine(user_id=main_user.id,
                             line_id=line.id,
                             main_user=True,
                             main_line=True)

        expected_user_line = user_line_dao.associate(user_line)

        result = (self.session.query(UserLineSchema)
                  .filter(UserLineSchema.id == expected_user_line.id)
                  .first())

        assert_that(result.user_id, equal_to(user_line.user_id))
        assert_that(result.line_id, equal_to(user_line.line_id))
        assert_that(result.extension_id, none())
        assert_that(result.main_user, equal_to(user_line.main_user))
        assert_that(result.main_line, equal_to(user_line.main_line))

    def test_associate_secondary_user_with_line(self):
        main_user = self.add_user()
        secondary_user = self.add_user()
        line = self.add_line()

        self.add_user_line(user_id=main_user.id,
                           line_id=line.id,
                           extension_id=None,
                           main_user=True,
                           main_line=True)

        secondary_user_line = UserLine(user_id=secondary_user.id,
                                       line_id=line.id,
                                       main_user=False,
                                       main_line=True)

        user_line_dao.associate(secondary_user_line)

        result = (self.session.query(UserLineSchema)
                  .filter(UserLineSchema.line_id == line.id)
                  .all())

        assert_that(result, contains_inanyorder(
            all_of(has_property('user_id', main_user.id),
                   has_property('line_id', line.id),
                   has_property('extension_id', None),
                   has_property('main_user', True),
                   has_property('main_line', True)),
            all_of(has_property('user_id', secondary_user.id),
                   has_property('line_id', line.id),
                   has_property('extension_id', None),
                   has_property('main_user', False),
                   has_property('main_line', True))))

    def test_associate_main_user_with_line_and_extension(self):
        user = self.add_user()
        line = self.add_line()
        extension = self.add_extension()
        user_line_row = self.add_user_line(line_id=line.id, extension_id=extension.id)

        user_line = UserLine(user_id=user.id,
                             line_id=line.id)

        user_line_dao.associate(user_line)

        result = self.session.query(UserLineSchema).filter(UserLineSchema.id == user_line_row.id).first()

        assert_that(result, all_of(
            has_property('user_id', user.id),
            has_property('line_id', line.id),
            has_property('extension_id', extension.id),
            has_property('main_user', True),
            has_property('main_line', True)))

    def test_associate_secondary_user_with_line_and_extension(self):
        main_user = self.add_user()
        secondary_user = self.add_user()
        line = self.add_line()
        extension = self.add_extension()

        main_user_line_row = self.add_user_line(user_id=main_user.id,
                                                line_id=line.id,
                                                extension_id=extension.id,
                                                main_user=True,
                                                main_line=True)

        user_line = UserLine(user_id=secondary_user.id,
                             line_id=line.id,
                             main_user=False)

        user_line_dao.associate(user_line)

        main_row = (self.session.query(UserLineSchema)
                    .filter(UserLineSchema.id == main_user_line_row.id)
                    .first())

        secondary_row = (self.session.query(UserLineSchema)
                         .filter(UserLineSchema.line_id == line.id)
                         .filter(UserLineSchema.user_id == secondary_user.id)
                         .first())

        assert_that(main_row, all_of(
            has_property('user_id', main_user.id),
            has_property('line_id', line.id),
            has_property('extension_id', extension.id),
            has_property('main_user', True),
            has_property('main_line', True)))

        assert_that(secondary_row, all_of(
            has_property('user_id', secondary_user.id),
            has_property('line_id', line.id),
            has_property('extension_id', extension.id),
            has_property('main_user', False),
            has_property('main_line', True)))

    def test_associate_user_with_line_not_exist(self):
        user = self.add_user()

        user_line = UserLine(user_id=user.id,
                             line_id=42)

        self.assertRaises(ElementCreationError, user_line_dao.associate, user_line)

    def test_associate_user_not_exist_with_line(self):
        line = self.add_line()

        user_line = UserLine(user_id=41,
                             line_id=line.id)

        self.assertRaises(ElementCreationError, user_line_dao.associate, user_line)

    def test_associate_user_not_exist_with_line_not_exist(self):
        user_line = UserLine(user_id=41,
                             line_id=12)

        self.assertRaises(ElementCreationError, user_line_dao.associate, user_line)


class TestDissociateUserLine(DAOTestCase):

    def test_dissociate_main_user_line_without_exten(self):
        user_line = self.add_user_line_without_exten()

        user_line_dao.dissociate(user_line)

        result = (self.session.query(UserLineSchema)
                  .filter(UserLineSchema.id == user_line.id)
                  .first())

        assert_that(result, none())

    def test_dissociate_main_user_line_with_exten(self):
        user_line = self.add_user_line_with_exten()

        user_line_dao.dissociate(user_line)

        result = (self.session.query(UserLineSchema)
                  .filter(UserLineSchema.id == user_line.id)
                  .first())

        assert_that(result.user_id, none())

    def test_dissociate_secondary_user_line(self):
        main_user_line = self.add_user_line_with_exten()
        secondary_user_line = self.prepare_secondary_user_line(main_user_line)

        user_line_dao.dissociate(secondary_user_line)

        self.assert_main_user_line_associated(main_user_line)
        self.assert_secondary_user_line_deleted(secondary_user_line)

    def prepare_secondary_user_line(self, main_user_line):
        user_row = self.add_user()
        self.add_user_line(user_id=user_row.id,
                           line_id=main_user_line.line_id,
                           extension_id=main_user_line.extension_id,
                           main_user=False,
                           main_line=True)

        return UserLine(user_id=user_row.id, line_id=main_user_line.id, main_user=False)

    def assert_main_user_line_associated(self, main_user_line):
        row = (self.session.query(UserLineSchema)
               .filter(UserLineSchema.user_id == main_user_line.user_id)
               .filter(UserLineSchema.line_id == main_user_line.line_id)
               .first())

        assert_that(row, is_not(none()))

    def assert_secondary_user_line_deleted(self, secondary_user_line):
        row = (self.session.query(UserLineSchema)
               .filter(UserLineSchema.user_id == secondary_user_line.user_id)
               .filter(UserLineSchema.line_id == secondary_user_line.line_id)
               .first())

        assert_that(row, none())


class TestLineHasSecondaryUser(DAOTestCase):

    def test_line_has_secondary_user(self):
        main_user = self.add_user()
        line = self.add_line()
        extension = self.add_extension()
        user_line = self.add_user_line(user_id=main_user.id,
                                       line_id=line.id,
                                       extension_id=extension.id,
                                       main_user=True,
                                       main_line=True)

        result = user_line_dao.line_has_secondary_user(user_line)

        assert_that(result, equal_to(False))

    def test_line_has_secondary_user_with_secondary_user(self):
        main_user = self.add_user()
        secondary_user = self.add_user()
        line = self.add_line()
        extension = self.add_extension()
        user_line = self.add_user_line(user_id=main_user.id,
                                       line_id=line.id,
                                       extension_id=extension.id,
                                       main_user=True,
                                       main_line=True)
        self.add_user_line(user_id=secondary_user.id,
                           line_id=line.id,
                           extension_id=extension.id,
                           main_user=False,
                           main_line=True)

        result = user_line_dao.line_has_secondary_user(user_line)

        assert_that(result, equal_to(True))


class TestUserLineFindAllByLineId(DAOTestCase):

    def test_find_all_by_line_id_no_user_line(self):
        result = user_line_dao.find_all_by_line_id(1)

        assert_that(result, has_length(0))

    def test_find_all_by_line_id_one_user_line_with_exten(self):
        user_line_row = self.add_user_line_with_exten()
        user_line = self.prepare_user_line(user_line_row)

        result = user_line_dao.find_all_by_line_id(user_line_row.line_id)

        assert_that(result, contains(user_line))

    def test_find_all_by_line_id_one_user_line_without_exten(self):
        user_line_row = self.add_user_line_without_exten()
        user_line = self.prepare_user_line(user_line_row)

        result = user_line_dao.find_all_by_line_id(user_line_row.line_id)

        assert_that(result, contains(user_line))

    def test_find_all_by_line_id_two_user_lines(self):
        user_line_row_1 = self.add_user_line_with_exten()
        user_row = self.add_user()
        user_line_row_2 = self.add_user_line(user_id=user_row.id,
                                             line_id=user_line_row_1.line_id,
                                             main_user=False,
                                             main_line=True)

        user_line_1 = self.prepare_user_line(user_line_row_1)
        user_line_2 = self.prepare_user_line(user_line_row_2)

        result = user_line_dao.find_all_by_line_id(user_line_row_1.line_id)

        assert_that(result, contains_inanyorder(user_line_1, user_line_2))

    def test_find_all_by_line_id_with_line_no_user(self):
        user_line_row = self.add_user_line_without_user()

        result = user_line_dao.find_all_by_line_id(user_line_row.line_id)

        assert_that(result, contains())

    def prepare_user_line(self, user_line_row):
        return UserLine(user_id=user_line_row.user_id,
                        line_id=user_line_row.line_id,
                        main_user=user_line_row.main_user,
                        main_line=user_line_row.main_line)
