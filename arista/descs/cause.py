
class ReloadCausePriority(object):
   NONE = 0
   LOW = 10
   NORMAL = 20
   HIGH = 30

class ReloadCauseScore(object):
   # DO NOT CHANGE EXISTING VALUES UNLESS YOU UNDERSTAND THE IMPLICATIONS
   # format:
   # 0:7 -> priority
   UNKNOWN = 0
   DETAILED = (1 << 10)
   EVENT = (1 << 16)
   LOGGED = (1 << 32)

   @staticmethod
   def getPriority(value):
       assert value == (value & 0xff)
       return value & 0xff

class ReloadCauseDesc(object):

   KILLSWITCH = 'killswitch'
   OVERTEMP = 'overtemp'
   POWERLOSS = 'powerloss'
   RAIL = 'rail'
   REBOOT = 'reboot'
   WATCHDOG = 'watchdog'
   CPU = 'cpu'
   SEU = 'seu'

   DEFAULT_DESCRIPTIONS = {
      KILLSWITCH: 'Kill switch',
      OVERTEMP: 'Thermal trip fault',
      POWERLOSS: 'System lost power',
      RAIL: 'Rail fault',
      REBOOT: 'Rebooted by user',
      WATCHDOG: 'Watchdog fired',
      CPU: 'CPU fault',
      SEU: 'SEU fault',
   }

   def __init__(self, code, typ, description=None):
      self.code = code
      self.typ = typ
      self.description = self.DEFAULT_DESCRIPTIONS.get(typ)
      if description is not None:
         self.description = f'{self.description} - {description}'

