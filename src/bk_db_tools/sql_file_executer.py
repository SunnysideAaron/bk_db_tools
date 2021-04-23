import sys
from pathlib import Path

from .xlsx_exporter import XlsxExporter

class SqlFileExecuter: 
    outputExtension = ".xlsx"
    
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db 
    
    def do_executions(self, params):
        """
        do_executions has to be the funnest method name I've ever come up with. :-)
        """
    
        if 1 < len(params) and params[1] == "csv":
            self.outputExtension = ".csv"
        
        filePath = Path(params[0])
    
        if filePath.is_dir():
            # only files of sql extension.
            for currentFile in Path(filePath).glob("*.sql"):
                self.execute_sql_file(currentFile)
                print("Executed " + str(currentFile.absolute()))
        elif Path(filePath).is_file():
            self.execute_sql_file(filePath)
            print("Executed: " + str(filePath))
        else:
            print("folder or file not found." )
            sys.exit(1)
            
    def execute_sql_file(self, filePath):
        with open(filePath, newline='') as file:
            allsql = file.read()
            file.close()
        
        statements = allsql.split(";")
        
        needFile = True
        
        for statementIndex, statement in enumerate(statements):
            if not statement:
                continue

            rows = self.db.query(statement)
            
            if not rows:
                self.db.commit()
                continue
            
            if self.outputExtension == ".xlsx":
                if needFile:
                    outputPath = filePath.parent / (filePath.stem + '.xlsx')
                    xlsxExporter = XlsxExporter(self.settings, self.db)
                    xlsxExporter.delete_all_sheets(outputPath)
                    needFile = False;
                
                worksheetName = "Sheet"
                if statementIndex > 0:
                    worksheetName = worksheetName + str(statementIndex)

                xlsxExporter.export_rows(outputPath, rows, worksheetName)
                
            if self.outputExtension == ".csv":
                #TODO
                print("csv needs to be coded")
            
        