from pipython import GCSDevice, pitools
from pipython import PILogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
import logging

class turntable:
    def __init__(self):
        self.REFMODES = REFMODES = ['FNL', 'FRF']
    
    def __del__(self):
        print('disconnecting: {}'.format(self.device.qIDN().strip()))
        self.device.CloseConnection()

    def connect_device(self, model, sn, stage):
        self.CONTROLLER_MODEL = model
        self.CONTROLLER_SN = sn
        self.STAGE = stage
        self.device = GCSDevice(self.CONTROLLER_MODEL)
        self.device.ConnectUSB(serialnum=self.CONTROLLER_SN)
        print('connected: {}'.format(self.device.qIDN().strip()))
        
        # Show the version info which is helpful for PI support when there
        # are any issues.
        if self.device.HasqVER():
            print('version info:\n{}'.format(self.device.qVER().strip()))
            
        print('initialize connected stages...')
        pitools.startup(self.device, stages=self.STAGE, refmodes=self.REFMODES)
        
        self.min_range = self.device.qTMN()
        self.max_range = self.device.qTMX()
        
        # The GCS commands qTMN() and qTMX() used above are query commands.
        # They don't need an argument and will then return all available
        # information, e.g. the limits for _all_ axes. With setter commands
        # however you have to specify the axes/channels. GCSDevice provides
        # a property "axes" which returns the names of all connected axes.
        # So lets move our stages...
    
    def test_stages(self):
        # Some devices can have multiple stages. This functions tests the broders of every stage even though the turntables have only one. So no need to go through all the stages and axes, but just let it stay to maybe use it for other devices from PI
        for axis in self.device.axes:
            for target in (self.min_range[axis], self.max_range[axis]):
                print('move axis {} to {:.2f}'.format(axis, target))
                self.device.MOV(axis, target)

                # To check the "on target state" of an axis there is the GCS command
                # qONT(). But it is more convenient to just call "waitontarget".

                pitools.waitontarget(self.device, axes=axis)

                # GCS commands usually can be called with single arguments, with
                # lists as arguments or with a dictionary.
                # If a query command is called with an argument the keys in the
                # returned dictionary resemble the arguments. If it is called
                # without an argument the keys are always strings.

                position = self.device.qPOS(axis)[axis]  # query single axis
                # position = self.device.qPOS()[str(axis)] # query all axes
                print('current position of axis {} is {:.2f}'.format(axis, position))

        print('done')
    
    ## Move Functions
    def home(self, wait=True):
        return self.move_absrot(0, wait)
    
    def move_relrot(self, deg, wait=True):
        curr_pos = self.get_pos()
        return self.move_absrot(curr_pos + deg, wait)
    
    def move_absrot(self, deg, wait=True):
        self.device.MOV(self.device.axes[0], deg)
        if wait:
            pitools.waitontarget(self.device, self.device.axes[0])
        return True
    
    ## Getter Functions
    def get_state(self):
        if turnt.device.qONT()['1']:
            return True
        else:
            return False
    
    def print_state(self):
        if self.get_state:
            print("Device ready")
        else:
            print("Device is moving")
    
    def get_pos(self):
        deg = float(self.device.qPOS()[self.device.axes[0]])
        return deg
    
    def print_pos(self):
        print("Current position is " + str(self.get_pos()))
        
    def get_numaxes(self):
        return self.device.numaxes
    
    def get_vel(self):
        return self.device.qVEL(self.device.axes[0])[self.device.axes[0]]
    
    def print_vel(self):
        print("Velocity is " + str(self.get_vel()))
    
    ## Setter Functions
    def set_vel(self, vel):
        self.device.VEL(self.device.axes[0], vel)
        return True
    
    def set_debugmode(self, on, kind='DEBUG'):
        if on:
            PILogger.setLevel(DEBUG)
        else:
            PILogger.setLevel(logging.NOTSET)