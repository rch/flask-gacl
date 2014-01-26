from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence

metadata = MetaData()

"""
    CREATE TABLE acl_sections
    (
      id integer NOT NULL DEFAULT 0,
      value character varying(230) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(230) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT acl_sections_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE acl_sections_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
acl_sections = Table('acl_sections', metadata,
    Column('id', Integer, Sequence('acl_sections_seq'), primary_key=True),
    Column('value', String),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE aro_sections
    (
      id integer NOT NULL DEFAULT 0,
      value character varying(230) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(230) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT aro_sections_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE aro_sections_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
aro_sections = Table('aro_sections', metadata,
    Column('id', Integer, Sequence('aro_sections_seq'), primary_key=True),
    Column('value', String),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE aco_sections
    (
      id integer NOT NULL DEFAULT 0,
      value character varying(230) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(230) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT aco_sections_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE aco_sections_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
aco_sections = Table('aco_sections', metadata,
    Column('id', Integer, Sequence('aco_sections_seq'), primary_key=True),
    Column('value', String),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE axo_sections
    (
      id integer NOT NULL DEFAULT 0,
      value character varying(230) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(230) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT axo_sections_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE axo_sections_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
axo_sections = Table('axo_sections', metadata,
    Column('id', Integer, Sequence('axo_sections_seq'), primary_key=True),
    Column('value', String),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)
