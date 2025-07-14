REQUIRED_HYPO_COLUMNS_NAME = [
    'source_id', 'source_lat', 'source_lon', 'source_depth_m',
    'source_origin_dt', 'source_err_rms_s', 'n_phases', 'source_gap_degree',
    'x_horizontal_err_m', 'y_horizontal_err_m', 'z_depth_err_m', 'magnitude',
    'remarks'
]

REQUIRED_PICKING_COLUMNS_NAME = [
    'source_id', 'station_code', 'p_arrival_dt', 'p_polarity', 'p_onset',
    's_arrival_dt', 'coda_dt'
]

REQUIRED_STATION_COLUMNS_NAME = [
    'station_code', 'network_code', 'station_lat', 'station_lon', 'station_elev_m'
]

REQUIRED_COLUMNS_NAME = [
    "id", "source_id", "source_lat_init", "source_lon_init", "location_init",
    "source_depth_m_init", "source_origin_dt_init", "source_err_rms_s_init", "gap_init",
    "remarks_init", "source_lat_reloc", "source_lon_reloc", "location_reloc",
    "source_depth_m_reloc", "source_origin_dt_reloc", "source_err_rms_s_reloc",
    "remarks_reloc", "network_code", "station_code", "station_lat",
    "station_lon", "station_elev_m", "p_arrival_dt", "s_arrival_dt",
    "coda_dt", "magnitude"
]

# combine all requirements in one object
DATA_STRUCTURES = {
    'hypo': {
        'header': REQUIRED_HYPO_COLUMNS_NAME,
        'type': ['Integer (PK)', 'Float', 'Float', 'Float',
                 'DateTime', 'Float', 'Integer', 'Float',
                 'Float', 'Float', 'Float', 'Float', 'String'],
        'sample': [2741, -1.6425079, 101.1422201, 1430.98,
                     '2023-01-20 19:11:19.260000', 0.0131338, 10, 292.576,
                     849.696, 474.627, 569.438, 0.286, 'specimen']
    },

    'picking': {
        'header': REQUIRED_PICKING_COLUMNS_NAME,
        'type': [ 'Integer (FK)', 'String', 'DateTime', 'String',
                 'String', 'DateTime', 'DateTime'],
        'sample': [ 3770, 'ML11', '2023-01-03 03:52:35.569630',
                   '+', 'I', '2023-01-03 03:52:36.200560',
                   '2023-01-03 03:52:44.200560']
    },
    
    'station': {
        'header': REQUIRED_STATION_COLUMNS_NAME,
        'type': ['String (FK)', 'String', 'Float', 'Float', 'Float'],
        'sample': ['ML09', 'ML', -1.618465946, 101.138134, 1270]
    }
}


REQUIREMENTS = {
    'hypo': REQUIRED_HYPO_COLUMNS_NAME,
    'picking': REQUIRED_PICKING_COLUMNS_NAME,
    'station': REQUIRED_STATION_COLUMNS_NAME,
    'merge': REQUIRED_COLUMNS_NAME
}