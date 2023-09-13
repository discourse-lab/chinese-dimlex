import codecs
from lxml import etree
import sys
from collections import defaultdict
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

xmlp = etree.XMLParser(strip_cdata=False, resolve_entities=False, encoding='utf-8')

def create_graphs(xml):

    tree = etree.parse(xml, parser=xmlp).getroot()
    
    amb_dict = defaultdict(int)
    sensegroups_dict = defaultdict(int)
    detailed_sensegroups_dict = defaultdict(int)
    for entry in tree.findall('.//entry'):
        amb_degree = len(entry.findall('.//pdtb3_relation'))
        amb_dict[amb_degree] += 1
        sensegroup = set(sorted([x.get('sense').split(':')[0] for x in entry.findall('.//pdtb3_relation')]))
        sensegroups_dict[','.join(sensegroup)] += 1
        detailed_sensegroup = set(sorted([':'.join(x.get('sense').split(':')[0:2]) for x in entry.findall('.//pdtb3_relation')]))
        detailed_sensegroups_dict[','.join(detailed_sensegroup)] += 1
        
    
    ambkeys = sorted(k for k in amb_dict)
    ambvals = [amb_dict[k] for k in ambkeys]
    amb_od = pd.DataFrame({'Number of Senses': ambkeys, 'Connectives': ambvals})
    amb_plot = sns.barplot(x='Number of Senses', y='Connectives', data=amb_od,
                palette = 'hls',
                saturation = 8,
                )
    fig = amb_plot.get_figure()
    fig.savefig("amb_plot.png")
    
    sgkeys = sorted(sensegroups_dict, key = lambda x: x[0])
    sgvals = [sensegroups_dict[k] for k in sgkeys]
    sg_od = pd.DataFrame({'Senses': sgkeys, 'Connectives': sgvals})
    plt.figure(figsize=(15,12))
    sg_plot = sns.barplot(x='Senses', y='Connectives', data=sg_od,
                palette = 'hls',
                saturation=8,
                )
    fig = sg_plot.get_figure()
    fig.autofmt_xdate()
    fig.savefig('sg_plot.png')
    
    detailedsgkeys = sorted(detailed_sensegroups_dict, key = lambda x: x[0])
    detailedsgvals = [detailed_sensegroups_dict[k] for k in detailedsgkeys]
    detailedsg_od = pd.DataFrame({'Senses': detailedsgkeys, 'Connectives': detailedsgvals})
    plt.figure(figsize=(25,20))
    detailedsg_plot = sns.barplot(x='Senses', y='Connectives', data=detailedsg_od,
                palette = 'hls',
                saturation=8,
                )
    fig = detailedsg_plot.get_figure()
    fig.autofmt_xdate()
    fig.savefig('detailed_sg_plot.png')
    
    

def main():
    
    create_graphs('chinese_dimlex.xml')


if __name__ == '__main__':
    main()