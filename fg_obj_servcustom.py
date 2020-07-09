#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from netaddr import IPAddress

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Service Custom para CSV')
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
    
    line_out = '"EDIT";"PROTOCOL";"SERVICES";"VISILIBITY";"COMMENT"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    while line:
        cli = line.lstrip(' ')
        command = cli.split()
        
        if command[0] == 'config': # Verifica se a linha corresponde a CONFIG
            correto = 'Seu arquivo deve iniciar com: "config firewall service custom"\n'
            errado = 'config'
            if command[1] == 'firewall': # Verifica se a linha corresponde a CONFIG FIREWALL
                errado = 'config firewall'
                if command [2] == 'service': # Verifica se a linha corresponde a CONFIG FIREWALL SERVICE
                    errado = 'config firewall service'
                    if command[3] == 'custom':
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

        elif command[0] == 'next':  # Verifica se a linha corresponde a NEXT
            print('                                                   ', end='\r')
            
            if obj_services == '"':
                obj_services = '"ALL'

            line_out = obj_edit
            line_out = line_out + ";" + obj_proto
            line_out = line_out + ";" + obj_services.rstrip('\n') + '"'
            line_out = line_out + ";" + obj_visibility.upper()
            line_out = line_out + ";" + obj_comment

            buffer_out.append(line_out)

        elif command[0] == 'edit':  # Verifica se a linha corresponde a EDIT
            print('^', end='')
            
            obj_edit = command[1]

            for x in range(2, len(command)):
                obj_edit = obj_edit + ' ' + command[x]
            
            #obj_edit = obj_edit.replace('"', '')
            obj_proto = '"TCP/UDP"'
            obj_services = '"'
            obj_visibility = '"ENABLE"'
            obj_comment = '"-"'

        elif command[0] == 'set':  # Verifica se a linha corresponde a SET
            print('.', end='')

            if command[1] == "protocol":
                obj_proto = '"' + command[2].upper() + '"'

            if command[1] == 'tcp-portrange':
                for x in range(2, len(command)):
                    if ':' in command[x]:
                        service = command[x].split(':')
                        obj_services += 'TCP/' + service[0] + ' (SRC ' + service[1] + ')\n'
                    else:
                        obj_services += 'TCP/' + command[x] + '\n'
            
            if command[1] == 'udp-portrange':
                for x in range(2, len(command)):
                    if ':' in command[x]:
                        service = command[x].split(':')
                        obj_services += 'UDP/' + service[0] + ' (SRC ' + service[1] + ')\n'
                    else:
                        obj_services += 'UDP/' + command[x] + '\n'
            
            if command[1] == 'protocol-number':
                for x in range(2, len(command)):
                        obj_services += 'IP/' + command[x] + '\n'

            if command[1] == 'icmptype':
                for x in range(2, len(command)):
                        obj_services += 'ICMP TYPE/' + command[x] + '\n'
            
            if command[1] == 'icmpcode':
                for x in range(2, len(command)):
                        obj_services += 'ICMP CODE/' + command[x] + '\n'

            if command[1] == "comment":
                obj_comment = command[2]

                for x in range(3, len(command)):
                    obj_comment = obj_comment + ' ' + command[x]
                
                obj_comment = '"' + obj_comment.replace('"', '') + '"'

                #obj_comment = obj_comment.replace('"', '')

            if command[1] == "visibility":
                obj_visibility = '"' + command[2] + '"'
        
        line = In.readline() # Le a proxima linha
    
    with open(Output, 'w') as Out:
        for x in range(len(buffer_out)):
           print(buffer_out[x])
           line = buffer_out[x] + '\n'
           Out.write(line)
