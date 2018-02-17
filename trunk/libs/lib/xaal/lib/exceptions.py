
# devices.py
class DeviceError(Exception):pass

# core.py
class XAALError(Exception):pass
class CallbackError(Exception):
    def __init__(self, code, desc):
        self.code = code
        self.description = desc

# messages.py
class MessageParserError(Exception):pass
class MessageError(Exception):pass


__all__ = ["DeviceError","XAALError","CallbackError","MessageParserError","MessageError"]
