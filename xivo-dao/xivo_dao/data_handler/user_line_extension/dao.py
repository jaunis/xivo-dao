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

from xivo_dao.alchemy.user_line import UserLine as ULESchema
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.data_handler.exception import ElementNotExistsError, \
    ElementCreationError, ElementDeletionError, ElementEditionError
from sqlalchemy.exc import SQLAlchemyError
from model import db_converter
from xivo_dao.data_handler.user import dao as user_dao


@daosession
def get(session, ule_id):
    ule_row = _get_ule_row(session, ule_id)

    return db_converter.to_model(ule_row)


def _get_ule_row(session, ule_id):
    ule_row = session.query(ULESchema).filter(ULESchema.id == ule_id).first()

    if not ule_row:
        raise ElementNotExistsError('UserLineExtension', id=ule_id)

    return ule_row


@daosession
def find_all(session):
    res = session.query(ULESchema).all()
    if not res:
        return []

    tmp = []
    for ule in res:
        tmp.append(db_converter.to_model(ule))

    return tmp


@daosession
def find_all_by_user_id(session, user_id):
    ules = session.query(ULESchema).filter(ULESchema.user_id == user_id).all()
    return [db_converter.to_model(ule) for ule in ules]


@daosession
def find_all_by_extension_id(session, extension_id):
    ules = session.query(ULESchema).filter(ULESchema.extension_id == extension_id).all()
    return [db_converter.to_model(ule) for ule in ules]


@daosession
def find_all_by_line_id(session, line_id):
    ules = session.query(ULESchema).filter(ULESchema.line_id == line_id).all()
    return [db_converter.to_model(ule) for ule in ules]


@daosession
def find_main_user(session, ule):
    row = (session.query(ULESchema.user_id)
           .filter(ULESchema.main_user == True)
           .filter(ULESchema.line_id == ule.line_id)
           .first())

    if not row:
        return user_dao.get(ule.user_id)

    return user_dao.get(row[0])


@daosession
def create(session, user_line_extension):
    user_line_extension_row = db_converter.to_source(user_line_extension)
    session.begin()
    session.add(user_line_extension_row)

    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise ElementCreationError('UserLineExtension', e)

    user_line_extension.id = user_line_extension_row.id

    return user_line_extension


@daosession
def edit(session, user_line_extension):
    ule_row = _get_ule_row(session, user_line_extension.id)
    db_converter.update_source(ule_row, user_line_extension)

    session.begin()
    session.add(ule_row)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise ElementEditionError('UserLineExtension', e)


@daosession
def delete(session, user_line_extension):
    session.begin()
    try:
        nb_row_affected = session.query(ULESchema).filter(ULESchema.id == user_line_extension.id).delete()
        session.commit()
    except SQLAlchemyError, e:
        session.rollback()
        raise ElementDeletionError('UserLineExtension', e)

    if nb_row_affected == 0:
        raise ElementDeletionError('UserLineExtension', 'user_line_extension_id %s not exsit' % user_line_extension.id)

    return nb_row_affected


@daosession
def already_linked(session, user_id, line_id):
    count = (session.query(ULESchema)
             .filter(ULESchema.user_id == user_id)
             .filter(ULESchema.line_id == line_id)
             .count())

    return count > 0


@daosession
def main_user_is_allowed_to_delete(session, main_line_id):
    count = (session.query(ULESchema)
             .filter(ULESchema.line_id == main_line_id)
             .count())

    return count == 1
