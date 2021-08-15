import json
import logging
import logging.handlers
import os
from datetime import datetime
import pytz
try:
    from eledio import Eledio
    from eledio.component.mpu.i2c import SMBus
    from eledio.device.pcu import PcuFactory
    from eledio.device.mpu import MpuFactory
except:
    pass

__all__ = ['HotWaterPumpDevice', 'HotWaterPumpLib']

def configure_logger():
    # Start local logging
    logging.basicConfig(level=10)
    log_path = 'log/hot-water-pump.log'
    os.makedirs(os.path.dirname(log_path))
    handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=100000,
        backupCount=10)
    handler.setLevel(10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


class HotWaterPumpDevice:
    def __init__(self):
        configure_logger()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.eledio = Eledio()
        self.eledio.register_device_factory("i2c", PcuFactory(SMBus(0)))
        self.eledio.register_device_factory("mpu", MpuFactory())
        self.eledio.error_handler = self._handle_eledio_error
        self.config = {}
        self.init_configuration()

    def init_configuration(self):
        # repeat for every configuration file
        with open('map.json') as f:
            self.eledio.append_config(json.load(f))

        with open('mpu-config.json') as f:
            self.eledio.append_config(json.load(f))

        with open('config.json') as f:
            self.config = json.load(f)

    def _handle_eledio_error(self, src, ex):
        message = "Eledio: error {}, {}".format(src, ex)
        self.logger.error(message)

        # until memory leak is resolved rather restart the script
        if "Out of memory" in str(ex):
            raise ex


class HotWaterPumpLib:
    def __init__(self, _config):
        self.config = _config

    def check_time_mask(self, datetime=datetime.now()):
        actual_time = datetime.hour * 60 + datetime.minute
        actual_day = datetime.weekday()
        if 0 <= actual_day <= 6:
            pass
        else:
            actual_day = 0

        for _ranges in self.config["timeplan"][str(actual_day)]:
            for _range in _ranges:
                if _range["begin"] <= actual_time <= _range["end"]:
                    return True
        return False