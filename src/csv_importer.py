import csv
from .importer import Importer
from pathlib import Path

class CsvImporter(Importer): 
    extension = "*.csv"

    def import_file(self, filePath):
        tableName = Path(filePath).stem
        
        with open(filePath, newline='') as file:
            reader = csv.reader(file)
            columnNames = next(reader)
            row1 = next(reader)
            
            self.create_table(tableName, columnNames, row1)
            sql = self.insert_table_str(tableName, columnNames)
            
            self.db.execute(sql, row1)
            
            for row in reader:
                self.db.execute(sql, row)

            self.db.commit()
