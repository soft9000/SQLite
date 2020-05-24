#!/usr/bin/env python3

from BasicFields import BasicFields
from collections import OrderedDict

import sqlite3

class BasicTable:
    """ 
    Class name implies that we are interested in a basic, "type 1," Table?
    Specifically:
        Classic 'ID' AUTO paradigm for the primary key is implied.
        No constraints outside of the primary key.
        No tech-mantained entity relationships. -We can manage those, ourselves?
    """

    def __init__(self, file_name="./default.sqlt3"):
        self.file = file_name
        self.conn = None
        self._curs = None
        self.bOpen = False
        self.fields = None
        self.table_name = None
        self.ex = None

    def do_exec(self, *values):
        ''' Exception management. Returns -1 on exception, else SQLite result. 
        Can also check if an exception has been error-cached, or None == ok.
        '''
        try:
            self.ex = None
            return self._curs.execute(*values)
        except Exception as ex:
            self.ex = ex
            return -1

    def delete_file(self):
        ''' Remove the database file form the file system. Data will be lost.
        Undo is not possible. T/F. 
        '''
        try:
            import os
            self.ex = None
            os.unlink(self.file)
            return True
        except Exception as ex:
            self.ex = ex
            return False

    def is_defined(self):
        ''' See if we can use the database, by checking if a table has been defined. 
        True if data table is defined and may be open()ed okay. False otherwise.
        '''
        if not self.fields:
            return False
        if not self.table_name:
            return False
        return True

    def define(self, sql_fields, table_name='MyTable'):
        ''' Associate the definition for a single database table. 
        True if data table is defined and may be open()ed okay. False otherwise.
        '''
        if not isinstance(sql_fields, BasicFields):
            return False
        if not BasicFields.IsGoodName(table_name):
            return False
        self.fields = sql_fields.get_od();
        self.table_name = table_name
        return True

    def undefine(self):
        ''' Invalidate a table definition, if any. None always returned. '''
        self.fields = self.table_name = None
        self.ex = None
        
    def open(self):
        ''' Connect to a database to access the table definition. 
        Returns False if no table definition, or upon exception / error.
        '''
        if not self.is_defined():
            self.ex = Exception("DAO: Undefined database table.")
            return False
        if self.bOpen is False:
            try:
                self.ex = None
                self.conn = sqlite3.connect(self.file)
                self.conn.row_factory = sqlite3.Row # WARNING: SQLite, Only!
                self._curs = self.conn.cursor()
                self.bOpen = True
            except Exception as ex:
                self.ex = ex
                return False
        return True
        
    def close(self):
        ''' Commit any changes, release database connection, and clear any 
        previous error. Database table definition remains ready for re-use.
        Returns False if the connection is not open, or upon error. Else True.
        '''
        if self.bOpen:
            self.conn.commit()
            self.bOpen = False
            self.ex = None
        return True
        
    def count(self):
        ''' Tally the numbers of rows in the database table. 
        Returns count, else -1 in error. 
        '''
        if self.bOpen:
            res = self.do_exec(f"SELECT count(*) FROM {self.table_name};")
            if not self.ex:
                return res.fetchone()[0]
        return -1
        
    def drop_table(self):
        ''' Delete all of the data in the table. All data will be lost. Undo is not possible. 
        Returns False if the connection is not open, or upon error. Else True.
        '''
        if self.bOpen:
            self.do_exec(f"DrOp TaBLe IF EXISTS {self.table_name};")
            if not self.ex:
                return True
        return False
        
    def create_table(self):
        ''' Create the associated database table, if is not already present. 
        Returns False if the connection is not open, or upon error. Else True.
        '''
        if self.bOpen:
            zStr = "ID INTEGER PRIMARY KEY AUTOINCREMENT"
            for field in self.fields:
                if field == 'ID':
                    continue
                zStr += ", "
                zStr += field + " " + self.fields[field]
            self.do_exec(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ({zStr});")
            if not self.ex:
                return True
        return False
        
    def insert(self, sql_fields):
        ''' Insert specified columns into a new database table row.
        Returns the database row-ID (>0) of the new row, upon success.
        Returns False if the connection is not open, or upon error. 
        '''
        if self.bOpen:
            if not isinstance(sql_fields, dict):
                return False
            for zKey in sql_fields:
                if zKey not in self.fields:
                    return False
            zKeys = tuple(sql_fields.keys())
            zValues = tuple(sql_fields.values())
            self.do_exec(
                f"INSERT INTO {self.table_name} {zKeys} VALUES {zValues};")
            if not self.ex:
                return self._curs.lastrowid
        return False
        
    def update(self, id_, sql_fields):
        ''' Update specified columns into database table row.
        Returns False if the connection is not open, or upon error. Else True.
        '''
        if self.bOpen:
            if not isinstance(sql_fields, dict):
                return False
            for zKey in sql_fields:
                if zKey not in self.fields:
                    return False
            zSet = "SET "; bFirst = True
            for key in sql_fields:
                if not bFirst:
                    zSet += ", "
                else:
                    bFirst = False
                zSet += f"{key} = ? "
            cmd = f"UPDATE {self.table_name} {zSet} WHERE ID = {id_};"
            self.do_exec(
                cmd,
                tuple(sql_fields.values())
                )
            if not self.ex:
                return True
        return False
        
    def delete(self, primary_key):
        ''' Remove specified ID data from database table. Undo is not possible.
        Returns False if the connection is not open, or upon error. Else True.
        '''
        if self.bOpen:
            self.do_exec(f"DELETE from {self.table_name} WHERE ID = ?;", [primary_key])
            if not self.ex:
                return True
        return False
        
    def select(self, sql_select):
        ''' Enumerate rows from database table matching SQL-Query.
        '''
        if self.bOpen:
            self.do_exec(sql_select)
            if not self.ex:
                zlist = self._curs.fetchall()
                for ref in zlist:
                    yield ref
        return None
        
    def select_dict(self, sql_select): # WARNING: Requires sqlite3.Row
        ''' Enumerate rows from database table matching SQL-Query.
        Returns row as an ORDERED dictionary.
        '''
        if self.bOpen:
            self.do_exec(sql_select)
            zlist = self._curs.fetchall()
            if not self.ex:
                for ref in zlist:
                    result = OrderedDict()
                    for ss, key in enumerate(ref.keys()):
                        result[key] = ref[ss]
                    yield result
        return None
