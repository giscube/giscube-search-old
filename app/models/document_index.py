import os
import re

import sqlalchemy
from sqlalchemy.dialects.postgresql import JSON
from geoalchemy2 import Geometry

from app.models.utils.tsvector import TsVector
from app.utils.words import remove_accents

metadata = sqlalchemy.MetaData()


def clean_table_name(s):
    s = remove_accents(s)
    s = s.lower().replace('-', '_').replace(' ', '_')
    s = [re.sub(r"[^a-zA-Z0-9_]+", '', k) for k in s]
    return ''.join(s)


def get_table(name):
    name = clean_table_name(name)
    table = metadata.tables.get(name, None)
    if table is None:
        table = sqlalchemy.Table(
            name,
            metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('content_type', sqlalchemy.String(length=255)),
            sqlalchemy.Column('object_id', sqlalchemy.Text()),
            sqlalchemy.Column('title', sqlalchemy.String(length=255)),
            sqlalchemy.Column('body', TsVector()),
            sqlalchemy.Column('data', JSON(), nullable=False),
            sqlalchemy.Column('geom_point', Geometry(geometry_type='MULTIPOINT', srid=4326)),
            sqlalchemy.Column('geom_linestring', Geometry(geometry_type='MULTIPOINT', srid=4326)),
            sqlalchemy.Column('geom_polygon', Geometry(geometry_type='MULTIPOINT', srid=4326)),
            sqlalchemy.Index('%s_body_idx' % name, 'body', postgresql_using='gin'),
            sqlalchemy.Index('%s_geom_point_idx' % name, 'geom_point', postgresql_using='gist'),
            sqlalchemy.Index('%s_geom_linestring_idx' % name, 'geom_linestring', postgresql_using='gist'),
            sqlalchemy.Index('%s_geom_polygon_idx' % name, 'geom_polygon', postgresql_using='gist'),
        )
    return table


def create_table(name):
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    name = clean_table_name(name)
    schema = get_table(name)
    schema.create(engine)
    return schema


def drop_table(name):
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    name = clean_table_name(name)
    schema = get_table(name)
    schema.drop(engine)
    return schema
