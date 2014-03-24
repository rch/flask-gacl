
from common import metadata

"""
    CREATE TABLE aro_groups
    (
      id integer NOT NULL DEFAULT 0,
      parent_id integer NOT NULL DEFAULT 0,
      lft integer NOT NULL DEFAULT 0,
      rgt integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      value character varying(255) NOT NULL,
      CONSTRAINT aro_groups_pkey PRIMARY KEY (id, value)
    )
    CREATE SEQUENCE aro_groups_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
aro_groups = Table('aro_groups', metadata,
    Column('id', Integer, Sequence('acl_groups_seq'), primary_key=True),
    Column('parent_id', Integer, nullable=False, default=0),
    Column('lft', Integer, nullable=False, default=0),
    Column('rgt', Integer, nullable=False, default=0),
    Column('name', String),
    Column('value', String, unique=True),
    Column('hidden', Integer),
)

"""
    CREATE TABLE axo_groups
    (
      id integer NOT NULL DEFAULT 0,
      parent_id integer NOT NULL DEFAULT 0,
      lft integer NOT NULL DEFAULT 0,
      rgt integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      value character varying(255) NOT NULL,
      CONSTRAINT axo_groups_pkey PRIMARY KEY (id, value)
    )
    CREATE SEQUENCE axo_groups_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
axo_groups = Table('axo_groups', metadata,
    Column('id', Integer, Sequence('acl_groups_seq'), primary_key=True),
    Column('parent_id', Integer, nullable=False, default=0),
    Column('lft', Integer, nullable=False, default=0),
    Column('rgt', Integer, nullable=False, default=0),
    Column('name', String),
    Column('value', String, unique=True),
    Column('hidden', Integer),
)
