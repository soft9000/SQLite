from BasicFields import BasicFields
from BasicTable import BasicTable

if __name__ == '__main__':
    fields = BasicFields()
    assert(fields.add("Name", "Text"))
    assert(fields.add("String", "Text"))
    assert(fields.add("Age", "Integer"))
    dao = BasicTable()
    dao.delete_file()
    assert(dao.define(fields))
    assert(dao.open())
    assert(dao.create_table())
    assert(dao.insert({"Name":'"John1"', "String":'123, "45"', "Age":21}))
    assert(dao.insert({"Name":"John2's", "String":"123, '45'", "Age":21}))
    assert(dao.insert({"Name":'''John3''', "Age":21}))
    assert(dao.update(1, {"Age":22}))
    assert(dao.update(1, {"Name":"Jasper"}))
    assert(dao.insert({"Name":"Nagy", "Age":432}))
    assert(dao.count() == 4)
    for row in dao.select(f"select * from {dao.table_name};"):
        print(*row)
    dao.close()

