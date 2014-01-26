--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.4
-- Dumped by pg_dump version 9.2.0
-- Started on 2014-01-25 23:48:16 MST

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 186 (class 3079 OID 11995)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2390 (class 0 OID 0)
-- Dependencies: 186
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_with_oids = false;

--
-- TOC entry 169 (class 1259 OID 35559)
-- Name: acl; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE acl (
    id integer DEFAULT 0 NOT NULL,
    section_value character varying(230) DEFAULT 'system'::character varying NOT NULL,
    allow integer DEFAULT 0 NOT NULL,
    enabled integer DEFAULT 0 NOT NULL,
    return_value text,
    note text,
    updated_date integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 170 (class 1259 OID 35575)
-- Name: acl_sections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE acl_sections (
    id integer DEFAULT 0 NOT NULL,
    value character varying(230) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(230) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 171 (class 1259 OID 35585)
-- Name: aco; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aco (
    id integer DEFAULT 0 NOT NULL,
    section_value character varying(240) DEFAULT '0'::character varying NOT NULL,
    value character varying(240) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(255) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 172 (class 1259 OID 35599)
-- Name: aco_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aco_map (
    acl_id integer DEFAULT 0 NOT NULL,
    section_value character varying(230) DEFAULT '0'::character varying NOT NULL,
    value character varying(230) NOT NULL
);


--
-- TOC entry 173 (class 1259 OID 35606)
-- Name: aco_sections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aco_sections (
    id integer DEFAULT 0 NOT NULL,
    value character varying(230) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(230) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 174 (class 1259 OID 35616)
-- Name: aro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aro (
    id integer DEFAULT 0 NOT NULL,
    section_value character varying(240) DEFAULT '0'::character varying NOT NULL,
    value character varying(240) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(255) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 180 (class 1259 OID 35678)
-- Name: aro_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aro_groups (
    id integer DEFAULT 0 NOT NULL,
    parent_id integer DEFAULT 0 NOT NULL,
    lft integer DEFAULT 0 NOT NULL,
    rgt integer DEFAULT 0 NOT NULL,
    name character varying(255) NOT NULL,
    value character varying(255) NOT NULL
);


--
-- TOC entry 182 (class 1259 OID 35701)
-- Name: aro_groups_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aro_groups_map (
    acl_id integer DEFAULT 0 NOT NULL,
    group_id integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 175 (class 1259 OID 35630)
-- Name: aro_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aro_map (
    acl_id integer DEFAULT 0 NOT NULL,
    section_value character varying(230) DEFAULT '0'::character varying NOT NULL,
    value character varying(230) NOT NULL
);


--
-- TOC entry 176 (class 1259 OID 35637)
-- Name: aro_sections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE aro_sections (
    id integer DEFAULT 0 NOT NULL,
    value character varying(230) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(230) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 177 (class 1259 OID 35647)
-- Name: axo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE axo (
    id integer DEFAULT 0 NOT NULL,
    section_value character varying(240) DEFAULT '0'::character varying NOT NULL,
    value character varying(240) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(255) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 183 (class 1259 OID 35708)
-- Name: axo_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE axo_groups (
    id integer DEFAULT 0 NOT NULL,
    parent_id integer DEFAULT 0 NOT NULL,
    lft integer DEFAULT 0 NOT NULL,
    rgt integer DEFAULT 0 NOT NULL,
    name character varying(255) NOT NULL,
    value character varying(255) NOT NULL
);


--
-- TOC entry 185 (class 1259 OID 35731)
-- Name: axo_groups_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE axo_groups_map (
    acl_id integer DEFAULT 0 NOT NULL,
    group_id integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 178 (class 1259 OID 35661)
-- Name: axo_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE axo_map (
    acl_id integer DEFAULT 0 NOT NULL,
    section_value character varying(230) DEFAULT '0'::character varying NOT NULL,
    value character varying(230) NOT NULL
);


--
-- TOC entry 179 (class 1259 OID 35668)
-- Name: axo_sections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE axo_sections (
    id integer DEFAULT 0 NOT NULL,
    value character varying(230) NOT NULL,
    order_value integer DEFAULT 0 NOT NULL,
    name character varying(230) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 181 (class 1259 OID 35693)
-- Name: groups_aro_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE groups_aro_map (
    group_id integer DEFAULT 0 NOT NULL,
    aro_id integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 184 (class 1259 OID 35723)
-- Name: groups_axo_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE groups_axo_map (
    group_id integer DEFAULT 0 NOT NULL,
    axo_id integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 168 (class 1259 OID 35554)
-- Name: phpgacl; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE phpgacl (
    name character varying(230) NOT NULL,
    value character varying(230) NOT NULL
);


--
-- TOC entry 2367 (class 0 OID 35559)
-- Dependencies: 169
-- Data for Name: acl; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2368 (class 0 OID 35575)
-- Dependencies: 170
-- Data for Name: acl_sections; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO acl_sections VALUES (1, 'system', 1, 'System', 0);
INSERT INTO acl_sections VALUES (2, 'user', 2, 'User', 0);


--
-- TOC entry 2369 (class 0 OID 35585)
-- Dependencies: 171
-- Data for Name: aco; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2370 (class 0 OID 35599)
-- Dependencies: 172
-- Data for Name: aco_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2371 (class 0 OID 35606)
-- Dependencies: 173
-- Data for Name: aco_sections; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2372 (class 0 OID 35616)
-- Dependencies: 174
-- Data for Name: aro; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2378 (class 0 OID 35678)
-- Dependencies: 180
-- Data for Name: aro_groups; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2380 (class 0 OID 35701)
-- Dependencies: 182
-- Data for Name: aro_groups_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2373 (class 0 OID 35630)
-- Dependencies: 175
-- Data for Name: aro_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2374 (class 0 OID 35637)
-- Dependencies: 176
-- Data for Name: aro_sections; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2375 (class 0 OID 35647)
-- Dependencies: 177
-- Data for Name: axo; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2381 (class 0 OID 35708)
-- Dependencies: 183
-- Data for Name: axo_groups; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2383 (class 0 OID 35731)
-- Dependencies: 185
-- Data for Name: axo_groups_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2376 (class 0 OID 35661)
-- Dependencies: 178
-- Data for Name: axo_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2377 (class 0 OID 35668)
-- Dependencies: 179
-- Data for Name: axo_sections; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2379 (class 0 OID 35693)
-- Dependencies: 181
-- Data for Name: groups_aro_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2382 (class 0 OID 35723)
-- Dependencies: 184
-- Data for Name: groups_axo_map; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 2366 (class 0 OID 35554)
-- Dependencies: 168
-- Data for Name: phpgacl; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO phpgacl VALUES ('version', '3.3.7');
INSERT INTO phpgacl VALUES ('schema_version', '2.1');


--
-- TOC entry 2308 (class 2606 OID 35571)
-- Name: acl_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY acl
    ADD CONSTRAINT acl_pkey PRIMARY KEY (id);


--
-- TOC entry 2313 (class 2606 OID 35582)
-- Name: acl_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY acl_sections
    ADD CONSTRAINT acl_sections_pkey PRIMARY KEY (id);


--
-- TOC entry 2321 (class 2606 OID 35605)
-- Name: aco_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aco_map
    ADD CONSTRAINT aco_map_pkey PRIMARY KEY (acl_id, section_value, value);


--
-- TOC entry 2317 (class 2606 OID 35596)
-- Name: aco_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aco
    ADD CONSTRAINT aco_pkey PRIMARY KEY (id);


--
-- TOC entry 2323 (class 2606 OID 35613)
-- Name: aco_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aco_sections
    ADD CONSTRAINT aco_sections_pkey PRIMARY KEY (id);


--
-- TOC entry 2355 (class 2606 OID 35707)
-- Name: aro_groups_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aro_groups_map
    ADD CONSTRAINT aro_groups_map_pkey PRIMARY KEY (acl_id, group_id);


--
-- TOC entry 2347 (class 2606 OID 35689)
-- Name: aro_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aro_groups
    ADD CONSTRAINT aro_groups_pkey PRIMARY KEY (id, value);


--
-- TOC entry 2331 (class 2606 OID 35636)
-- Name: aro_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aro_map
    ADD CONSTRAINT aro_map_pkey PRIMARY KEY (acl_id, section_value, value);


--
-- TOC entry 2327 (class 2606 OID 35627)
-- Name: aro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aro
    ADD CONSTRAINT aro_pkey PRIMARY KEY (id);


--
-- TOC entry 2333 (class 2606 OID 35644)
-- Name: aro_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY aro_sections
    ADD CONSTRAINT aro_sections_pkey PRIMARY KEY (id);


--
-- TOC entry 2365 (class 2606 OID 35737)
-- Name: axo_groups_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY axo_groups_map
    ADD CONSTRAINT axo_groups_map_pkey PRIMARY KEY (acl_id, group_id);


--
-- TOC entry 2357 (class 2606 OID 35719)
-- Name: axo_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY axo_groups
    ADD CONSTRAINT axo_groups_pkey PRIMARY KEY (id, value);


--
-- TOC entry 2341 (class 2606 OID 35667)
-- Name: axo_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY axo_map
    ADD CONSTRAINT axo_map_pkey PRIMARY KEY (acl_id, section_value, value);


--
-- TOC entry 2337 (class 2606 OID 35658)
-- Name: axo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY axo
    ADD CONSTRAINT axo_pkey PRIMARY KEY (id);


--
-- TOC entry 2343 (class 2606 OID 35675)
-- Name: axo_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY axo_sections
    ADD CONSTRAINT axo_sections_pkey PRIMARY KEY (id);


--
-- TOC entry 2353 (class 2606 OID 35699)
-- Name: groups_aro_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY groups_aro_map
    ADD CONSTRAINT groups_aro_map_pkey PRIMARY KEY (group_id, aro_id);


--
-- TOC entry 2363 (class 2606 OID 35729)
-- Name: groups_axo_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY groups_axo_map
    ADD CONSTRAINT groups_axo_map_pkey PRIMARY KEY (group_id, axo_id);


--
-- TOC entry 2306 (class 2606 OID 35558)
-- Name: phpgacl_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY phpgacl
    ADD CONSTRAINT phpgacl_pkey PRIMARY KEY (name);


--
-- TOC entry 2351 (class 1259 OID 35700)
-- Name: aro_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX aro_id ON groups_aro_map USING btree (aro_id);


--
-- TOC entry 2361 (class 1259 OID 35730)
-- Name: axo_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axo_id ON groups_axo_map USING btree (axo_id);


--
-- TOC entry 2309 (class 1259 OID 35572)
-- Name: enabled_acl; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enabled_acl ON acl USING btree (enabled);


--
-- TOC entry 2314 (class 1259 OID 35584)
-- Name: hidden_acl_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_acl_sections ON acl_sections USING btree (hidden);


--
-- TOC entry 2318 (class 1259 OID 35598)
-- Name: hidden_aco; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_aco ON aco USING btree (hidden);


--
-- TOC entry 2324 (class 1259 OID 35615)
-- Name: hidden_aco_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_aco_sections ON aco_sections USING btree (hidden);


--
-- TOC entry 2328 (class 1259 OID 35629)
-- Name: hidden_aro; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_aro ON aro USING btree (hidden);


--
-- TOC entry 2334 (class 1259 OID 35646)
-- Name: hidden_aro_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_aro_sections ON aro_sections USING btree (hidden);


--
-- TOC entry 2338 (class 1259 OID 35660)
-- Name: hidden_axo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_axo ON axo USING btree (hidden);


--
-- TOC entry 2344 (class 1259 OID 35677)
-- Name: hidden_axo_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hidden_axo_sections ON axo_sections USING btree (hidden);


--
-- TOC entry 2348 (class 1259 OID 35692)
-- Name: lft_rgt_aro_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lft_rgt_aro_groups ON aro_groups USING btree (lft, rgt);


--
-- TOC entry 2358 (class 1259 OID 35722)
-- Name: lft_rgt_axo_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lft_rgt_axo_groups ON axo_groups USING btree (lft, rgt);


--
-- TOC entry 2349 (class 1259 OID 35690)
-- Name: parent_id_aro_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parent_id_aro_groups ON aro_groups USING btree (parent_id);


--
-- TOC entry 2359 (class 1259 OID 35720)
-- Name: parent_id_axo_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX parent_id_axo_groups ON axo_groups USING btree (parent_id);


--
-- TOC entry 2310 (class 1259 OID 35573)
-- Name: section_value_acl; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX section_value_acl ON acl USING btree (section_value);


--
-- TOC entry 2319 (class 1259 OID 35597)
-- Name: section_value_value_aco; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX section_value_value_aco ON aco USING btree (section_value, value);


--
-- TOC entry 2329 (class 1259 OID 35628)
-- Name: section_value_value_aro; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX section_value_value_aro ON aro USING btree (section_value, value);


--
-- TOC entry 2339 (class 1259 OID 35659)
-- Name: section_value_value_axo; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX section_value_value_axo ON axo USING btree (section_value, value);


--
-- TOC entry 2311 (class 1259 OID 35574)
-- Name: updated_date_acl; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX updated_date_acl ON acl USING btree (updated_date);


--
-- TOC entry 2315 (class 1259 OID 35583)
-- Name: value_acl_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_acl_sections ON acl_sections USING btree (value);


--
-- TOC entry 2325 (class 1259 OID 35614)
-- Name: value_aco_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_aco_sections ON aco_sections USING btree (value);


--
-- TOC entry 2350 (class 1259 OID 35691)
-- Name: value_aro_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_aro_groups ON aro_groups USING btree (value);


--
-- TOC entry 2335 (class 1259 OID 35645)
-- Name: value_aro_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_aro_sections ON aro_sections USING btree (value);


--
-- TOC entry 2360 (class 1259 OID 35721)
-- Name: value_axo_groups; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_axo_groups ON axo_groups USING btree (value);


--
-- TOC entry 2345 (class 1259 OID 35676)
-- Name: value_axo_sections; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX value_axo_sections ON axo_sections USING btree (value);


-- Completed on 2014-01-25 23:48:16 MST

--
-- PostgreSQL database dump complete
--

