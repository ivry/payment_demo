import psycopg2.extras
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor, execute_values
import logging
import json
import os
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

secrets_hash = {}

# runs on import
# required adapter between python and postgres UUID types
psycopg2.extras.register_uuid()


class _CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 != 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, (date, datetime, time, timedelta, UUID)):
            return o.__str__()
        return super(_CustomJsonEncoder, self).default(o)


def get_connection(
        db_host=None,
        db_name=None,
        db_user=None,
        db_password=None,
        db_port=None,
        db_schema=None
):
    conn_str = "host={0} dbname={1} user={2} password={3} port={4} options='-c search_path={5}'".format(
        db_host or os.environ.get('DB_HOST'),
        db_name or os.environ.get('DB_NAME'),
        db_user or os.environ.get('DB_USER'),
        db_password or (os.environ.get('DB_PASSWORD') if 'DB_PASSWORD' in os.environ else None),
        db_port or os.environ.get('DB_PORT'),
        db_schema or os.environ.get('DB_SCHEMA')
    )

    try:
        conn = connect(conn_str)
        conn.autocommit = True
        return conn
    except Exception as e:
        logging.error(e)


def insert(conn, table, data_dict):
    populated_keys = [k for k, v in data_dict.items() if v is not None]

    column_ids = [sql.Identifier(k) for k in populated_keys]
    col_str = sql.SQL(',').join(column_ids)

    value_placeholders = [sql.Placeholder(name=k) for k in populated_keys]
    value_placeholder_str = sql.SQL(',').join(value_placeholders)

    query = sql.SQL('INSERT INTO {tbl}({col_str}) values ({val_str}) RETURNING *').format(
        tbl=sql.Identifier(table),
        col_str=col_str,
        val_str=value_placeholder_str
    )

    logging.info(query.as_string(conn))
    logging.debug(f'INSERTING {json.dumps(data_dict, indent=4, cls=_CustomJsonEncoder)}')

    # execute query
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, data_dict)
        out = cur.fetchone()

    return out
