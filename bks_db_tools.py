#BKsDBTools.py
import argparse
import sys
import importlib
from settings import Settings
from src import csv_importer
from src import sql_file_executer
from src import xlsx_importer
from src import xlsx_exporter
from pathlib import Path
from pydoc import locate


parser = argparse.ArgumentParser(
    #prog='BKsDBTools',
    #usage='%(prog).py [options] path',
    description='Tools for importing and exporting into a DB.',
    epilog='Enjoy the program! :)')

group = parser.add_mutually_exclusive_group(required=True)
'''
# TODO not yet implemented

group.add_argument(
    '-ec',
    '--exportcsv',
    type=str,
    metavar='PATH, TABLE, or ALL',
    help='Export sql results or table as a csv file. ALL for all tables.')
'''
group.add_argument(
    '-es2x',
    '--exportsql2xlsx',
    type=str,
    metavar='PATH',
    help='Export sql results as an excel file.')

group.add_argument(
    '-es',
    '--executesql',
    type=str,
    metavar='PATH',
    nargs='+',
    help='Executes a sql file, or a folder containing sql files. 2nd argument can be csv or xlsx (default) for SELECT results output.')

group.add_argument(
    '-ic',
    '--importcsv',
    type=str,
    metavar='PATH',
    help='Import csv file, or a folder containing csv files.')

group.add_argument(
    '-ix',
    '--importxlsx',
    type=str,
    metavar='PATH',
    help='Import excel file, or a folder containing xlsx files.')

group.add_argument(
    '-s',
    '--script',
    type=str,
    metavar='FILE',
    nargs='+',
    help='Runs a saved script.')

group.add_argument(
    '-xd',
    '--xlsxdump',
    type=str,
    metavar='TABLE NAME',
    #nargs=1, #TODO set higher if we want to set an output file by name.
    help='Export tables or views to an xlsx data dump file. Uses % as wildcard. % for all.')	

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()
'''
if args.exportcsv:
    # TODO not yet implemented
    print(args.exportcsv)
'''
if args.exportsql2xlsx:	
    xlsxExporter = xlsx_exporter.XlsxExporter()
    xlsxExporter.export_sql(args.exportsql2excel)

if args.executesql:
    sqlFileExecuter = sql_file_executer.SqlFileExecuter()
    sqlFileExecuter.do_executions(args.executesql)
    
if args.importcsv:
    csvImporter = csv_importer.CsvImporter()
    csvImporter.do_import(args.importcsv)

if args.importxlsx:
    xlsxImporter = xlsx_importer.XlsxImporter()
    xlsxImporter.do_import(args.importxlsx)

if args.script:
    filePath = Path(Settings.modulePath) / args.script[0]

    if not filePath.is_file():
        print("File not found." )
        sys.exit(1)
    
    #20/80 rule and KISS. simple conversion of file name to class name.
    temp = filePath.stem.split('_')
    className = ''.join(ele.title() for ele in temp)
    
    classLocation = str(filePath.parent).replace('\\', '.')
    classLocation = classLocation + '.' + filePath.stem + '.' + className
    
    scriptClass = locate(classLocation)
    
    #20/80 rule and KISS. Each script will have a runScript method
    if scriptClass is None:
        print('Class not found. Check class name.')
        sys.exit(1)

    script = scriptClass()
    
    #TODO someday could convert args.script (a list) to actual method paramaters.
    #https://stackoverflow.com/questions/9539921/how-do-i-create-a-python-function-with-optional-arguments
    script.run_script(args.script)
    
if args.xlsxdump:	
    xlsxExporter = xlsx_exporter.XlsxExporter()
    xlsxExporter.export_tables(args.xlsxdump)    
