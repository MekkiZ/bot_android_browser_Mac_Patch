# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.0)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x72\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\
\x00\x00\x00\x04\x73\x42\x49\x54\x08\x08\x08\x08\x7c\x08\x64\x88\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x00\x6f\x00\x00\x00\x6f\
\x01\xf1\xa2\xdc\x43\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\
\x74\x77\x61\x72\x65\x00\x77\x77\x77\x2e\x69\x6e\x6b\x73\x63\x61\
\x70\x65\x2e\x6f\x72\x67\x9b\xee\x3c\x1a\x00\x00\x00\xef\x49\x44\
\x41\x54\x38\x8d\xa5\x93\x31\x6e\xc2\x50\x10\x44\xdf\x7c\xa7\x27\
\x67\xa0\x88\x28\x90\xdc\x21\xe5\x06\x39\x42\xe4\x53\xb8\x73\x99\
\x14\x28\x47\x31\x5c\x24\x29\x28\xd3\x80\xb8\x8b\x35\x29\x58\xa2\
\x0f\xfa\x76\x50\x18\x69\x9b\x9d\x99\xdd\xbf\xab\xfd\xb2\x4d\x0e\
\x49\x4f\x40\x03\x2c\x00\x45\xda\xc0\x1e\xd8\xd8\x3e\x5e\x18\x6c\
\x13\x45\x04\xb4\x40\x0f\xd4\x40\x95\x71\x55\xe4\xfa\xd0\xe8\x97\
\xcb\xcc\x3d\xd0\x9c\x89\xc8\xcf\x81\xf9\x55\xae\x09\xad\xf2\x02\
\xed\x88\xf9\x33\xa2\x54\xa4\xb5\x4d\x8a\x99\x57\xb6\x7b\x6e\x44\
\x68\x57\xe1\xe5\x1d\xa8\xf3\x0e\x53\x23\x64\x5c\x0d\xbc\x01\x6c\
\xf3\x85\x65\x82\xef\xe0\xbe\x80\x97\x02\x5f\x01\xdb\x87\x58\xc6\
\x30\xf2\xda\x35\xb0\x04\x1e\x0b\x63\x0c\x92\x94\x26\x46\xfd\x08\
\xf3\x24\x12\x60\x49\xd5\x5f\xc2\x6b\x84\xc7\x09\x38\xdc\xd2\xa9\
\x80\x25\xb0\x4f\x9c\x8e\xa2\xfb\x47\x81\x0e\xd8\xa4\xb8\xed\x9d\
\xa4\xa6\x20\x7a\x8e\xb8\x40\x68\x77\xb6\x8f\xa3\xa7\x0c\xcc\x80\
\xd7\x88\xd9\xe4\x29\xdf\xf3\x99\x74\xef\x77\xfe\x01\x61\x27\xe4\
\xb5\xef\xd1\x5b\xd9\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\
\x82\
"

qt_resource_name = b"\
\x00\x04\
\x00\x07\x04\xcf\
\x00\x69\
\x00\x6e\x00\x66\x00\x6f\
\x00\x0f\
\x06\xb2\xe7\x27\
\x00\x69\
\x00\x6e\x00\x66\x00\x6f\x00\x72\x00\x6d\x00\x61\x00\x74\x00\x69\x00\x6f\x00\x6e\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x76\x1b\x19\x2f\xc3\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
