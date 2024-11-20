CREATE TABLE seml_cat_wcc (
    id INT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    utm_x_m DOUBLE PRECISION,
    utm_y_m DOUBLE PRECISION,
    depth_m DOUBLE PRECISION,
    elev_m DOUBLE PRECISION,
    year INT,
    month INT,
    day INT,
    hour INT,
    minute INT,
    second DOUBLE PRECISION,
    dt_origin TIMESTAMP(6),
    rms_error DOUBLE PRECISION,
    ml_mag FLOAT,
    mw_mag FLOAT,
    remarks VARCHAR(10)
);

