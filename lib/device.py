import os
import json
from subprocess import call

from skin import Skin

class Device(object):
    """
    A class representing an Android Virtual Device device.
    """
    
    def __init__(self, device_name, avd_root, avd_repo_root, android_sdk_root=os.getenv('ANDROID_SDK_ROOT')):
        self.AVD_ROOT = avd_root
        self.AVD_REPO_ROOT = avd_repo_root
        # don't catch any exceptions so that they bubble up
        device_file = os.path.abspath(os.path.join(self.AVD_ROOT, 'devices', device_name + '.json'))
        device_dict = json.load(open(device_file, 'r'))
        # the loops is more elegant but the manual way will uncover any missing fields
        # for key in device_dict:
        #     self[key] = device_dict[key]
        self.name = device_dict['name']
        self.supported_versions = device_dict['supported_versions']
        if 'skin' in device_dict:
            self.skin = Skin(device_dict['skin'], self.AVD_ROOT, android_sdk_root)
        # so people have to only test 'if myDevice.skin: ...' and not for its existence
        else:
            self.skin = None
        if 'sdcard' in device_dict:
            self.sdcard = device_dict['sdcard']
        # so people have to only test 'if myDevice.sdcard: ...' and not for its existence
        else:
            self.sdcard = None
        if 'options' in device_dict:
            self.options = device_dict['options']
        # so people have to only test 'if myDevice.options: ...' and not for its existence
        else:
            self.options = None
        
    def versioned_name(self, android_version):
        return self.name + '-' + android_version
    
    def is_installed(self, android_version):
        device_avd_dir = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.avd'))
        device_avd_ini = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.ini'))
        return (
            os.path.exists(device_avd_dir) and
            os.path.isdir(device_avd_dir) and
            os.path.exists(device_avd_ini) and
            os.path.isfile(device_avd_ini)
        )
    
    def installed_versions(self):
        return [t[0] for t in [(version, self.is_installed(version)) for version in self.supported_versions] if t[1]]
        
    def install(self, android_version):
        # first check the user isn't trying to install an unsupported version
        if (not android_version in self.supported_versions):
            return False
        device_avd_dir = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.avd'))
        device_avd_ini = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.ini'))
        # return False if it already exists
        if (os.path.isdir(device_avd_dir) and os.path.isfile(device_avd_ini)):
            return False
        command = ['android', 'create', 'avd']
        # force creation, since we've already checked that both files don't already exist
        command.append('-f')
        # add the name
        command.extend(['-n', self.versioned_name(android_version)])
        # add the target
        command.extend(['-t', android_version])
        if self.sdcard:
            if 'file' in self.sdcard:
                img_path = os.path.abspath(os.path.join(self.AVD_ROOT, 'devices', self.sdcard['file']))
                command.extend(['-c', img_path])
            elif 'size' in self.sdcard:
                command.extend(['-c', self.sdcard['size']])
        if self.skin:
            if (self.skin.is_installed(android_version) or self.skin.install(android_version)):
                command.extend(['-s', self.skin.name])
            else:
                return False
        retcode = call(command)
        if (os.path.isdir(device_avd_dir) and os.path.isfile(device_avd_ini)):
            # now add any additional options if specified
            if self.options:
                fp = open(device_avd_ini, 'a+')
                lines = ['{key}={value}\n'.format(key=option, value=self.options[option]) for option in self.options]
                fp.writelines(lines)
                fp.close()
            return True
        else:
            return False
        
    def uninstall(self, android_version):
        # first check the user isn't trying to uninstall an unsupported version
        if (not android_version in self.supported_versions):
            return False
        device_avd_dir = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.avd'))
        device_avd_ini = os.path.abspath(os.path.join(self.AVD_REPO_ROOT, self.versioned_name(android_version) + '.ini'))
        # return True if it already doesn't exist
        if (not os.path.isdir(device_avd_dir) and not os.path.isfile(device_avd_ini)):
            return True
        retcode = call(['android', 'delete', 'avd', '-n', self.versioned_name(android_version)])
        return not os.path.exists(device_avd_dir) and not os.path.exists(device_avd_ini)