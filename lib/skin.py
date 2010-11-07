import os
import json

class Skin(object):
    """
    A class representing an Android Virtual Device skin.
    """
    
    def __init__(self, skin_name, avd_root, android_sdk_root=os.getenv('ANDROID_SDK_ROOT')):
        self.AVD_ROOT = avd_root
        self.ANDROID_SDK_ROOT = android_sdk_root
        # don't catch any exceptions so that they bubble up
        skin_file = os.path.abspath(os.path.join(self.AVD_ROOT, 'skins', skin_name, skin_name + '.json'))
        skin_dict = json.load(open(skin_file, 'r'))
        # the loops is more elegant but the manual way will uncover any missing fields
        # for key in skin_dict:
        #     self[key] = skin_dict[key]
        self.name = skin_dict['name']
        self.author = skin_dict['author']
        self.version = skin_dict['version']
        self.homepage = skin_dict['homepage']
        self.supported_versions = skin_dict['supported_versions']
        
    def is_installed(self, android_version):
        skin_avd_dir = os.path.abspath(os.path.join(self.AVD_ROOT, 'skins', self.name))
        skin_android_dir = os.path.abspath(os.path.join(self.ANDROID_SDK_ROOT, 'platforms', android_version, 'skins', self.name))
        return (
            os.path.exists(skin_avd_dir) and
            os.path.isdir(skin_avd_dir) and
            os.path.exists(skin_android_dir) and
            os.path.islink(skin_android_dir) and
            os.path.realpath(skin_avd_dir) == os.path.realpath(skin_android_dir)
        )
    
    def installed_versions(self):
        return [t[0] for t in [(version, self.is_installed(version)) for version in self.supported_versions] if t[1]]
        
    def install(self, android_version):
        # first check the user isn't trying to install an unsupported version
        if (not android_version in self.supported_versions):
            return False
        skin_avd_dir = os.path.abspath(os.path.join(self.AVD_ROOT, 'skins', self.name))
        skin_android_dir = os.path.abspath(os.path.join(self.ANDROID_SDK_ROOT, 'platforms', android_version, 'skins', self.name))
        # return False if it already exists
        if (os.path.exists(skin_android_dir)):
            return False
        os.symlink(skin_avd_dir, skin_android_dir)
        return os.path.islink(skin_android_dir)
        
    def uninstall(self, android_version):
        # first check the user isn't trying to uninstall an unsupported version
        if (not android_version in self.supported_versions):
            return False
        skin_avd_dir = os.path.abspath(os.path.join(self.AVD_ROOT, 'skins', self.name))
        skin_android_dir = os.path.abspath(os.path.join(self.ANDROID_SDK_ROOT, 'platforms', android_version, 'skins', self.name))
        # return True if it already doesn't exist
        if (not os.path.exists(skin_android_dir)):
            return True
        # return False if it isn't a symlink, suggesting that it wasn't installed by avd
        if (not os.path.islink(skin_android_dir)):
            return False
        os.remove(skin_android_dir)
        return not os.path.exists(skin_android_dir)