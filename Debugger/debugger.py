from ctypes import *
from debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass

    def load(self, path_to_exe):
        #dwCreation flag determines how to create the process
        creation_flags = DEBUG_PROCESS

        #instantiate structs
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        #show in separate window
        startupinfo.dwFlags =0x1
        startupinfo.wShowWindow = 0x0

        #init cb var which is the size of the struct
        startupinfo.cb = sizeof(startupinfo)

        #app name, command line args, process attributes, thread attributes, inherithandles (T/F), creation flagsm environment, current dir, startup info, process info
        if kernel32.CreateProcessA(path_to_exe, None, None, None, None, creation_flags, None, None, byref(startupinfo), byref(process_information)):
            print("[*] Process launched!")
            print("[*] PID %d" % process_information.dwProcessId)
        else:
            print("[*] Error: 0x%08x." % kernel32.GetLastError())

