from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence
from common import metadata
from gacl_sections import *

"""
    CREATE TABLE acl
    (
      id integer NOT NULL DEFAULT 0,
      section_value character varying(240) NOT NULL DEFAULT '0'::character varying,
      value character varying(240) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT acl_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE acl_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
acl = Table('acl', metadata,
    Column('id', Integer, Sequence('acl_seq'), primary_key=True),
    Column('section_value', String, ForeignKey('acl_sections.value')),
    Column('value', String, unique=True),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE aco
    (
      id integer NOT NULL DEFAULT 0,
      section_value character varying(240) NOT NULL DEFAULT '0'::character varying,
      value character varying(240) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT aco_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE aco_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
aco = Table('aco', metadata,
    Column('id', Integer, Sequence('aco_seq'), primary_key=True),
    Column('section_value', String, ForeignKey('aco_sections.value')),
    Column('value', String, unique=True),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE aro
    (
      id integer NOT NULL DEFAULT 0,
      section_value character varying(240) NOT NULL DEFAULT '0'::character varying,
      value character varying(240) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT aro_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE aro_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
aro = Table('aro', metadata,
    Column('id', Integer, Sequence('aro_seq'), primary_key=True),
    Column('section_value', String, ForeignKey('aro_sections.value')),
    Column('value', String, unique=True),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)

"""
    CREATE TABLE axo
    (
      id integer NOT NULL DEFAULT 0,
      section_value character varying(240) NOT NULL DEFAULT '0'::character varying,
      value character varying(240) NOT NULL,
      order_value integer NOT NULL DEFAULT 0,
      name character varying(255) NOT NULL,
      hidden integer NOT NULL DEFAULT 0,
      CONSTRAINT axo_pkey PRIMARY KEY (id)
    )
    
    CREATE SEQUENCE axo_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 10
      CACHE 1;
"""
axo = Table('axo', metadata,
    Column('id', Integer, Sequence('axo_seq'), primary_key=True),
    Column('section_value', String, ForeignKey('axo_sections.value')),
    Column('value', String, unique=True),
    Column('order_value', Integer),
    Column('name', String),
    Column('hidden', Integer),
)
