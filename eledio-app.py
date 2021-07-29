import json

from eledio import Eledio
from eledio.component.mpu.i2c import SMBus
from eledio.device.pcu import PcuFactory
from eledio.device.mpu import MpuFactory
from eledio.device.srq import Srq


def handle_srq(identifiers):
    """
    User handling of SRQ (called in context of eledio.wait_events)
    :param identifiers: dictionary of eledio identifiers and their new value after SRQ
    :return:
    """
    print("Service requests!", identifiers)


def handle_error(src, ex):
    """
    Handle error inside eledio library
    :param src:
    :param ex:
    :return:
    """
    print(src, ex)


if __name__ == "__main__":
    eledio = Eledio()
    eledio.register_device_factory("i2c", PcuFactory(SMBus(0)))
    eledio.register_device_factory("mpu", MpuFactory())
    eledio.error_handler = handle_error

    # repeat for every configuration file
    with open('data/map.json') as f:
        eledio.append_config(json.load(f))

    with open('data/mpu-config.json') as f:
        eledio.append_config(json.load(f))

    while True:
        # load state of inputs and outputs
        eledio.load_inputs()

        # manipulate with inputs and outputs by identifier
        # e.g.
        #   print(eledio["test1"])
        #   eledio["test2"] = True

        # apply final value to hardware
        eledio.store_outputs()

        # do something else or wait some time
        eledio.wait_events(1.0)
