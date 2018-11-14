import pyshield as ps
import os
import shutil

def copy_config():
    if ps.__pkg_root in os.getcwd():
        msg = 'Cannot export config file to a folder of the pyshield package'
        raise IOError(msg)

    config_file = os.path.join(ps.__pkg_root__, ps.DEF_CONFIG_FILE)
    # copy file to current location
    shutil.copyfile(config_file, ps.CONFIG_FILE)       

if __name__ == "__main__":
    copy_config()                   