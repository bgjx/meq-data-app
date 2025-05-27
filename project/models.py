from django.contrib.gis.db import models

# SEML catalog models
class SemlInitialCatalog(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_lat = models.FloatField(blank=True, null=True)
    source_lon = models.FloatField(blank=True, null=True)
    source_depth_m = models.FloatField(blank=True, null=True)
    source_origin_dt = models.DateTimeField(blank=True, null=True)
    source_err_rms_s = models.FloatField(blank=True, null=True)
    n_phases = models.IntegerField(blank=True, null=True)
    source_gap_degree = models.FloatField(blank=True, null=True)
    x_horizontal_err_m = models.FloatField(blank=True, null=True)
    y_horizontal_err_m = models.FloatField(blank=True, null=True)
    z_depth_err_m = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_initial_catalog'


class SemlRelocatedCatalog(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_lat = models.FloatField(blank=True, null=True)
    source_lon = models.FloatField(blank=True, null=True)
    source_depth_m = models.FloatField(blank=True, null=True)
    source_origin_dt = models.DateTimeField(blank=True, null=True)
    source_err_rms_s = models.FloatField(blank=True, null=True)
    n_phases = models.IntegerField(blank=True, null=True)
    source_gap_degree = models.FloatField(blank=True, null=True)
    x_horizontal_err_m = models.FloatField(blank=True, null=True)
    y_horizontal_err_m = models.FloatField(blank=True, null=True)
    z_depth_err_m = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_relocated_catalog'


class SemlPickingCatalog(models.Model):
    source_id = models.IntegerField(blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    p_polarity = models.CharField(max_length=5, blank=True, null=True)
    p_onset = models.CharField(max_length=5, blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_picking_catalog'

# SERD catalog models
class SerdInitialCatalog(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_lat = models.FloatField(blank=True, null=True)
    source_lon = models.FloatField(blank=True, null=True)
    source_depth_m = models.FloatField(blank=True, null=True)
    source_origin_dt = models.DateTimeField(blank=True, null=True)
    source_err_rms_s = models.FloatField(blank=True, null=True)
    n_phases = models.IntegerField(blank=True, null=True)
    source_gap_degree = models.FloatField(blank=True, null=True)
    x_horizontal_err_m = models.FloatField(blank=True, null=True)
    y_horizontal_err_m = models.FloatField(blank=True, null=True)
    z_depth_err_m = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_initial_catalog'

class SerdRelocatedCatalog(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_lat = models.FloatField(blank=True, null=True)
    source_lon = models.FloatField(blank=True, null=True)
    source_depth_m = models.FloatField(blank=True, null=True)
    source_origin_dt = models.DateTimeField(blank=True, null=True)
    source_err_rms_s = models.FloatField(blank=True, null=True)
    n_phases = models.IntegerField(blank=True, null=True)
    source_gap_degree = models.FloatField(blank=True, null=True)
    x_horizontal_err_m = models.FloatField(blank=True, null=True)
    y_horizontal_err_m = models.FloatField(blank=True, null=True)
    z_depth_err_m = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_relocated_catalog'


class SerdPickingCatalog(models.Model):
    source_id = models.IntegerField(blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    p_polarity = models.CharField(max_length=5, blank=True, null=True)
    p_onset = models.CharField(max_length=5, blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_picking_catalog'


# station model
class SemlStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'

class SerdStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_station'