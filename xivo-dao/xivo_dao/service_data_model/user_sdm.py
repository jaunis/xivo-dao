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


class UserSdm(object):

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

        # TODO: explain
        self.userfield = ""
        self.timezone = ""
        self.language = ""
        self.description = ""
        self.cti_profile_id = None
        self.voicemailid = None
        self.agentid = None
        self.entityid = None
