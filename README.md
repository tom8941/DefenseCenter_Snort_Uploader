# DefenseCenter_Snort_Uploader

This is a little script that give the possibility to upload snort file automatically on SourceFire Defense Center.
By combining this project with this other one to export snort from MISP: MISP-IOC-Validator (https://github.com/tom8941/MISP-IOC-Validator),
you can get an export of validated snort rules from MISP and upload it automatically into SourceFire Defense Center.

## Prerequisite

- install of the following module:
 - selenium for python (http://selenium-python.readthedocs.io/installation.html)
- The server should have a X server running
- Be sure that the X session of the user that is running the script is open (you can even "lock the screen" of the Desktop session)
- xterm should be installed on the system
- This script has been desgined to run with Firefox only (some Firefox version may be incompatible with some selenium version)
- An Intrusion policy should be already created. You have to get his uuid which is like xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (you can find it in the url when editing the policy)

## Usage and Examples

```
parameters : 
  -f FILE, --file FILE  Snort file to upload
  -s SOURCEFIRE, --sourcefire SOURCEFIRE
                        Sourcefire ip or hostname
  -u USER, --user USER  Sourcefire user account
  -p PASSWORD, --password PASSWORD
                        Sourcefire user password
  -i UUID, --uuid UUID  Intrusion Policy UUID that will contains new
                        signatures

DISPLAY=:0 xterm -e './dc_snort_uploader.py -u user -p password -s sourcefire.local  -f /tmp/snort_rules.yml -i xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

If there is some errors you can add -hold option in front of xterm to let the Xwindow open
```

You can modify time.sleep() in the script if you want.
There are not always necessary but it strongly advised because some actions of the web interface and data loads need some time.

## External Source
 
- selenium : http://www.seleniumhq.org/
- MISP-IOC-Validator : https://github.com/tom8941/MISP-IOC-Validator
