from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# SEML catalog models
class SemlInitialCatalog(models.Model):
    source_id = models.AutoField(primary_key=True)
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

    # special spatial field
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        db_table = 'seml_initial_catalog'
    
    # def save(self, *args, **kwargs):
    #     if self.source_lat is not None and self.source_lon is not None:
    #         self.location_init = Point(self.source_lon, self.source_lat)
    #     super().save(*args, **kwargs)


class SemlRelocatedCatalog(models.Model):
    source_id = models.AutoField(primary_key=True)
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

    # special spatial field
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        db_table = 'seml_relocated_catalog'
    
    # def save(self, *args, **kwargs):
    #     if self.source_lat is not None and self.source_lon is not None:
    #         self.location_reloc = Point(self.source_lon, self.source_lat)
    #     super().save(*args, **kwargs)


class SemlPickingCatalog(models.Model):
    id = models.AutoField(primary_key=True)
    source_id = models.IntegerField(blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    p_polarity = models.CharField(max_length=5, blank=True, null=True)
    p_onset = models.CharField(max_length=5, blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'seml_picking_catalog'

# SERD catalog models
class SerdInitialCatalog(models.Model):
    source_id = models.AutoField(primary_key=True)
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
        db_table = 'serd_initial_catalog'

class SerdRelocatedCatalog(models.Model):
    source_id = models.AutoField(primary_key=True)
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
        db_table = 'serd_relocated_catalog'


class SerdPickingCatalog(models.Model):
    id = models.AutoField(primary_key=True)
    source_id = models.IntegerField(blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    p_polarity = models.CharField(max_length=5, blank=True, null=True)
    p_onset = models.CharField(max_length=5, blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'serd_picking_catalog'


# station model
class SemlStation(models.Model):
    id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'seml_station'

class SerdStation(models.Model):
    id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'serd_station'


# Merged view model
class SemlCatalogMergedView(models.Model):
    id = models.BigIntegerField(primary_key=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_lat_init = models.FloatField(blank=True, null=True)
    source_lon_init = models.FloatField(blank=True, null=True)
    location_init = models.PointField(blank=True, null=True)
    source_depth_m_init = models.FloatField(blank=True, null=True)
    source_origin_dt_init = models.DateTimeField(blank=True, null=True)
    source_err_rms_s_init = models.FloatField(blank=True, null=True)
    gap_init = models.FloatField(blank=True, null=True)
    remarks_init = models.CharField(max_length=10, blank=True, null=True)
    source_lat_reloc = models.FloatField(blank=True, null=True)
    source_lon_reloc = models.FloatField(blank=True, null=True)
    location_reloc = models.PointField(blank=True, null=True)
    source_depth_m_reloc = models.FloatField(blank=True, null=True)
    source_origin_dt_reloc = models.DateTimeField(blank=True, null=True)
    source_err_rms_s_reloc = models.FloatField(blank=True, null=True)
    remarks_reloc = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_catalog_merged_view'


class SerdCatalogMergedView(models.Model):
    id = models.BigIntegerField(primary_key=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_lat_init = models.FloatField(blank=True, null=True)
    source_lon_init = models.FloatField(blank=True, null=True)
    location_init = models.PointField(blank=True, null=True)
    source_depth_m_init = models.FloatField(blank=True, null=True)
    source_origin_dt_init = models.DateTimeField(blank=True, null=True)
    source_err_rms_s_init = models.FloatField(blank=True, null=True)
    gap_init = models.FloatField(blank=True, null=True)
    remarks_init = models.CharField(max_length=10, blank=True, null=True)
    source_lat_reloc = models.FloatField(blank=True, null=True)
    source_lon_reloc = models.FloatField(blank=True, null=True)
    location_reloc = models.PointField(blank=True, null=True)
    source_depth_m_reloc = models.FloatField(blank=True, null=True)
    source_origin_dt_reloc = models.DateTimeField(blank=True, null=True)
    source_err_rms_s_reloc = models.FloatField(blank=True, null=True)
    remarks_reloc = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)
    p_arrival_dt = models.DateTimeField(blank=True, null=True)
    s_arrival_dt = models.DateTimeField(blank=True, null=True)
    coda_dt = models.DateTimeField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_catalog_merged_view'

# File upload models
class Updates(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    description = models.CharField(max_length=225)
    file_name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title