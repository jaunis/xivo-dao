# -*- coding: utf-8 -*-

import unittest

from mock import patch, Mock

from xivo_dao.data_handler.line.model import LineSIP, LineOrdering
from xivo_dao.data_handler.line import services as line_services
from xivo_dao.data_handler.exception import MissingParametersError, \
    ElementCreationError, ElementNotExistsError, InvalidParametersError, \
    ElementEditionError
from xivo_dao.data_handler.device.model import Device
from xivo_dao.data_handler.user.model import User


class TestLineServices(unittest.TestCase):

    @patch('xivo_dao.data_handler.line.dao.get')
    def test_get(self, mock_line_get):
        line_id = 1

        line = Mock()
        mock_line_get.return_value = line

        result = line_services.get(line_id)

        mock_line_get.assert_called_once_with(line_id)
        self.assertEquals(result, line)

    @patch('xivo_dao.data_handler.line.dao.get')
    def test_get_not_exist(self, mock_line_get):
        mock_line_get.side_effect = ElementNotExistsError('Line')

        self.assertRaises(ElementNotExistsError, line_services.get, 1)

    @patch('xivo_dao.data_handler.line.dao.get_by_user_id')
    def test_get_by_user_id(self, mock_get_by_user_id):
        user_id = 1

        line = Mock()
        mock_get_by_user_id.return_value = line

        result = line_services.get_by_user_id(user_id)

        mock_get_by_user_id.assert_called_once_with(user_id)
        self.assertEquals(result, line)

    @patch('xivo_dao.data_handler.line.dao.get_by_user_id')
    def test_get_by_user_id_not_exist(self, mock_get_by_user_id):
        mock_get_by_user_id.side_effect = ElementNotExistsError('Line')

        self.assertRaises(ElementNotExistsError, line_services.get_by_user_id, 1)

    @patch('xivo_dao.data_handler.line.dao.get_by_number_context')
    def test_get_by_number_context(self, mock_get_by_number_context):
        number = '1000'
        context = 'default'

        line = Mock()
        mock_get_by_number_context.return_value = line

        result = line_services.get_by_number_context(number, context)

        mock_get_by_number_context.assert_called_once_with(number, context)
        self.assertEquals(result, line)

    @patch('xivo_dao.data_handler.line.dao.get_by_number_context')
    def test_get_by_number_context_not_exist(self, mock_get_by_number_context):
        mock_get_by_number_context.side_effect = ElementNotExistsError('Line')

        self.assertRaises(ElementNotExistsError, line_services.get_by_number_context, '1000', 'default')

    @patch('xivo_dao.data_handler.line.dao.find_all')
    def test_find_all(self, line_dao_find_all):
        first_line = Mock(LineSIP)
        second_line = Mock(LineSIP)
        expected_order = None

        expected = [first_line, second_line]

        line_dao_find_all.return_value = expected

        result = line_services.find_all()

        self.assertEquals(result, expected)

        line_dao_find_all.assert_called_once_with(order=expected_order)

    @patch('xivo_dao.data_handler.line.dao.find_all')
    def test_find_all_order_by_name(self, line_dao_find_all):
        first_line = Mock(LineSIP)
        second_line = Mock(LineSIP)
        expected_order = [LineOrdering.name]

        expected = [first_line, second_line]

        line_dao_find_all.return_value = expected

        result = line_services.find_all(order=[LineOrdering.name])

        self.assertEquals(result, expected)

        line_dao_find_all.assert_called_once_with(order=expected_order)

    @patch('xivo_dao.data_handler.line.dao.find_all_by_name')
    def test_find_all_by_name(self, line_dao_find_all_by_name):
        expected_result = [Mock(LineSIP)]
        name = 'Lord'

        line_dao_find_all_by_name.return_value = expected_result

        result = line_services.find_all_by_name(name)

        self.assertEquals(result, expected_result)
        line_dao_find_all_by_name.assert_called_once_with(name)

    @patch('xivo_dao.data_handler.line.dao.find_all_by_name')
    def test_find_all_by_name_no_result(self, line_dao_find_all_by_name):
        expected_result = []
        name = 'Lord'

        line_dao_find_all_by_name.return_value = expected_result

        result = line_services.find_all_by_name(name)

        self.assertEquals(result, expected_result)
        line_dao_find_all_by_name.assert_called_once_with(name)

    @patch('xivo_dao.data_handler.line.dao.find_all_by_device_id')
    def test_find_all_by_device_id(self, line_dao_find_all_by_device_id):
        expected_result = [Mock(LineSIP)]
        device_id = '222'

        line_dao_find_all_by_device_id.return_value = expected_result

        result = line_services.find_all_by_device_id(device_id)

        self.assertEquals(result, expected_result)
        line_dao_find_all_by_device_id.assert_called_once_with(device_id)

    @patch('xivo_dao.data_handler.line.dao.find_all_by_device_id')
    def test_find_all_by_device_id_no_result(self, line_dao_find_all_by_device_id):
        expected_result = []
        device_id = '222'

        line_dao_find_all_by_device_id.return_value = expected_result

        result = line_services.find_all_by_device_id(device_id)

        self.assertEquals(result, expected_result)
        line_dao_find_all_by_device_id.assert_called_once_with(device_id)

    @patch('xivo_dao.data_handler.line.dao.provisioning_id_exists')
    def test_make_provisioning_id(self, provd_id_exists):
        provd_id_exists.return_value = False

        provd_id = line_services.make_provisioning_id()

        self.assertEquals(len(str(provd_id)), 6)
        self.assertEquals(str(provd_id).startswith('0'), False)

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.notifier.created')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create(self, line_dao_create, line_notifier_created, make_provisioning_id):
        name = 'line'
        context = 'toto'
        secret = '1234'

        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device_slot=1)

        line_dao_create.return_value = line

        result = line_services.create(line)

        line_dao_create.assert_called_once_with(line)
        line_notifier_created.assert_called_once_with(line)
        make_provisioning_id.assert_called_with()
        self.assertEquals(type(result), LineSIP)

    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create_with_missing_attributes(self, line_dao_create, make_provisioning_id):
        line = LineSIP(name='lpko')

        self.assertRaises(MissingParametersError, line_services.create, line)
        self.assertEquals(make_provisioning_id.call_count, 0)

    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create_with_empty_attributes(self, line_dao_create, make_provisioning_id):
        line1 = LineSIP(context='',
                       device_slot=1)

        line2 = LineSIP(context='default',
                       device_slot='')

        self.assertRaises(InvalidParametersError, line_services.create, line1)
        self.assertRaises(InvalidParametersError, line_services.create, line2)
        self.assertEquals(make_provisioning_id.call_count, 0)

    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create_with_invalid_attributes(self, line_dao_create, make_provisioning_id):
        line1 = LineSIP(context='default',
                       device_slot=0)

        line2 = LineSIP(context='default',
                       device_slot=-1)

        line3 = LineSIP(context='default',
                       device_slot='abcd')

        self.assertRaises(InvalidParametersError, line_services.create, line1)
        self.assertRaises(InvalidParametersError, line_services.create, line2)
        self.assertRaises(InvalidParametersError, line_services.create, line3)
        self.assertEquals(make_provisioning_id.call_count, 0)

    @patch('xivo_dao.data_handler.context.services.find_by_name')
    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create_with_inexisting_context(self, line_dao_create, make_provisioning_id, find_context_by_name):
        line = LineSIP(context='superdupercontext',
                       device_slot=1)
        find_context_by_name.return_value = None

        self.assertRaises(InvalidParametersError, line_services.create, line)
        self.assertEquals(make_provisioning_id.call_count, 0)

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.line.services.make_provisioning_id')
    @patch('xivo_dao.data_handler.line.dao.create')
    def test_create_with_error_from_dao(self, line_dao_create, make_provisioning_id):
        name = 'line'
        context = 'toto'
        secret = '1234'

        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device_slot=1)

        error = Exception("message")
        line_dao_create.side_effect = ElementCreationError(error, '')

        self.assertRaises(ElementCreationError, line_services.create, line)
        make_provisioning_id.assert_called_with()

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.device.services.rebuild_device_config')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.edited')
    @patch('xivo_dao.data_handler.line.dao.edit')
    def test_edit(self,
                  line_dao_edit,
                  line_notifier_edited,
                  device_dao_find,
                  device_services_rebuild_device_config):
        name = 'line'
        context = 'toto'
        secret = '1234'
        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device_slot=1)

        line_services.edit(line)

        line_dao_edit.assert_called_once_with(line)
        self.assertEquals(device_dao_find.call_count, 0)
        self.assertEquals(device_services_rebuild_device_config.call_count, 0)
        line_notifier_edited.assert_called_once_with(line)

    @patch('xivo_dao.data_handler.device.services.rebuild_device_config')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.edited')
    @patch('xivo_dao.data_handler.line.dao.edit')
    def test_edit_with_empty_attributes(self,
                                        line_dao_edit,
                                        line_notifier_edited,
                                        device_services_get,
                                        device_services_rebuild_device_config):
        line = LineSIP(context='',
                       device_slot=1)

        self.assertRaises(InvalidParametersError, line_services.edit, line)
        self.assertEquals(line_dao_edit.call_count, 0)
        self.assertEquals(device_services_get.call_count, 0)
        self.assertEquals(device_services_rebuild_device_config.call_count, 0)
        self.assertEquals(line_notifier_edited.call_count, 0)

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.device.services.rebuild_device_config')
    @patch('xivo_dao.data_handler.device.services.get')
    @patch('xivo_dao.data_handler.line.notifier.edited')
    @patch('xivo_dao.data_handler.line.dao.edit')
    def test_edit_with_error_from_dao(self,
                                      line_dao_edit,
                                      line_notifier_edited,
                                      device_dao_find,
                                      device_services_rebuild_device_config):
        name = 'line'
        context = 'toto'
        secret = '1234'

        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device_slot=1)

        error = Exception("message")
        line_dao_edit.side_effect = ElementEditionError(error, '')

        self.assertRaises(ElementEditionError, line_services.edit, line)
        self.assertEquals(device_dao_find.call_count, 0)
        self.assertEquals(device_services_rebuild_device_config.call_count, 0)
        self.assertEquals(line_notifier_edited.call_count, 0)

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.device.services.rebuild_device_config')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.edited')
    @patch('xivo_dao.data_handler.line.dao.edit')
    def test_edit_with_a_device_associated(self,
                                           line_dao_edit,
                                           line_notifier_edited,
                                           device_dao_find,
                                           device_services_rebuild_device_config):
        name = 'line'
        context = 'toto'
        secret = '1234'
        device_id = '2'
        device = Device(id=device_id)
        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device=device_id,
                       device_slot=1)

        device_dao_find.return_value = device

        line_services.edit(line)

        line_dao_edit.assert_called_once_with(line)
        line_notifier_edited.assert_called_once_with(line)
        device_dao_find.assert_called_once_with(device_id)
        device_services_rebuild_device_config.assert_called_once_with(device)

    @patch('xivo_dao.data_handler.context.services.find_by_name', Mock(return_value=Mock()))
    @patch('xivo_dao.data_handler.device.services.rebuild_device_config')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.edited')
    @patch('xivo_dao.data_handler.line.dao.edit')
    def test_edit_with_a_device_associated_but_not_found(self,
                                                         line_dao_edit,
                                                         line_notifier_edited,
                                                         device_dao_find,
                                                         device_services_rebuild_device_config):
        name = 'line'
        context = 'toto'
        secret = '1234'
        device_id = '2'
        line = LineSIP(name=name,
                       context=context,
                       username=name,
                       secret=secret,
                       device=device_id,
                       device_slot=1)

        device_dao_find.return_value = None

        line_services.edit(line)

        line_dao_edit.assert_called_once_with(line)
        line_notifier_edited.assert_called_once_with(line)
        device_dao_find.assert_called_once_with(device_id)
        self.assertEquals(device_services_rebuild_device_config.call_count, 0)

    @patch('xivo_dao.data_handler.device.services.remove_line_from_device')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.deleted')
    @patch('xivo_dao.data_handler.line.dao.delete')
    def test_delete(self,
                    line_dao_delete,
                    line_notifier_deleted,
                    device_dao_find,
                    remove_line_from_device):
        line_id = 1
        username = 'line'
        secret = 'toto'

        line = LineSIP(id=line_id, username=username, secret=secret)

        line_services.delete(line)

        line_dao_delete.assert_called_once_with(line)
        line_notifier_deleted.assert_called_once_with(line)
        self.assertEquals(device_dao_find.call_count, 0)
        self.assertEquals(remove_line_from_device.call_count, 0)

    @patch('xivo_dao.data_handler.device.services.remove_line_from_device')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.deleted')
    @patch('xivo_dao.data_handler.line.dao.delete')
    def test_delete_with_device(self,
                                line_dao_delete,
                                line_notifier_deleted,
                                device_dao_find,
                                remove_line_from_device):
        line_id = 1
        username = 'line'
        secret = 'toto'
        device_id = 15
        device_slot = 1

        line = LineSIP(id=line_id, username=username, secret=secret, device=device_id, device_slot=device_slot)
        device = device_dao_find.return_value = Mock()

        line_services.delete(line)

        line_dao_delete.assert_called_once_with(line)
        device_dao_find.assert_called_once_with(line.device)
        remove_line_from_device.assert_called_once_with(device, line)
        line_notifier_deleted.assert_called_once_with(line)

    @patch('xivo_dao.data_handler.device.services.remove_line_from_device')
    @patch('xivo_dao.data_handler.device.dao.find')
    @patch('xivo_dao.data_handler.line.notifier.deleted')
    @patch('xivo_dao.data_handler.line.dao.delete')
    def test_delete_with_device_not_found(self,
                                          line_dao_delete,
                                          line_notifier_deleted,
                                          device_dao_find,
                                          remove_line_from_device):
        line_id = 1
        username = 'line'
        secret = 'toto'
        device_id = 15
        device_slot = 1

        line = LineSIP(id=line_id, username=username, secret=secret, device=device_id, device_slot=device_slot)
        device_dao_find.return_value = None

        line_services.delete(line)

        line_dao_delete.assert_called_once_with(line)
        device_dao_find.assert_called_once_with(line.device)
        self.assertEquals(remove_line_from_device.call_count, 0)
        line_notifier_deleted.assert_called_once_with(line)

    @patch('xivo_dao.data_handler.line.services.edit')
    @patch('xivo_dao.data_handler.line.dao.find_by_user_id')
    def test_update_callerid(self, line_dao_find_by_user_id, line_services_edit):
        expected_callerid = 'titi'
        user = User(id=1,
                    firstname='titi',
                    callerid=expected_callerid)
        line = LineSIP(callerid=expected_callerid,
                       number='1000',
                       name='toto')

        line_dao_find_by_user_id.return_value = line

        line_services.update_callerid(user)

        line_dao_find_by_user_id.assert_called_once_with(user.id)
        line_services_edit.assert_called_once_with(line)

    @patch('xivo_dao.data_handler.line.services.edit')
    @patch('xivo_dao.data_handler.line.dao.find_by_user_id')
    def test_update_callerid_with_no_line(self, line_dao_find_by_user_id, line_services_edit):
        expected_callerid = 'titi'
        user = User(id=1,
                    firstname='titi',
                    callerid=expected_callerid)

        line_dao_find_by_user_id.return_value = None

        line_services.update_callerid(user)

        line_dao_find_by_user_id.assert_called_once_with(user.id)
        self.assertEquals(line_services_edit.call_count, 0)
