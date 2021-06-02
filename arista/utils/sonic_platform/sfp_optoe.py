import time

try:
   from arista.utils.sonic_platform.thermal import SfpThermal
   from sonic_platform_base.sonic_xcvr.sfp_optoe_base import SfpOptoeBase
except ImportError as e:
   raise ImportError("%s - required module not found" % e)

EEPROM_PATH = '/sys/class/i2c-adapter/i2c-{0}/{0}-{1:04x}/eeprom'

# XXX: Temporary class while sfp refactor is in progress. Once refactor is done
# this class should replace the existing Sfp class.
class SfpOptoe(SfpOptoeBase):
   """
   Platform-specific sfp class
   """

   RESET_DELAY = 1

   def __init__(self, index, slot):
      SfpOptoeBase.__init__(self)
      self._index = index
      self._slot = slot
      sfp = slot.getXcvr()
      self._eepromPath = EEPROM_PATH.format(sfp.getI2cAddr().bus,
                                            sfp.getI2cAddr().address)
      self._sfp_type = None
      self._thermal_list.append(SfpThermal(self))

   @property
   def sfp_type(self):
      if self._sfp_type is None:
         self._sfp_type = self._detect_sfp_type()

      return self._sfp_type

   def _detect_sfp_type(self):
      info = self.get_transceiver_info()
      sfp_type = self._slot.getXcvr().getType().upper()
      if info:
         sfp_type = info.get("type_abbrv_name")
      # XXX: Need this hack until xcvrd is refactored
      if sfp_type == "OSFP-8X" or sfp_type == "QSFP-DD":
         sfp_type = "QSFP_DD"
      return sfp_type

   def get_id(self):
      return self._index

   def get_name(self):
      return self._slot.getName()

   def get_position_in_parent(self):
      return self._index

   def get_presence(self):
      return self._slot.getPresence()

   def is_replaceable(self):
      return True

   def get_status(self):
      return self.get_presence() and bool(self.get_transceiver_bulk_status())

   def get_lpmode(self):
      try:
         return self._slot.getLowPowerMode()
      except NotImplementedError:
         return False
      except: # pylint: disable-msg=W0702
         return False

   def set_lpmode(self, lpmode):
      try:
         self._slot.setLowPowerMode(lpmode)
      except NotImplementedError:
         return False
      except: # pylint: disable-msg=W0702
         return False
      return True

   def get_reset_status(self):
      reset = self._slot.getReset()
      return reset.read() if reset else False

   def reset(self):
      try:
         self._slot.getReset().resetIn()
      except: # pylint: disable-msg=W0702
         return False
      time.sleep(self.RESET_DELAY)
      try:
         self._slot.getReset().resetOut()
      except: # pylint: disable-msg=W0702
         return False
      # XXX: Hack to handle SFP modules plugged into non-SFP ports, which could
      # allow for a reset to "succeed" when it shouldn't
      if self.sfp_type == "SFP":
         return False
      return True

   def clear_interrupt(self):
      intr = self._slot.getInterruptLine()
      if not intr:
         return False
      self.get_presence()
      intr.clear()
      return True

   def get_interrupt_file(self):
      intr = self._slot.getInterruptLine()
      if intr:
         return intr.getFile()
      return None

   def get_eeprom_path(self):
      return self._eepromPath