from ctypes import *

#Map MS types to ctypes for clarity
WORD = c_ushort           #unsigned short in C, int/long in python
DWORD = c_ulong           #unsigned long in C, int/long in python
LPBYTE = POINTER(c_ubyte) #char in C, int/long in python
LPTSTR = POINTER(c_char)  #char in C, 1 char string in python
HANDLE = c_void_p         #void * in C, int/long or name in python  

#Constants
DEBUG_PROCESS = 0x00000001 
CREATE_NEW_CONSOLE = 0x00000010


#Structs for CreateProcessA() function
#This process gets a process to run via the debugger
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb",                  DWORD),
        ("lpReserved",          LPTSTR),
        ("lpDesktop",           LPTSTR),
        ("lpTitle",             LPTSTR),
        ("dwX",                 DWORD),
        ("dwY",                 DWORD),
        ("dwXSize",             DWORD),
        ("dwYSize",             DWORD),
        ("dwXCountChars",       DWORD),
        ("dwYCountChars",       DWORD),
        ("dwFillAttribute",     DWORD),
        ("dwFlags",             DWORD),     #command line flags
        ("wShowWindow",         WORD),      #should this be a separate window?
        ("cbReserved2",         WORD),
        ("lpReserved2",         LPBYTE),
        ("hStdInput",           HANDLE),    #input
        ("hStdOutput",          HANDLE),    #output
        ("hSTDError",           HANDLE),    #errors
    ]

class PROCESS_INFORMATION(Structure):
    _fields_ =[
        ("hProcess",            HANDLE),
        ("hThread",             HANDLE),
        ("dwProcessId",         DWORD),     #the PID
        ("dwThreadId",          DWORD),
    ]

