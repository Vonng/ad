
-- 国家统计局统计用行政区划代码
DROP TABLE IF EXISTS ad.nbs cascade;
CREATE TABLE ad.nbs
(
    code     BIGINT      NOT NULL, -- 12位行政区划代码
    parent   BIGINT      NOT NULL, -- 父级行政区划代码
    urcode   SMALLINT,             -- 城乡性质代码
    rank     SMALLINT    NOT NULL, -- 行政区划等级：0-5 (国省市县乡村)
    name     VARCHAR(64) NOT NULL, -- 行政区划名称
    province VARCHAR(64),          -- 区划所属省份
    city     VARCHAR(64),          -- 区划所属城市
    county   VARCHAR(64),          -- 区划所属区县
    town     VARCHAR(64),          -- 区划所属乡镇街道
    village  VARCHAR(64),          -- 区划所属村/居委会
    PRIMARY KEY (code),            -- 行政区划代码为唯一主键
    CHECK ( rank >= 0 AND rank <= 5 ),
    CHECK ( code >= 100000000000 AND code <= 999999999999 )
);

COMMENT ON TABLE ad.nbs IS '国家统计局统计用行政区划代码';
COMMENT ON COLUMN ad.nbs.code IS '12位行政区划代码';
COMMENT ON COLUMN ad.nbs.parent IS '父级行政区划代码';
COMMENT ON COLUMN ad.nbs.urcode IS '城乡性质代码';
COMMENT ON COLUMN ad.nbs.rank IS '行政区划等级：0-5 (国省市县乡村)';
COMMENT ON COLUMN ad.nbs.name IS '行政区划名称';
COMMENT ON COLUMN ad.nbs.province IS '区划所属省份';
COMMENT ON COLUMN ad.nbs.city IS '区划所属城市';
COMMENT ON COLUMN ad.nbs.county IS '区划所属区县';
COMMENT ON COLUMN ad.nbs.town IS '区划所属乡镇街道';
COMMENT ON COLUMN ad.nbs.village IS '区划所属村/居委会';

CREATE TABLE ad.nbs_2009 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2010 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2011 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2012 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2013 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2014 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2015 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2016 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2017 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2018 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2019 (PRIMARY KEY (code)) INHERITS (ad.nbs);
CREATE TABLE ad.nbs_2020 (PRIMARY KEY (code)) INHERITS (ad.nbs);
