# -*- coding: UTF-8 -*-
#
# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from xivo_dao.service_data_model.base_sdm import BaseSdm
from xivo_dao.service_data_model.sdm_exception import MissingParametersException


class UserSdm(BaseSdm):

    REQUIRED_PARAMETERS = ['firstname']

    def __init__(self):
        self.id = None
        self.firstname = ""
        self.lastname = ""
        self.callerid = ""
        self.username = ""
        self.password = ""
        self.enableclient = False
        self.musiconhold = ""
        self.outcallerid = ""
        self.mobilephonenumber = ""

        # field to be used for user specific purposes like billing
        self.userfield = ""
        self.timezone = ""
        self.language = ""
        self.description = ""
        self.ctiprofileid = None
        self.voicemailid = None
        self.agentid = None
        self.entityid = None
        self.line = None

    def validate(self, parameters):
        BaseSdm.validate(self, parameters)

        missing = []
        for param_name in self.REQUIRED_PARAMETERS:
            if param_name not in parameters:
                missing.append(param_name)

        if len(missing) > 0:
            raise MissingParametersException(*missing)

        return True
