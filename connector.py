
import mysql.connector
from mysql.connector.errors import Error

def clrscr():
    from os import system
    system('clear')

class Connector:
    db_config = dict(
        user = 'exclusive',
        password = 'exclusive123',
        host = '10.32.1.21',
        port = 3307,
        database = 'exclusive'
    )

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)

        except mysql.connector.Error as err:
            print(err)

        else:
            if self.connection.is_connected():
                print('\n', 'Connected to MySQL database', '\n')
                self.connection.autocommit = True
  
    # example:: db.insert_data('test_table',['my_string_field'],['yeah4567'])

    def insert(self, table_name, column_names, values_to_insert):
        columns_string = ','.join(column_names)
        columns_format = ','.join(['%s' for _ in column_names])
        query = f'INSERT INTO {table_name} ({columns_string}) VALUES ({columns_format});'
        self.execute_query([query, values_to_insert])

    def select(self, table_name, column_names):
        columns_string = ','.join(column_names)
        query = f'SELECT {columns_string} FROM {table_name};'
        data = self.execute_query([query])
        return data

    # example:: db.update_data('test_table',['my_string_field'],['123456'],'id','10')

    def update(self, table_name, columns_to_update, values_to_update, condition_column, condition_value):
        set_string = self.create_update_string(columns_to_update, values_to_update)
        query = f'UPDATE {table_name} SET {set_string} WHERE {condition_column} = {condition_value};'
        self.execute_query([query])

    def delete(self, table_name, column, value):
        query = f'DELETE FROM {table_name} WHERE {column} = {value};'
        self.execute_query([query])

    def execute_query(self, args):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(*args)
            except Error as e:
                print(e)
            else:
                data = cursor.fetchall()
            finally:
                cursor.close()
        return data

    def create_update_string(self, columns_to_update, values_to_update):
        if len(columns_to_update) != len(values_to_update):
            raise ValueError('columns\' and values\' array lengths isn\'t equal')
        set_list = []
        for i in range(len(columns_to_update)):
            set_list.append(f'{columns_to_update[i]}=\' {values_to_update[i]}\'')
        set_string = ','.join(set_list)
        return set_string

class Query:
    get_authors = '''
        SELECT
            author_id,
            first_name,
            last_name,
            indexed_name,
            country,
            scopus_affiliation.url AS url
        FROM scopus_author_affiliation_history
        INNER JOIN scopus_author ON author_id = scopus_author.id
        INNER JOIN scopus_affiliation ON affiliation_id = scopus_affiliation.id
        WHERE author_id IN 
        (
            SELECT DISTINCT author_id FROM scopus_paper_query
            INNER JOIN scopus_paper_author ON scopus_paper_id = paper_id
            WHERE query_id={}
        )
        GROUP BY url, author_id, country
        HAVING url IS NOT NULL
        ORDER BY author_id

    '''

    get_found_authors = '''
        SELECT DISTINCT scopus_author_id FROM scopus_author_info_raw
        UNION
        SELECT DISTINCT scopus_author_id FROM scopus_author_photo
    '''

    get_last_info_id = '''
        SELECT author_info_raw_id
        FROM scopus_author_info_raw
        ORDER BY author_info_raw_id DESC
        LIMIT 1
    '''

class ScopusAuthor:
    def __init__(self, db_object: tuple):
        self.author_id = db_object[0]
        self.first_name = db_object[1]
        self.last_name = db_object[2]
        self.indexed_name = db_object[3]
        self.country = db_object[4]
        self.url = db_object[5]

class Database:

    db = Connector()

    @classmethod
    def get_authors(cls, query_id):
        data = cls.db.execute_query([Query.get_authors.format(query_id)])
        authors = [ ScopusAuthor(db_object) for db_object in data ]
        return authors

    @classmethod
    def write_raw_info(cls, author_id, link, info):
        cls.db.insert('scopus_author_info_raw',
            ['scopus_author_id', 'link', 'info'],
            [author_id, link, info]
        )

    @classmethod
    def write_img_info(cls, author_id, path):
        cls.db.insert('scopus_author_photo',
            ['scopus_author_id', 'path'],
            [author_id, path]
        )

    @classmethod
    def get_found_author(cls):
        data = cls.db.execute_query([Query.get_found_authors])
        if data:
            found_authors_id = [row_data[0] for row_data in data]
            return found_authors_id

    @classmethod
    def get_last_info_id(cls):
        data = cls.db.execute_query([Query.get_last_info_id])
        if data:
            return data[0][0]


if __name__ == '__main__':
    clrscr()
    db = Connector()
    # authors = Database.get_authors()
    
