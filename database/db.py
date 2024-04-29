import mysql.connector
import mysql.connector.errors
import config


class ORM:
    def read_from_table(self, table: str, key: str = None, value=None, inner_joins: list[tuple[str, str]] = None):
        inner_join_sql = ""
        if inner_joins:
            inner_join_sql = " ".join([f"LEFT JOIN {table2} ON {table}.{key2} = {table2}.{key2}" for table2, key2 in inner_joins])

        where_clause = f"WHERE {key} = {value}" if key and value is not None else ""

        if isinstance(value, str):
            where_clause = f"WHERE {key} = '{value}'" if key and value is not None else ""

        sql = f"SELECT * FROM {table} {inner_join_sql} {where_clause};" if inner_join_sql or where_clause else f"SELECT * FROM {table};"
        ret = self.get_query(sql)

        if self.is_error(ret):
            return ret

        return ret

    def write_to_table(self, table: str, data: dict):
        keys = ", ".join(data.keys())
        values = ", ".join("null" if value is None else (str(value) if isinstance(value, int) else f"'{value}'") for value in data.values())

        query = f"INSERT INTO {table}({keys}) VALUES({values});"

        return self.post_query(query)

    def remove_from_table(self, table: str, key: str, value):
        if isinstance(value, int):
            sql = f"DELETE FROM {table} WHERE {key} = {value};"
        else:
            sql = f"DELETE FROM {table} WHERE {key} = '{value}';"

        return self.post_query(sql)

    def update_to_table(self, table: str, data: dict, key: str, value):

        values = []
        for k, v in data.items():
            if isinstance(v, int):
                values.append(f"{k} = {v}")
            else:
                if v is None:
                    values.append(f"{k} = null")
                else:
                    values.append(f"{k} = '{v}'")

        result = ", ".join(values)
        if isinstance(value, int):
            sql = f"UPDATE {table} SET {result} WHERE {key} = {value};"
        else:
            sql = f"UPDATE {table} SET {result} WHERE {key} = '{value}';"

        ret = self.post_query(sql)
        if ret:
            return True
        return False

    def exists_entry(self, table: str, key: str, value):
        if isinstance(value, int):
            sql = f"SELECT * FROM {table} WHERE {key} = {value};"
        else:
            sql = f"SELECT * FROM {table} WHERE {key} = '{value}';"

        ret = self.get_query(sql)
        if self.is_error(ret):
            return ret

        return len(ret) > 0

    def post_query(self, sql: str):
        try:
            conn, cursor = self.connect()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        except mysql.connector.errors.Error as e:
            return e

    def get_query(self, sql: str):
        try:
            conn, cursor = self.connect()
            cursor.execute(sql)
            ret = cursor.fetchall()
            conn.close()
            return ret
        except mysql.connector.errors.Error as e:
            return e

    def is_error(self, e):
        return isinstance(e, mysql.connector.errors.Error)

    def connect(self):
        conn = mysql.connector.connect(
            host=config.SQL_HOST,
            user=config.SQL_USER,
            password=config.SQL_PASSWORD,
            database=config.SQL_DATABASE
        )
        cursor = conn.cursor()
        return conn, cursor

