from pipython import GCSDevice

__pidevice = GCSDevice()

def search_usb():
    print('Searching for USB devices ...')
    print(__pidevice.EnumerateUSB())
    
def search_tcp():
    print('Searching for TCP/IP devices ...')
    print(__pidevice.EnumerateTCPIPDevices())
    
def search_all():
    search_usb()
    search_tcp()

def select_device():
    """ This funcitons opens a window to select a PI device. You need to install the PI Software Suite to use this. """
    __pidevice.InterfaceSetupDlg()