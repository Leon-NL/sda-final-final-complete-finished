from .enums.ptpMode import PTPMode
from .enums.CommunicationProtocolIDs import CommunicationProtocolIDs
from .enums.ControlValues import ControlValues


class Message:
    def __init__(self, b=None):
        if b is None:
            self.header = bytes([0xAA, 0xAA])
            self.len = 0x00
            self.ctrl = ControlValues.ZERO
            self.params = bytes([])
            self.checksum = None
        else:
            self.header = b[0:2]
            self.len = b[2]
            self.id = CommunicationProtocolIDs(b[3])
            self.ctrl = ControlValues(b[4])
            self.params = b[5:-1]
            self.checksum = b[-1:][0]

    def __repr__(self):
        return "Message()"

    def __str__(self):
        self.refresh()
        hexHeader = " ".join("%02x" % b for b in self.header)
        hexParams = " ".join("%02x" % b for b in self.params)
        ret = "%s:%d:%d:%d:%s:%s" % (hexHeader, self.len, self.id.value, self.ctrl.value, hexParams, self.checksum)
        return ret.upper()

    def refresh(self):
        if self.checksum is None:
            try:
                self.checksum = self.id.value + self.ctrl.value
            except:
                self.checksum = self.id + self.ctrl

            for i in range(len(self.params)):
                if isinstance(self.params[i], int):
                    self.checksum += self.params[i]
                else:
                    self.checksum += int(self.params[i].encode('hex'), 16)
            self.checksum = self.checksum % 256
            self.checksum = 2 ** 8 - self.checksum
            self.checksum = self.checksum % 256
            self.len = 0x02 + len(self.params)

    def bytes(self):
        self.refresh()
        if len(self.params) > 0:
            command = bytearray([0xAA, 0xAA, self.len, self.id.value, self.ctrl.value])
            command.extend(self.params)
            command.append(self.checksum)
        else:
            try:
                command = bytes([0xAA, 0xAA, self.len, self.id.value, self.ctrl.value, self.checksum])
            except:
                command = bytes([0xAA, 0xAA, self.len, self.id, self.ctrl, self.checksum])
        return command
