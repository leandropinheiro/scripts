#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from netaddr import IPAddress

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Address Custom para CSV')
parser.add_argument('File', metavar='In_File', type=str, help='Arquivo com os comandos exportados do Fortigate')
parser.add_argument('-o', metavar='Out_File', dest='Output', help='Define o file name de saída, padrão [In_File].csv')

args = parser.parse_args()

Input = args.File

if str(args.Output) == 'None':
    Output = Path(str(Input)).stem + ".csv"

else:
    Output = args.Output

print("Argumentos:", vars(args))

print("Arquivo de Configuração:", Input)
print("Arquivo de Saída:", Output, "\n")

# Abrir Aquivo

print("Processando:", Input, "\n")

with open(Input) as In:
    line = In.readline() # Le a primeira linha
    
    line_out = '"edit";"type";"associated-interface";"address";"visibility";"allow-routing";"comment"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    while line:
        cli = line.lstrip(' ')
        command = cli.split()
        
        if command[0] == 'config': # Verifica se a linha corresponde a CONFIG
            correto = 'Seu arquivo deve iniciar com: "config firewall address"\n'
            errado = 'config'
            if command[1] == 'firewall': # Verifica se a linha corresponde a CONFIG FIREWALL
                errado = 'config firewall'
                if command [2] == 'address': # Verifica se a linha corresponde a CONFIG FIREWALL ADDRESS
                    print('!', end='')
                else:
                    print('Arquivo Incorreto!!!\n')
                    for x in range(2, len(command)):
                        errado = errado + ' ' + command[x]
                    print('Seu arquivo inicia com: ' + errado)
                    print(correto)
                    quit()
            else:
                print('Arquivo Incorreto!!!\n')
                for x in range(1, len(command)):
                    errado = errado + ' ' + command[x]
                print('Seu arquivo inicia com: ' + errado)
                print(correto)
                quit()

        elif command[0] == 'end': # Verifica se a linha corresponde a END
            print('                                                   ', end='\r')
            print('*')

        elif command[0] == 'edit':  # Verifica se a linha corresponde a EDIT
            print('^', end='')
            
            obj_edit = command[1]

            for x in range(2, len(command)):
                obj_edit = obj_edit + ' ' + command[x]
            
            #obj_edit = obj_edit.replace('"', '')
            obj_type = '"subnet"'
            obj_addr = '"-"'
            obj_iface = '"-"'
            obj_visibility ='"True"'
            obj_allowrouting = '"Disable"'
            obj_comment = '"-"'

        elif command[0] == 'next':  # Verifica se a linha corresponde a NEXT
            print('                                                   ', end='\r')
            
            line_out = obj_edit
            line_out = line_out + ";" + obj_type.upper()
            line_out = line_out + ";" + obj_iface
            line_out = line_out + ";" + obj_addr
            line_out = line_out + ";" + obj_visibility.upper()
            line_out = line_out + ";" + obj_allowrouting.upper()
            line_out = line_out + ";" + obj_comment

            buffer_out.append(line_out)


        elif command[0] == 'set':  # Verifica se a linha corresponde a SET
            print('.', end='')

            if command[1] == 'type': # Verifica o TYPE do objeto
                if command[2] == 'fqdn':
                    obj_type = '"' + command[2] + '"'
                elif command[2] == 'iprange':
                    obj_type = '"' + command[2] + '"'
            
            if command[1] == 'associated-interface':
                obj_iface = '"' + command[2].replace('"', '') + '"'
            
            if command[1] == 'start-ip':
                obj_addr = '"' + command[2]
            
            if command[1] == 'end-ip':
                obj_addr = obj_addr + "-" + command[2] + '"'
            
            if command[1] == 'subnet':
                obj_addr = '"' + command[2] + "/" + str(IPAddress(command[3]).netmask_bits()) + '"'
            
            if command[1] == "comment":
                obj_comment = command[2]

                for x in range(3, len(command)):
                    obj_comment = obj_comment + ' ' + command[x]
                
                obj_comment = '"' + obj_comment.replace('"', '') + '"'

                #obj_comment = obj_comment.replace('"', '')

            if command[1] == "allow-routing":
                obj_allowrouting = '"' + command[2] + '"'
        
        line = In.readline() # Le a proxima linha
    
    with open(Output, 'w') as Out:
        for x in range(len(buffer_out)):
           print(buffer_out[x])
           line = buffer_out[x] + '\n'
           Out.write(line)
