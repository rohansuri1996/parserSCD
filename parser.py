import os
import xml.etree.ElementTree as ET

def foo():
    json = {}

    file_name= 'SCD.xml'
    full_file= os.path.abspath(os.path.join( 'data' , file_name))
    #SCD_filepath="/Users/rohansuri/Desktop/ResearchProject/parser/SCD.xml" #gives the file path for the xml(SCD) by yourself

    tree=ET.parse(full_file) #some xml element in this tree, now we can perform queries on it
    root=tree.getroot()

    #print(root[2].tag + " hi rohan") #finds child of root and here it finds communication tag

    communication= root[2]

    def find(node, value):
        return node.find('{http://www.iec.ch/61850/2006/SCL}' + value)

    def findall(node, value):
        return node.findall('{http://www.iec.ch/61850/2006/SCL}' + value)

    def format_mac(value):
        return value.lower().replace('-', ':')

    communication = find(root, 'Communication')
    aps = findall(communication[0], 'ConnectedAP')

    print("\n ****** AP NAMES ****** \n")

    for ap in aps:
        ied_name = ap.get('iedName') 
        json[ied_name]=""
        #print(ied_name)
        
        gses = findall(ap, 'GSE')
        publish_goose = []
        for gse in gses:
            address = find(gse, 'Address')
            privates = findall(address, 'P')
            for p in privates:
                if p.get('type') == 'MAC-Address':
                    publish_goose.append(format_mac(p.text))
                    (p.text)
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

    print("\n ****** AP IP ****** \n")
    for ap,name in zip(aps,list(json.keys())):
        address = find(ap, 'Address')
        privates = findall(address, 'P')
        for p in privates:
            if p.get('type') == 'IP':
                ip = p.text
                json[name] = ip
                #print(ip)
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

    return json

if __name__ == '__main__':
    foo()