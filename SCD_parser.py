import os
import xml.etree.ElementTree as ET


file_name= 'SCD.xml'
full_file= os.path.abspath(os.path.join( 'data' , file_name))
#SCD_filepath="/Users/rohansuri/Desktop/ResearchProject/parser/SCD.xml" #gives the file path for the xml(SCD) by yourself

tree=ET.parse(full_file) #some xml element in this tree, now we can perform queries on it
root=tree.getroot()

def find(node, value):
    return node.find('{http://www.iec.ch/61850/2006/SCL}' + value)

def findall(node, value):
    return node.findall('{http://www.iec.ch/61850/2006/SCL}' + value)

def format_mac(value):
    return value.lower().replace('-', ':')

substation = find(root, 'Substation')
VoltLevel={}
Bay_attrib=[]
PT_attrib=[]
Volt_value=[]


#for substations
for subs in substation:
    Voltagelevel_name=subs.get('name')
    Bays = findall(subs, 'Bay')
    PTs=findall(subs,'PowerTransformer')
    Volts=findall(subs,'Voltage')
    for Bay in Bays:
        Bay_attrib.append({Voltagelevel_name:Bay.attrib})
        # Bay_attrib.append(Bay.get('name'))
    for PT in PTs:
        PT_attrib.append({Voltagelevel_name:PT.attrib})
        # PT_attrib.append(PT.get('name'))
    for Volt in Volts:
        Volt_value.append({Voltagelevel_name:Volt.attrib})
        # Volt_value.append(Volt.get('name'))
    
    # VoltLevel[Voltagelevel_name] = {
        # 'Bays': Bay_attrib,
        # 'PowerTransformer': PT_attrib, 'Volt_value': Volt_value}


communication = find(root, 'Communication')
aps = findall(communication[0], 'ConnectedAP')


substation = {}

for ap in aps:
    ied_name = ap.get('iedName')
    print(ied_name)
    address = find(ap, 'Address')
    privates = findall(address, 'P')
    for p in privates:
        if p.get('type') == 'IP':
            ip = p.text
    
        break

    gses = findall(ap, 'GSE')
    publish_goose = []
    for gse in gses:
        address = find(gse, 'Address')
        privates = findall(address, 'P')
        for p in privates:
            if p.get('type') == 'MAC-Address':
                publish_goose.append(format_mac(p.text))
                break

    smvs = findall(ap, 'SMV')
    publish_sv = []
    for smv in smvs:
        address = find(smv, 'Address')
        privates = findall(address, 'P')
        for p in privates:
            if p.get('type') == 'MAC-Address':
                publish_sv.append(format_mac(p.text))
                
                break

    substation[ied_name] = {
        'ip': ip,
        'publish': {'goose': publish_goose, 'sv': publish_sv}} 



ieds = findall(root, 'IED')
for ied in ieds:
    ied_name = ied.get('name')
    (ied_name) #all 12 IEDS name
    
     
DataType_Temp = find(root, 'DataTypeTemplates')
LNodes= findall(DataType_Temp, 'LNodeType')

Lnode_attrib=[]

for LNode in LNodes:
    # id_name = Lnode.get('id')
    # InClass= Lnode.get('InClass')
    Lnode_attrib.append(LNode.attrib)


DOTypes= findall(DataType_Temp, 'DOType')

DOType_attrib=[]

for DOType in DOTypes:
    # id_name = Lnode.get('id')
    # InClass= Lnode.get('cdc')
    DOType_attrib.append(DOType.attrib)

EnumTypes= findall(DataType_Temp, 'EnumType')

EnumType_attrib=[]

for EnumType in EnumTypes:
    # id_name = Lnode.get('id')
    EnumType_attrib.append(EnumType.attrib)
