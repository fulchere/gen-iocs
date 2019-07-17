import xlrd
import os
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
from itertools import izip

source = '../docs/FTS Tracker.xlsx'

wb = xlrd.open_workbook(source, on_demand=True)
ws = wb.sheet_by_name('.db Parsing')

header = [h for h in ws.row_values(0)]
items = zip(*[ws.col_values(header.index(col), 1) for col in
            (u'hostname', u'ch', u'serves this sensor')])

seen = set()
iocs = OrderedDict()

# Build source data
data = []
odd = ["A","C","E","G"]
even = ["B","D","F","H"]
Jenkinsfile_names = {'the_names' : []}
for name, channel, sensor in items:
    if name == "":
        continue

    # Convert LS1_CA01:FTHS_N0002 to ls1-ca01-fths-n0002
    name = name.strip()
    name_sensor = name
    name_l = list(name)
    name_l[3],name_l[8],name_l[13] = "-","-","-"
    name = "".join(name_l).lower()

    if sensor != "" and sensor != 0.0:
        # Convert LS1:CA01:FTS:TX481A to LS1_CA01:FTHS_TX481A
        sensor_l = list(sensor)
        if len(sensor_l) == 18:
            sensor_l.insert(10, "H")
        sensor_l[3],sensor_l[13] = "_","_"
        sensor = "".join(sensor_l)
    else:
        continue

    # Create data package
    if name not in iocs:
        iocs[name] = {
            'name': name,
            'name_sensor': name_sensor,
            'dct' : []
            }
    specific_ioc = iocs[name]
    specific_ioc['dct'].append(sensor)
    if name not in Jenkinsfile_names['the_names']:
        Jenkinsfile_names['the_names'].append(name)

# Create st.cmd file
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('template.st.cmd')

# Create Makefile
env_two = Environment(loader=FileSystemLoader('./'))
template_two = env_two.get_template('template.Makefile')

# Create Jenkinsfile
env_three = Environment(loader=FileSystemLoader('./'))
template_three = env_three.get_template('template.Jenkinsfile')

txt_file_pth = 'folder_names'    
with open(txt_file_pth, 'wb') as txtfile:

    for iocname, iocdata in iocs.items():
        txtfile.write("ioc-" + iocname + '\n')    
        
        iocname = "ioc-" + iocname
        target = '../iocBoot/%s/st.cmd' % iocname
        target_pth = target[:-7]

        if not os.path.exists(target_pth):
            os.makedirs(target_pth)
        with open(target, 'wb') as f:
            f.write(template.render(iocdata))

        # Make the target executable
        os.chmod(target, 0o755)

        # Create Makefile
        target = '../iocBoot/%s/Makefile' % iocname
        target_pth = target[:-9]
        if not os.path.exists(target_pth):
            os.makedirs(target_pth)
        with open(target, 'wb') as f:
            f.write(template_two.render(iocdata))
        
        # Printed after every folder created
        print '%s Done' % iocname

    # Create Jenkinsfile
    target = '../Jenkinsfile'
    with open(target, 'wb') as f:
        f.write(template_three.render(Jenkinsfile_names))

txtfile.close()

