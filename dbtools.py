import inspect


def orm(cursor, dto_type):
    args = inspect.getfullargspec(dto_type.__init__).args

    args = args[1:]

    col_names = [column[0] for column in cursor.description]

    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        self._table_name = dto_type.__name__ + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = ins_dict.values()
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)
        self._conn.execute(stmt, list(params))

    def find_all(self,comd):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {} ORDER BY {} '.format(self._table_name, comd))
        return orm(c, self._dto_type)

    def findByProd(self, id):
        c = self._conn.cursor()
        c.execute('SELECT prod.quantity '
                  'FROM Products prod WHERE prod.id=(?)', [id])

        last_quantity= c.fetchone()
        return last_quantity

    def findPrice(self, id):
        c = self._conn.cursor()
        c.execute('SELECT prod.price '
                  'FROM Products prod WHERE prod.id=({})'.format(id))

        return c.fetchone()[0]

    def findLocation(self, id):
        c = self._conn.cursor()
        c.execute('SELECT Coffee_stands.location FROM Coffee_stands WHERE(Coffee_stands.id=(?))',[id])
        return c.fetchone()[0]

    def updrage_quan (self, new_quantity, id):
        c = self._conn.cursor()
        c.execute('UPDATE Products SET quantity=(?) WHERE Products.id=(?)', [new_quantity, id])
        return

    def findByActiv(self, activatorId):
        c = self._conn.cursor()
        c.execute('SELECT * FROM Activities activ WHERE activ.activator_id=(?)',[activatorId])
        return orm(c, self._dto_type)


