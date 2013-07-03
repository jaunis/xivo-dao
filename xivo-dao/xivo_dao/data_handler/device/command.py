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

from __future__ import unicode_literals


class AbstractDeviceIDParams(object):

    def __init__(self, device_id, deviceid):
        self.id = int(device_id)
        self.deviceid = int(deviceid)

    def marshal(self):
        return {
            'id': self.id,
            'deviceid': self.deviceid
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['deviceid'])


class EditDeviceCommand(AbstractDeviceIDParams):
    name = 'device_edited'


class CreateDeviceCommand(AbstractDeviceIDParams):
    name = 'device_created'


class DeleteDeviceCommand(AbstractDeviceIDParams):
    name = 'device_deleted'
