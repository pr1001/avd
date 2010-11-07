#! /usr/bin/env python

"""
avd

avd is both a Python script and a database of device settings to generate Android Virtual Devices.

"""

__author__  = 'Peter Robinett <peter@bubblefoundry.com>' 
__version__ = '0.1'

import sys
import os
import optparse

from lib.device import Device
from lib.skin import Skin

def run(options, arguments):
    AVD_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
    AVD_REPO_ROOT = os.path.abspath(options.repo)
    ANDROID_SDK_ROOT = os.path.abspath(options.sdk)
    
    if len(arguments) == 1:
        subject = arguments[0]
        if (subject == 'devices'):
            devices = [os.path.basename(entry) for entry in os.listdir(os.path.join(AVD_ROOT, 'devices')) if os.path.isfile(os.path.join(AVD_ROOT, 'devices', entry)) and os.path.splitext(os.path.join(AVD_ROOT, 'devices', entry))[1] == '.json']
            # stupid Python and returning None instead of an empty List
            if (not devices):
                devices = []
            for device_name in devices:
                device = Device(os.path.splitext(device_name)[0], AVD_ROOT, AVD_REPO_ROOT, ANDROID_SDK_ROOT)
                print 'Name: {name}'.format(name=device.name)
                if device.skin:
                    print 'Skin: {skin}'.format(skin=device.skin.name)
                versions = ', '.join(device.supported_versions) if device.supported_versions else 'None'
                print 'Versions Supported: {versions}'.format(versions=versions)
                installed = ', '.join(device.installed_versions()) if device.installed_versions() else 'None'
                print 'Versions Installed: {installed}'.format(installed=installed)
            if not devices:
                print "No devices installed."
        elif (subject == 'skins'):
            skins = [os.path.basename(entry) for entry in os.listdir(os.path.join(AVD_ROOT, 'skins')) if os.path.isdir(os.path.join(AVD_ROOT, 'skins', entry))]
            # stupid Python and returning None instead of an empty List
            if (not skins):
                skins = []
            for skin_name in skins:
                skin = Skin(skin_name, AVD_ROOT, ANDROID_SDK_ROOT)
                print 'Name: {name}'.format(name=skin.name)
                versions = ', '.join(skin.supported_versions) if skin.supported_versions else 'None'
                print 'Versions Supported: {versions}'.format(versions=versions)
                installed = ', '.join(skin.installed_versions()) if skin.installed_versions() else 'None'
                print 'Versions Installed: {installed}'.format(installed=installed)
            if not skins:
                print 'No skins installed.'
    elif len(arguments) == 3:
        subject, action, name = arguments
        
        if (subject == 'device'):
            device = Device(name, AVD_ROOT, AVD_REPO_ROOT, ANDROID_SDK_ROOT)
            if (action == 'info'):
                print 'Name: {name}'.format(name=device.name)
                if device.skin:
                    print 'Skin: {skin}'.format(skin=device.skin.name)
                versions = ', '.join(device.supported_versions) if device.supported_versions else 'None'
                print 'Versions Supported: {versions}'.format(versions=versions)
                installed = ', '.join(device.installed_versions()) if device.installed_versions() else 'None'
                print 'Versions Installed: {installed}'.format(installed=installed)
            elif (action == 'install'):
                if (options.target):
                    if (device.install(options.target)):
                        print 'Successfully installed the device {name} for version {version}. The specific device name is {versioned_name}.'.format(name=device.name, version=options.target, versioned_name=device.versioned_name(options.target))
                    else:
                        print 'Unable to install the device {name} for version {version}. Please check that the devices isn\'t already installed, {version} is one of the device\'s supported versions, and that the appropriate file permissions are set.'.format(name=device.name, version=options.target)
                else:
                    results = [device.install(version) for version in device.supported_versions]
                    if not False in results:
                        print 'Successfully installed the device {name} for all supported versions: {versions}. The specific device names are: {versioned_names}.'.format(name=device.name, versions=', '.join(device.supported_versions), versioned_names=', '.join([device.versioned_name(version) for version in device.supported_versions]))
                    else:
                        print 'Unable to install the device {name} for one or more of the Android versions.'.format(name=device.name)
            elif (action == 'uninstall'):
                if (options.target):
                    if (device.uninstall(options.target)):
                        print 'Successfully uninstalled the device {name} for version {version}.'.format(name=device.name, version=options.target)
                    else:
                        print 'Unable to uninstall the device {name} for version {version}. Please check that the device isn\'t already uninstalled, {version} is one of the device\'s supported versions, and that the appropriate file permissions are set.'.format(name=device.name, version=options.target)
                else:
                    results = [device.uninstall(version) for version in device.supported_versions]
                    if not False in results:
                        print 'Successfully uninstalled the device {name} for all supported versions: {versions}.'.format(name=device.name, versions=', '.join(device.supported_versions))
                    else:
                        print 'Unable to uninstall the device {name} for one or more of the Android versions.'.format(name=device.name)
            else:
                print "Invalid action: {action}".format(action=action)
                return False
        elif (subject == 'skin'):
            skin = Skin(name, AVD_ROOT, ANDROID_SDK_ROOT)
            if (action == 'info'):
                print 'Name: {name}'.format(name=skin.name)
                versions = ', '.join(skin.supported_versions) if skin.supported_versions else 'None'
                print 'Versions Supported: {versions}'.format(versions=versions)
                installed = ', '.join(skin.installed_versions()) if skin.installed_versions() else 'None'
                print 'Versions Installed: {installed}'.format(installed=installed)
            elif (action == 'install'):
                if (options.target):
                    if (skin.install(options.target)):
                        print 'Successfully installed the skin {name} for version {version}.'.format(name=skin.name, version=options.target)
                    else:
                        print 'Unable to install the skin {name} for version {version}. Please check that the skins isn\'t already installed, {version} is one of the skin\'s supported versions, and that the appropriate file permissions are set.'.format(name=skin.name, version=options.target)
                else:
                    results = [skin.install(version) for version in skin.supported_versions]
                    if not False in results:
                        print 'Successfully installed the skin {name} for all supported versions: {versions}.'.format(name=skin.name, versions=', '.join(skin.supported_versions))
                    else:
                        print 'Unable to install the skin {name} for one or more of the Android versions.'.format(name=skin.name)
            elif (action == 'uninstall'):
                if (options.target):
                    if (skin.uninstall(options.target)):
                        print 'Successfully uninstalled the skin {name} for version {version}.'.format(name=skin.name, version=options.target)
                    else:
                        print 'Unable to uninstall the skin {name} for version {version}. Please check that the skin isn\'t already uninstalled, {version} is one of the skin\'s supported versions, and that the appropriate file permissions are set.'.format(name=skin.name, version=options.target)
                else:
                    results = [skin.uninstall(version) for version in skin.supported_versions]
                    if not False in results:
                        print 'Successfully uninstalled the skin {name} for all supported versions: {versions}.'.format(name=skin.name, versions=', '.join(skin.supported_versions))
                    else:
                        print 'Unable to uninstall the skin {name} for one or more of the Android versions.'.format(name=skin.name)
            else:
                print "Invalid action: {action}".format(action=action)
                return False
        else:
            print "Invalid subject: {subject}".format(subject=subject)
            return False

def main():
    p = optparse.OptionParser(description='Creates Android Virtual Devices based upon actual Android devices.',
                               prog='avd',
                               version=__version__,
                               usage='%prog [--option=value ...] subject [action [name]]')
    p.add_option('--sdk', default=os.getenv('ANDROID_SDK_ROOT'), help="The location of the Android SDK. Defaults to the environment variable ANDROID_SDK_ROOT.")
    p.add_option('--repo', default=os.path.join(os.path.expanduser('~'), '.android', 'avd'), help="The location where user AVDs are stored. Defaults to ~/.android/avd/.")
    p.add_option('--target', '-t', help="The Android version to target. If no version is specified then all valid versions are assumed.")
    # p.add_option('--debug', '-d', action='store_true', dest='debug', default=False, help="Debug mode. Default: %default.")
    options, arguments = p.parse_args()
    run(options, arguments)

if __name__ == "__main__":
    sys.exit(main())
