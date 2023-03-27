import argparse, os, subprocess, json
from jinja2 import Template, Environment, FileSystemLoader

'''
Generate a "regression" result from a document.
Obtain the latest_result through "http://portal:8002".
From the results obtained, one adoc is generated.
Kick : python3.7 report_regression.py 
'''

THIS_DIR = os.path.dirname(os.path.abspath(__file__))  

def parser():
  parse = argparse.ArgumentParser(description="Generate a func_regression_report.adoc by Dashboard data")
  parse.add_argument("--output", type=str, default=f"{THIS_DIR}/build/tb/FULL/doc/func_regression_report.adoc", help="Generateed adoc file name")
  parse.add_argument("--port", type=str, default="8003", help="LD dashboard port number")
  parse.add_argument("--project", type=str, default="RHEA_EVT1", help="Project name")
  parse.add_argument("--source", type=argparse.FileType('r'), default=f"{THIS_DIR}/func_regression_report.adoc.jinja", help="Source Jinja file")
  parse.add_argument("--detail", action='store_true', help="Generate more detail")
  return parse

def get_data_ld_dashboard(port ,project):
  return json.loads(subprocess.check_output(f"curl -X GET http://portal:{port}/get_report/{project}".split(" ")).decode('utf-8').replace('\'',''))


def render_adoc(regression_data : dict, **kargs):
  jinja_text = Template(kargs['source'].read())
  return jinja_text.render( **kargs, **regression_data)

def main_regression_report(**kargs):
  
  if not os.path.isdir( os.path.dirname(kargs.get('output')) ):
    os.makedirs( os.path.dirname(kargs.get('output')) )
    
  regression_data = get_data_ld_dashboard(kargs['port'], kargs['project'])
  
  adoc_text = render_adoc(regression_data = regression_data,**kargs)
  
  with open(kargs['output'], 'w') as f_adoc:
    f_adoc.write(adoc_text)
  
  
if __name__ == "__main__":
  args = vars(parser().parse_args())
  main_regression_report(**args)