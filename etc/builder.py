from iocbuilder import AutoSubstitution
from iocbuilder.arginfo import *
from iocbuilder.modules.asyn import AsynPort
from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, pvAccessCPP, pvDatabaseCPP, pvDataCPP, normativeTypesCPP,\
    makeTemplateInstance


class pvaDriverTemplate(AutoSubstitution):
    TemplateFile = "pvaDriver.template"


class pvaDetector(AsynPort):
    """Creates a pvAccess detector"""
    Dependencies = (ADCore, pvAccessCPP, pvDatabaseCPP, pvDataCPP, normativeTypesCPP)
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    _SpecificTemplate = pvaDriverTemplate

    def __init__(self, PORT, PVNAME, BUFFERS = 50, MEMORY = 0, PRIORITY = 0, STACKSIZE = 0, **args):
        # Init the superclass (AsynPort)
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    # __init__ arguments
    ArgInfo = ADBaseTemplate.ArgInfo + _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        PORT = Simple('Port name for the detector', str),
        PVNAME = Simple('PV Name', str),
        BUFFERS = Simple('Maximum number of NDArray buffers to be created for plugin callbacks', int),
        MEMORY = Simple('Max memory to allocate, should be maxw*maxh*nbuffer for driver and all attached plugins', int),
        PRIORITY = Simple('Max buffers to allocate', int),
        STACKSIZE = Simple('Max buffers to allocate', int))

    # Device attributes
    LibFileList = ['pvaDriver']
    DbdFileList = ['pvaDriverSupport']

    def Initialise(self):
        print '# pvaDriverConfig(portName, pvName, maxBuffers, maxMemory, priority, stackSize)'
        print 'pvaDriverConfig("%(PORT)s", %(PVNAME)s, %(BUFFERS)d, %(MEMORY)d, %(PRIORITY)d, %(STACKSIZE)d)' % self.__dict__
