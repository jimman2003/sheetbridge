from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET

with ZipFile('../test.xlsx') as myzip:
    with myzip.open('xl/worksheets/sheet1.xml') as myfile:
        content = myfile.read().decode('utf-8')
root=ET.fromstring(content)    
tokens_spec= [
        ('RANGE',r'[A-Z]+\d+:[A-Z]+\d+'),
        ('CELL',r'[A-Z]+\d+'),
        ('FUNCTION',r'SUM|AVERAGE|MAX|MIN'),
        
    ]
def tokenize(content):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in tokens_spec)
    for mo in re.finditer(tok_regex, content):
        kind = mo.lastgroup
        value = mo.group()
        yield kind, value

# def transpile(cells):
#     find_replace= [
#         {r'SUM\((.+)\)': r'\1.sum()'},
#         {r'([A-Z]+\d+:[A-Z]+\d+)': r'xl("\1")'},
#     ]
#     #tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in tokens_spec)
#     for su in find_replace:
#         for k, v in su.items():
#             cells = re.sub(k, v, cells)
#     return cells
def transpile():
   ns={'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
   for possible_tag in  root.iterfind(".//ns:c",ns):
         if possible_tag.find('ns:f',ns) is not None:
              cells=possible_tag.find('ns:f',ns).text
              for kind, value in tokenize(cells):
                if kind == 'RANGE':
                     print(cells)
                elif kind == 'CELL':
                     print(value)
                elif kind == 'FUNCTION':
                    print(value)
         else:
              print('No formula')
              print(possible_tag.find('ns:v',ns).text)
#print(content)
transpile()