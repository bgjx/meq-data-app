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