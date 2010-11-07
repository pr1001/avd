# avd

avd is a Python command-line tool to manage Android Virtual Devices. The goal is to assemble a large library of device profiles such that Android developers can make test their code in the Android Emulator in environments as close to their target devices as possible.

    $ ./avd.py --help
    Usage: avd [--option=value ...] subject [action [name]]
    
    Creates Android Virtual Devices based upon actual Android devices.
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --sdk=SDK             The location of the Android SDK. Defaults to the
                            environment variable ANDROID_SDK_ROOT.
      --repo=REPO           The location where user AVDs are stored. Defaults to
                            ~/.android/avd/.
      -t TARGET, --target=TARGET
                            The Android version to target. If no version is
                            specified then all valid versions are assumed.

Valid subjects are 'device' and 'skin'. If the plural of the subject is given and no action then the currently installed devices or skins are listed. Valid actions are 'info', 'install', and 'uninstall'.

This is a work in progress and there are definitely rough edges. For instance, default (i.e. non-custom) skins are currently **not** supported. Please open tickets for any bugs or feature requests. Or better yet, send me a pull request with the fix. To add devices or skins clone the repository and then make the appropriate JSON files in the appropriate directories. The README files in `devices/` and `skins` have more information.

By Peter Robinett of [Bubble Foundry](http://www.bubblefoundry.com). avd is available under the MIT license:

Copyright (c) 2010 Peter Robinett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
