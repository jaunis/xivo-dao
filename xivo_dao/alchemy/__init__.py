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

from xivo_dao.alchemy.accesswebservice import AccessWebService
from xivo_dao.alchemy.agentfeatures import AgentFeatures
from xivo_dao.alchemy.agent_login_status import AgentLoginStatus
from xivo_dao.alchemy.agent_membership_status import AgentMembershipStatus
from xivo_dao.alchemy.agentqueueskill import AgentQueueSkill
from xivo_dao.alchemy.callfiltermember import Callfiltermember
from xivo_dao.alchemy.callfilter import Callfilter
from xivo_dao.alchemy.call_log import CallLog
from xivo_dao.alchemy.cel import CEL
from xivo_dao.alchemy.contextinclude import ContextInclude
from xivo_dao.alchemy.contextmember import ContextMember
from xivo_dao.alchemy.contextnumbers import ContextNumbers
from xivo_dao.alchemy.context import Context
from xivo_dao.alchemy.contexttype import ContextType
from xivo_dao.alchemy.cti_contexts import CtiContexts
from xivo_dao.alchemy.ctidirectories import CtiDirectories
from xivo_dao.alchemy.ctidirectoryfields import CtiDirectoryFields
from xivo_dao.alchemy.cti_displays import CtiDisplays
from xivo_dao.alchemy.ctimain import CtiMain
from xivo_dao.alchemy.ctiphonehintsgroup import CtiPhoneHintsGroup
from xivo_dao.alchemy.ctiphonehints import CtiPhoneHints
from xivo_dao.alchemy.cti_preference import CtiPreference
from xivo_dao.alchemy.ctipresences import CtiPresences
from xivo_dao.alchemy.cti_profile_preference import CtiProfilePreference
from xivo_dao.alchemy.cti_profile import CtiProfile
from xivo_dao.alchemy.cti_profile_service import CtiProfileService
from xivo_dao.alchemy.cti_profile_xlet import CtiProfileXlet
from xivo_dao.alchemy.ctireversedirectories import CtiReverseDirectories
from xivo_dao.alchemy.cti_service import CtiService
from xivo_dao.alchemy.ctisheetactions import CtiSheetActions
from xivo_dao.alchemy.ctisheetevents import CtiSheetEvents
from xivo_dao.alchemy.ctistatus import CtiStatus
from xivo_dao.alchemy.cti_xlet_layout import CtiXletLayout
from xivo_dao.alchemy.cti_xlet import CtiXlet
from xivo_dao.alchemy.dialaction import Dialaction
from xivo_dao.alchemy.dialpattern import DialPattern
from xivo_dao.alchemy.entity import Entity
from xivo_dao.alchemy.extension import Extension
from xivo_dao.alchemy.features import Features
from xivo_dao.alchemy.func_key_destination_type import FuncKeyDestinationType
from xivo_dao.alchemy.func_key_dest_group import FuncKeyDestGroup
from xivo_dao.alchemy.func_key_dest_user import FuncKeyDestUser
from xivo_dao.alchemy.func_key_mapping import FuncKeyMapping
from xivo_dao.alchemy.func_key import FuncKey
from xivo_dao.alchemy.func_key_template import FuncKeyTemplate
from xivo_dao.alchemy.func_key_type import FuncKeyType
from xivo_dao.alchemy.groupfeatures import GroupFeatures
from xivo_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits
from xivo_dao.alchemy.incall import Incall
from xivo_dao.alchemy.ldapfilter import LdapFilter
from xivo_dao.alchemy.ldapserver import LdapServer
from xivo_dao.alchemy.linefeatures import LineFeatures
from xivo_dao.alchemy.meetmefeatures import MeetmeFeatures
from xivo_dao.alchemy.musiconhold import MusicOnHold
from xivo_dao.alchemy.phonebookaddress import PhonebookAddress
from xivo_dao.alchemy.phonebooknumber import PhonebookNumber
from xivo_dao.alchemy.phonebook import Phonebook
from xivo_dao.alchemy.phonefunckey import PhoneFunckey
from xivo_dao.alchemy.pickupmember import PickupMember
from xivo_dao.alchemy.pickup import Pickup
from xivo_dao.alchemy.queuefeatures import QueueFeatures
from xivo_dao.alchemy.queueinfo import QueueInfo
from xivo_dao.alchemy.queue_log import QueueLog
from xivo_dao.alchemy.queuemember import QueueMember
from xivo_dao.alchemy.queuepenaltychange import QueuePenaltyChange
from xivo_dao.alchemy.queuepenalty import QueuePenalty
from xivo_dao.alchemy.queue import Queue
from xivo_dao.alchemy.queueskill import QueueSkill
from xivo_dao.alchemy.queueskillrule import QueueSkillRule
from xivo_dao.alchemy.record_campaigns import RecordCampaigns
from xivo_dao.alchemy.recordings import Recordings
from xivo_dao.alchemy.rightcallmember import RightCallMember
from xivo_dao.alchemy.rightcall import RightCall
from xivo_dao.alchemy.sccpdevice import SCCPDevice
from xivo_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from xivo_dao.alchemy.sccpline import SCCPLine
from xivo_dao.alchemy.schedulepath import SchedulePath
from xivo_dao.alchemy.schedule import Schedule
from xivo_dao.alchemy.sipauthentication import SIPAuthentication
from xivo_dao.alchemy.stat_agent_periodic import StatAgentPeriodic
from xivo_dao.alchemy.stat_agent import StatAgent
from xivo_dao.alchemy.stat_call_on_queue import StatCallOnQueue
from xivo_dao.alchemy.staticiax import StaticIAX
from xivo_dao.alchemy.staticmeetme import StaticMeetme
from xivo_dao.alchemy.staticqueue import StaticQueue
from xivo_dao.alchemy.staticsip import StaticSIP
from xivo_dao.alchemy.staticvoicemail import StaticVoicemail
from xivo_dao.alchemy.stat_queue_periodic import StatQueuePeriodic
from xivo_dao.alchemy.stat_queue import StatQueue
from xivo_dao.alchemy.trunkfeatures import TrunkFeatures
from xivo_dao.alchemy.usercustom import UserCustom
from xivo_dao.alchemy.userfeatures import UserFeatures
from xivo_dao.alchemy.useriax import UserIAX
from xivo_dao.alchemy.user_line import UserLine
from xivo_dao.alchemy.usersip import UserSIP
from xivo_dao.alchemy.voicemail import Voicemail