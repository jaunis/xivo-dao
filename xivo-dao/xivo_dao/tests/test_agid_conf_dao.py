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

from hamcrest import *

from xivo_dao import agid_conf_dao
from xivo_dao.alchemy.agent_login_status import AgentLoginStatus
from xivo_dao.alchemy.agentfeatures import AgentFeatures
from xivo_dao.alchemy.agentqueueskill import AgentQueueSkill
from xivo_dao.alchemy.context import Context
from xivo_dao.alchemy.contextinclude import ContextInclude
from xivo_dao.alchemy.cti_profile import CtiProfile
from xivo_dao.alchemy.ctiphonehintsgroup import CtiPhoneHintsGroup
from xivo_dao.alchemy.ctipresences import CtiPresences
from xivo_dao.alchemy.extension import Extension
from xivo_dao.alchemy.features import Features
from xivo_dao.alchemy.groupfeatures import GroupFeatures
from xivo_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits
from xivo_dao.alchemy.linefeatures import LineFeatures
from xivo_dao.alchemy.musiconhold import MusicOnHold
from xivo_dao.alchemy.phonefunckey import PhoneFunckey
from xivo_dao.alchemy.pickup import Pickup
from xivo_dao.alchemy.pickupmember import PickupMember
from xivo_dao.alchemy.queue import Queue
from xivo_dao.alchemy.queuefeatures import QueueFeatures
from xivo_dao.alchemy.queuemember import QueueMember
from xivo_dao.alchemy.queuepenalty import QueuePenalty
from xivo_dao.alchemy.queuepenaltychange import QueuePenaltyChange
from xivo_dao.alchemy.queueskill import QueueSkill
from xivo_dao.alchemy.queueskillrule import QueueSkillRule
from xivo_dao.alchemy.sccpdevice import SCCPDevice
from xivo_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from xivo_dao.alchemy.sccpline import SCCPLine
from xivo_dao.alchemy.sipauthentication import SIPAuthentication
from xivo_dao.alchemy.staticiax import StaticIAX
from xivo_dao.alchemy.staticmeetme import StaticMeetme
from xivo_dao.alchemy.staticqueue import StaticQueue
from xivo_dao.alchemy.staticsip import StaticSIP
from xivo_dao.alchemy.staticvoicemail import StaticVoicemail
from xivo_dao.alchemy.user_line import UserLine
from xivo_dao.alchemy.userfeatures import UserFeatures
from xivo_dao.alchemy.usersip import UserSIP
from xivo_dao.alchemy.voicemail import Voicemail
from xivo_dao.tests.test_dao import DAOTestCase


class TestAsteriskConfDAO(DAOTestCase):

    tables = [AgentFeatures,
              AgentLoginStatus,
              AgentQueueSkill,
              Context,
              ContextInclude,
              CtiPhoneHintsGroup,
              CtiPresences,
              CtiProfile,
              Extension,
              Features,
              GroupFeatures,
              IAXCallNumberLimits,
              LineFeatures,
              MusicOnHold,
              PhoneFunckey,
              Pickup,
              PickupMember,
              Queue,
              QueueFeatures,
              QueueMember,
              QueuePenalty,
              QueuePenaltyChange,
              QueueSkill,
              QueueSkillRule,
              SCCPDevice,
              SCCPGeneralSettings,
              SCCPLine,
              SIPAuthentication,
              StaticIAX,
              StaticMeetme,
              StaticQueue,
              StaticSIP,
              StaticVoicemail,
              UserLine,
              UserFeatures,
              UserSIP,
              Voicemail]

    def setUp(self):
        self.empty_tables()

    def test_get_group_settings_no_group(self):
        self.assertRaises(LookupError, agid_conf_dao.get_group_settings, 666)

    def test_get_group_settings_not_found(self):
        group = self.add_group()
        self.add_queue(name=group.name, category='queue')

        self.assertRaises(LookupError, agid_conf_dao.get_group_settings, group.id)

        group = self.add_group()

        self.assertRaises(LookupError, agid_conf_dao.get_group_settings, group.id)

    def test_get_group_settings(self):
        group = self.add_group()
        queue = self.add_queue(name=group.name, category='group')

        expected_result = {
            'number': group.number,
            'context': group.context,
            'name': group.name,
            'timeout': group.timeout,
            'transfer_user': group.transfer_user,
            'transfer_call': group.transfer_call,
            'write_caller': group.write_caller,
            'write_calling': group.write_calling,
            'preprocess_subroutine': group.preprocess_subroutine,
            'musicclass': queue.musicclass
        }

        result = agid_conf_dao.get_group_settings(group.id)

        assert_that(result, has_entries(expected_result))

    def test_get_agent_device_no_agent(self):
        self.assertRaises(LookupError, agid_conf_dao.get_agent_device, 666)

    def test_get_agent_device(self):
        state_interface = 'toto'
        agent_login_status = self.add_agent_login_status(state_interface=state_interface)

        expected_result = state_interface

        result = agid_conf_dao.get_agent_device(agent_login_status.agent_id)

        assert_that(result, equal_to(expected_result))

    def test_get_agent_no_agent(self):
        self.assertRaises(LookupError, agid_conf_dao.get_agent, 666)

    def test_get_agent(self):
        agent = self.add_agent(firstname='toto',
                               lastname='titi')

        expected_result = {
            'id': agent.id,
            'number': agent.number,
            'passwd': agent.passwd,
            'firstname': agent.firstname,
            'lastname': agent.lastname,
            'language': agent.language,
            'preprocess_subroutine': agent.preprocess_subroutine
        }

        result = agid_conf_dao.get_agent(agent.id)

        assert_that(result, has_entries(expected_result))

    def test_get_agent_with_number_no_agent(self):
        self.assertRaises(LookupError, agid_conf_dao.get_agent_with_number, 666)

    def test_get_agent_with_number(self):
        agent = self.add_agent(firstname='toto',
                               lastname='titi')

        expected_result = {
            'id': agent.id,
            'number': agent.number,
            'passwd': agent.passwd,
            'firstname': agent.firstname,
            'lastname': agent.lastname,
            'language': agent.language,
            'preprocess_subroutine': agent.preprocess_subroutine
        }

        result = agid_conf_dao.get_agent_with_number(agent.number)

        assert_that(result, has_entries(expected_result))
