from zipfile import ZipFile
import xml.etree.ElementTree as ET

from lark import Lark,Transformer


with open('grammar.lark') as f:
    grammar = f.read()

l = Lark(grammar)

class PythonTransformer(Transformer):
      def range(self,r):
        [start,end] =r 
        return f'xl("{start}:{end}")'
      def cell(self,r):
        (_,cell),=r
        return f'xl("{cell}")'
      def sum(self,s):
        return f'{s[0]}.sum()'

with ZipFile('../test.xlsx') as myzip:
    with myzip.open('xl/worksheets/sheet1.xml') as myfile:
        content = myfile.read().decode('utf-8')
root=ET.fromstring(content)

def get_formulas():
    ns={'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for tag in root.iterfind(".//ns:c/ns:f",ns):
                 yield tag.text

for formula in get_formulas():
    #print(formula)
    tree =l.parse(formula)
    print(tree.pretty())
    print(PythonTransformer().transform(tree))
