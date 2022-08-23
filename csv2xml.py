import csv
import codecs
import re
from lxml import etree
import sys
from collections import defaultdict


def main():

    rows = csv.reader(codecs.open(sys.argv[1]), delimiter=',')
    entries = defaultdict(list)
    for row in rows:
        entry, variation, rel, postag, en_trans, example = row
        entries[entry].append([variation, rel, postag, en_trans, example])

    root = etree.Element('dimlex')
    doc = etree.ElementTree(root)
    nodeid = 1

    cats = set()
    senses = set()
    
    for entry in entries:
        node = etree.Element('entry')
        node.set('id', 'c'+str(nodeid))
        node.set('word', entry.strip())
        orths = etree.Element('orths')
        orth = etree.Element('orth')
        orth.attrib['type'] = 'cont' if not re.search('\s', entry) else 'discont'
        orth.attrib['canonical'] = '1'
        orth.attrib['onr'] = str(nodeid) + 'o1'
        part = etree.Element('part')
        part.attrib['type'] = 'single' if not re.search('\r', entry) else 'phrasal'
        part.text = entry.strip()
        orth.append(part)
        orths.append(orth)
        orthid = 2
        for inst in entries[entry]:
            if inst[0]:
                orth = etree.Element('orth')
                orth.attrib['type'] = 'cont' if not re.search('\r', inst[0]) else 'discont'
                orth.attrib['canonical'] = '0'
                orth.attrib['onr'] = str(nodeid) + 'o'+str(orthid)
                part = etree.Element('part')
                part.attrib['type'] = 'single' if not re.search('\r', inst[0]) else 'phrasal'
                part.text = inst[0].strip()
                orth.append(part)
                orths.append(orth)
                orthid += 1
        node.append(orths)
        syn = etree.Element('syn')
        catnode = etree.Element('cat')
        catnode.text = inst[2]
        cats.add(inst[2])
        syn.append(catnode)
        for inst in entries[entry]:
            sem = inst[1]
            sem = sem.strip()
            sem = re.sub(r'\.', ':', sem)
            sem = sem.split(':')[0].upper() + ':' + ':'.join(sem.split(':')[1:])
            senses.add(sem)
            postag = inst[2]
            en_eq = inst[3]
            ex = inst[4]
            semnode = etree.Element('sem')
            relnode = etree.Element('pdtb3_relation')
            relnode.set('sense', sem)
            exnode = etree.Element('example')
            exnode.text = ex.strip()
            en_eqnode = etree.Element('english_equivalent')
            en_eqnode.text = en_eq.strip()
            semnode.append(relnode)
            semnode.append(exnode)
            semnode.append(en_eqnode)
            syn.append(semnode)

        node.append(syn)
        root.append(node)
            
        nodeid += 1
        
    doc.write('chinese_dimlex.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)

    
if __name__ == '__main__':
    main()
