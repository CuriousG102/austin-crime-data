import csv

class Database:
    def __init__(self, dbFileLoc):
        self.col = 1
        self.identity = 0
        self.keys = {'id':0}
        self.table = []
        self.dbFileLoc = dbFileLoc

        if os.path.exists(dbFileLoc):
            with open(dbFileLoc, 'rb') as f:
                reader = csv.reader(f, dialect='excel')
                colRow = reader.next()
                for cell in colRow:
                    self.keys[cell] = col
                    self.col += 1
                self.table.append(colRow)
                for row in reader:
                    self.table.append(row)
                    self.identity += 1
        else:
            self.table.append([])
            

    def add(self, crime):
        rowToAdd = []
        keys = crime.keys()
        for key in keys:
            if key not in self.keys:
                self.keys[key] = self.col
                self.col += 1
        for i in range(0, len(self.keys)):
            rowToAdd.append('')
        crime['id'] = self.identity
        self.identity += 1
        for key in keys:
            rowToAdd[self.keys[key]] = crime[key]

        self.table.append(rowToAdd)

    def close(self):
        newColRow = []
        keys = self.keys.keys()
        
        for i in range(0, len(keys)):
            newColRow.append('')

        for key in keys:
            newColRow[self.keys[key]] = key
        
        self.table[0] = newColRow
        with open(self.dbFileLoc, 'wb') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(self.table)






