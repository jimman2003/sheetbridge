from zipfile import ZipFile
import xml.etree.ElementTree as ET

from lark import Lark,Transformer,Token




l = Lark.open('grammar.lark')

class PythonTransformer(Transformer):
      def range(self,r):
        [start,end] =r 
        return f'xl("{start}:{end}")'
      def cell(self,r):
        (_,cell)=r
        return f'xl("{cell}")'
      
      def function(self,s):
        [excel_function,args]=s
        changed_names={
            'AVERAGE':'mean'
        }
        python_name=changed_names.get(excel_function,excel_function.lower())
        match excel_function.type:
          case 'SUFFIX_FUNCTION':
            return f'{args}.{python_name}()'
          case 'PREFIX_FUNCTION':
            return f'{python_name}({args})'
         
      
    

with ZipFile('../test.xlsx') as myzip:
    with myzip.open('xl/worksheets/sheet1.xml') as myfile:
        content = myfile.read().decode('utf-8')
root=ET.fromstring(content)

def get_formulas():
    ns={'ns':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for tag in root.iterfind(".//ns:c/ns:f",ns):
      if "_xlfn._xlws.PY" not in tag.text:
          yield tag.text

for formula in get_formulas():
    print(formula)
    tree =l.parse(formula)
    print(tree)
    print(PythonTransformer().transform(tree))
