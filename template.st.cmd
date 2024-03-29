#!../../bin/linux-x86_64/fths

# !!! This file was autogenerated by gen-iocs/gen.py

< envPaths

epicsEnvSet("LOCATION", "Rack Group {{ name_sensor }}")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)")

## Register all support components
dbLoadDatabase("${TOP}/dbd/fths.dbd",0,0)
fths_registerRecordDeviceDriver(pdbbase)


drvAsynIPPortConfigure("dev1","{{ name }}:5000", 0, 0, 0)


## Load first record instance
dbLoadRecords("../../db/cryocon.db","P={{ name_sensor }}")


## Load the rest of the record instances
{%- for i in range((dct.__len__()//2)) %}
dbLoadRecords("${TOP}/db/fths.db", "SRC={{ dct[2*i] }},SRC2={{ dct[(2*i)+1] }},P={{ name_sensor }}")
{%- endfor %}


## load Asyn
dbLoadRecords("$(EPICS_BASE)/db/asynRecord.db","P={{ name_sensor }}:,R=asyn,PORT=dev1,ADDR=0,OMAX=40,IMAX=40")


## Last line
iocInit()

