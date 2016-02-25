#!/usr/bin/env python

import sys
import math
import csv
import copy
import shutil
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

print YELLOW + "Welcome to Metabolome Analysis Platform :)" + ENDC

class MAP:
    def __init__(self):
        pass

    def zscore(self, name, value_name='fructose'):
        f = open(name,'rU')
        data = csv.reader(f)
        value_up, id, id_data, means, dev_all, disps, zvalues_all, metabolite = [],[],[],[],[],[],[],[]
        for i in data:
            for j in range(len(i)):
                value_up.append(i[j].upper())
        f.seek(0,0)

        sw = 0
        while sw == 0:
            #value_name = raw_input('Input name of value : ')
            for i in data:
                if value_name.upper() in value_up:
                    sw += 1
            if sw == 0:
                print RED + 'Sorry,that value name does not exist' + ENDC
            f.seek(0,0)

        x = 0
        for i in data:
            x = int(value_up.index(value_name.upper()))
            if x != 0:
                break
        f.seek(0,0)

        for row in data:
            id.append(row[2])
            id_data.append(row[x:])
        f.seek(0,0)
        metabolite.append(id_data[0])
        id_data.pop(0)

        id_data_n = copy.deepcopy(id_data)
        for i in range(len(id_data_n)):
            while '' in id_data_n[i]:
                id_data_n[i].remove('')
            while 0 in id_data_n[i]:
                id_data_n.remove(0)

        #calculating mean
        for i in range(len(id_data_n)):
            total = 0.0
            for j in range(len(id_data_n[i])):
                total = total + float(id_data_n[i][j])
            if len(id_data_n[i]) == 0:
                mean = 0
            else:
                mean = total / float(len(id_data_n[i]))
            means.append(mean)

        #calculating difference and dispersion
        for i in range(len(id_data_n)):
            dev,dif = 0.0,0.0
            devs = []
            for j in range(len(id_data_n[i])):
                dif = float(id_data_n[i][j]) - float(means[i])
                dev = dev + dif ** 2
                devs.append(dev)
            dev_all.append(devs)
            if sum(dev_all[i]) == 0:
                disp = 0
            else:
                disp = math.sqrt(sum(dev_all[i]) / len(dev_all[i]))
            disps.append(disp)

        #calculating the z-value
        z = 0
        for i in range(len(id_data)):
            zvalues = []
            for j in range(len(id_data[i])):
                zvalue = 0
                if id_data[i][j] == '' or id_data[i][j] == 0:
                    zvalue = '0'
                else:
                    zvalue = (float(id_data[i][j]) - float(means[i])) / disps[i]
                zvalues.append(zvalue)
            zvalues_all.append(zvalues)

        top = []
        top.append(id[0])
        id.pop(0)
        for i in range(len(metabolite[0])):
                top.append(metabolite[0][i])
        for i in range(len(zvalues_all)):
                zvalues_all[i].insert(0,id[i])
        zvalues_all.insert(0,top)

        zvalues_tab = copy.deepcopy(zvalues_all)
        for i in range(len(zvalues_tab)):
            for j in range(len(zvalues_tab[i])):
                zvalues_tab[i][j]
        name2 = name.replace('csv','txt')
        f = open(name2,'w')
        for i in range(len(zvalues_tab)):
            for j in range(len(zvalues_tab[i])):
                f.write(str(zvalues_tab[i][j]))
                f.write('\t')
            f.write('\n')
        f.close()
        print RED + "{:<12}".format('(z-scored)') + BLUE + "{:<20}".format(name) + YELLOW + '  ->  ' + BLUE + name2 + ENDC

    def ranking(self, name, value):
        f = open(name,'rU')
        data = csv.reader(f)
        value_up, id, id_data, ranking = [],[],[],[]

        for i in data:
            for j in range(len(i)):
                value_up.append(i[j].upper())
        f.seek(0,0)

        sw = 0
        while sw == 0:
            #value_name = raw_input('Input value name: ')
            value_name = value
            for i in data:
                if value_name.upper() in value_up:
                    sw += 1
            if sw == 0:
                print 'That value name does not exist'
            f.seek(0,0)

        x = int(value_up.index(value_name.upper()))
        for row in data:
            id.append(row[2])
            id_data.append(row[x])
        f.seek(0,0)

        for i in range(len(id_data)):
            num = []
            num.append(id[i])
            if i == 0:
                num.append(id_data[i])
            elif id_data[i] == '':
                num.append(0)
            else:
                num.append(float(id_data[i]))
            ranking.append(num)

        rank = sorted(ranking, key = lambda x: x[1], reverse = True)
        #print rank
        name2 = name.replace('.csv','_ranking.txt')
        f = open(name2, 'w')
        z = 1
        for i in range(len(rank)):
            f.write(str(z))
            f.write('\t')
            for j in range(len(rank[i])):
                f.write(str(rank[i][j]))
                f.write('\t')
            f.write('\n')
            z += 1
        f.close()
        name2 = name.replace('.csv','_ranking.txt')
        print RED + "{:<12}".format('(ranked)') + BLUE + "{:<20}".format(name) + YELLOW + '  ->  ' + BLUE + name2 + ENDC

    def finalize(self):
        pass
