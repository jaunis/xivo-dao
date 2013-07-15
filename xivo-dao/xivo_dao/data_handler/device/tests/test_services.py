# -*- coding: UTF-8 -*-

import unittest
from xivo_dao.data_handler.device.services import remove_line_from_device
from mock import patch


class Test(unittest.TestCase):

    def setUp(self):
        self.deviceid = "ad0a12fd5f244ae68a3c626789203698"

    @patch('xivo_dao.helpers.provd_connector.config_manager')
    @patch('xivo_dao.helpers.provd_connector.device_manager')
    def test_remove_line_from_device(self, device_manager, config_manager):
        config_dict = {
            "raw_config": {
                "sip_lines": {
                    "1": {"username": "1234"},
                    "2": {"username": "5678"}
                },
                "funckeys": {}
            }
        }
        config_manager.get.return_value = config_dict

        expected_arg = {
            "raw_config": {
                "sip_lines": {
                    "1": {"username": "1234"}
                },
                "funckeys": {}
            }
        }

        remove_line_from_device(self.deviceid, 2)

        config_manager.get.assert_called_with(self.deviceid)
        config_manager.update.assert_called_with(expected_arg)
        self.assertEquals(0, config_manager.autocreate.call_count)

    @patch('xivo_dao.helpers.provd_connector.config_manager')
    @patch('xivo_dao.helpers.provd_connector.device_manager')
    def test_remove_line_from_device_autoprov(self, device_manager, config_manager):
        autoprovid = "autoprov1234"
        config_dict = {
            "raw_config": {
                "sip_lines": {
                    "1": {"username": "1234"}
                },
                "funckeys": {}
            }
        }

        device_dict = {"ip": "10.60.0.109",
                       "version": "3.2.2.1136",
                       "config": self.deviceid,
                       "id": self.deviceid}
        config_manager.get.return_value = config_dict
        device_manager.get.return_value = device_dict
        config_manager.autocreate.return_value = autoprovid

        expected_arg_config = {"raw_config": {}}
        expected_arg_device = {"ip": "10.60.0.109",
                               "version": "3.2.2.1136",
                               "config": autoprovid,
                               "id": self.deviceid}
        remove_line_from_device(self.deviceid, 1)

        config_manager.get.assert_called_with(self.deviceid)
        config_manager.autocreate.assert_called_with()
        device_manager.get.assert_called_with(self.deviceid)
        device_manager.update.assert_called_with(expected_arg_device)
        config_manager.update.assert_called_with(expected_arg_config)

    @patch('xivo_dao.helpers.provd_connector.config_manager')
    @patch('xivo_dao.helpers.provd_connector.device_manager')
    def test_remove_line_from_device_no_funckeys(self, device_manager, config_manager):
        autoprovid = "autoprov1234"
        config_dict = {
            "raw_config": {
                "sip_lines": {
                    "1": {"username": "1234"}
                },
                "funckeys": {}
            }
        }
        device_dict = {"ip": "10.60.0.109",
                       "version": "3.2.2.1136",
                       "config": self.deviceid,
                       "id": self.deviceid}
        config_manager.get.return_value = config_dict
        device_manager.get.return_value = device_dict
        config_manager.autocreate.return_value = autoprovid

        try:
            remove_line_from_device("abcd", 1)
        except:
            self.fail("An exception was raised whereas it should not")
