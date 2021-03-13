import sys
from pathlib import Path
from .database import Database
from settings import Settings
from src import xlsx_exporter

class SqlFileExecuter: 
    db = Database()
    outputExtension = ".xlsx"
    
    def do_executions(self, params):
        """
        do_executions has to be the funnest method name I've ever come up with. :-)
        """
    
        if 1 < len(params) and params[1] == "csv":
            self.outputExtension = ".csv"
        
        filePath = Path(Settings.modulePath) / params[0]
    
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
                continue
            
            if self.outputExtension == ".xlsx":
                if needFile:
                    outputPath = filePath.parent / (filePath.stem + '.xlsx')
                    xlsxExporter = xlsx_exporter.XlsxExporter()
                    xlsxExporter.delete_all_sheets(outputPath)
                    needFile = False;
                
                worksheetName = "Sheet"
                if statementIndex > 0:
                    worksheetName = worksheetName + str(statementIndex)

                xlsxExporter.export_rows(outputPath, rows, worksheetName)
                
            if self.outputExtension == ".csv":
                #TODO
                print("csv needs to be codded")
            
        