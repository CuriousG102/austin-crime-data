import csv
import os

class Database:
    def __init__(self, dbFileLoc):
        self.identity = 0
        self.keys = {'id':0}
        self.reverseDict{0:'id'}
        self.table = []
        self.dbFileLoc = dbFileLoc

        if os.path.exists(dbFileLoc):
            with open(dbFileLoc, 'r') as f:
                self.col = 0
                reader = csv.reader(f, dialect='excel')
                colRow = next(reader)
                for cell in colRow:
                    self.keys[cell] = self.col
                    self.reverseDict[self.col] = key
                    self.col += 1
                self.table.append(colRow)
                for row in reader:
                    self.table.append(row)
                    self.identity += 1
        else:
            self.col = 1
            self.table.append([])
        
    def add(self, crime):
        rowToAdd = []
        keys = crime.keys()
        for key in keys:
            if key not in self.keys:
                self.keys[key] = self.col
                self.reverseDict[self.col] = key
                self.col += 1
        for i in range(0, len(self.keys)):
            rowToAdd.append('')
        crime['id'] = self.identity
        self.identity += 1
        for key in keys:
            rowToAdd[self.keys[key]] = crime[key]

        self.table.append(rowToAdd)

    def __len__(self):
        """
        Returns the number of entries we have
        """
        return self.identity + 1

    def getID(self, id):
        row = self.table[id + 1]
        dictToReturn = {}
        for colNum in range(len(row)):
            dictToReturn[self.reverseDict[colNum]] = row[colNum]
        return dictToReturn
            

    def close(self):
        newColRow = []
        keys = list(self.keys.keys())
        
        for i in range(0, len(keys)):
            newColRow.append('')

        for key in keys:
            newColRow[self.keys[key]] = key
        
        self.table[0] = newColRow
        if not os.path.exists(os.path.dirname(self.dbFileLoc)):
            os.makedirs(os.path.dirname(self.dbFileLoc))

        with open(self.dbFileLoc, 'w') as f:
                writer = csv.writer(f, dialect='excel')
                writer.writerows(self.table)



