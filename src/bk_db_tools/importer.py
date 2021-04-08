import sys
from pathlib import Path

class Importer: 
    extension = ""
    
    def __init__(self, db):
        self.db = db
    
    def do_import(self, params):
        filePath = Path(params)
        
        if filePath.is_dir():
            # only files of extension.
            for currentFile in Path(filePath).glob(self.extension):
                self.import_file(currentFile)
                print("Imported: " + str(currentFile.absolute()))
        elif Path(filePath).is_file():
            self.import_file(filePath)
            print("Imported: " + str(filePath))
        else:
            print("folder or file not found." )
            sys.exit(1)

    def import_file(self, filePath):
        """
        child classes should do work here.
        """
        
    def create_table(self, tableName, columnNames, row1):
        sql = f'DROP TABLE IF EXISTS {tableName}'
        self.db.execute(sql)

        columnCount = len(columnNames)
        columnType = self.get_sqlite_column_type(row1[0])
        sql = f'CREATE TABLE {tableName} ({columnNames[0]} {columnType}'
        
        for i in range(1,columnCount):
            columnType = self.get_sqlite_column_type(row1[i])
            sql += ', ' + columnNames[i] + ' ' + columnType
        sql += ');'

        self.db.execute(sql)

    def insert_table_str(self, tableName, columnNames):
        columnCount = len(columnNames)
        sql = f'INSERT INTO {tableName} ({columnNames[0]}'
        
        for i in range(1,columnCount):
            sql += ', ' + columnNames[i]
        sql += ') VALUES (?'
        for i in range(1,columnCount):
            sql += ', ?'
        sql += ');'

        return(sql)
        
    def get_sqlite_column_type(self, value):
        if isinstance(value, int):
            return 'INT'
        if isinstance(value, float):
            return 'REAL'
        if isinstance(value, str):
            if value.isdigit():
                return 'INT'
            try:
                float(value)
                return 'REAL'
            except ValueError:
                return 'TEXT'
        
        #safe enough default for sqlite
        return 'TEXT'
