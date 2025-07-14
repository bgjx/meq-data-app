from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
# from django.utils.timezone import make_aware
# from zoneinfo import ZoneInfo

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
        managed = False
        db_table = 'seml_initial_catalog'
    
    # override method for location point and timezone aware
    def save(self, *args, **kwargs):
        if self.source_lat is not None and self.source_lon is not None:
            self.location_init = Point(self.source_lon, self.source_lat)

        # timezone_jkt = ZoneInfo("Asia/Jakarta")
        # for field in self._meta.fields:
        #     if isinstance(field, models.DateTimeField):
        #         value = getattr(self, field.name)
        #         if value and value.tzinfo is None:
        #             setattr(self, field.name, make_aware(value, timezone=timezone_jkt))

        super().save(*args, **kwargs)
    

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
        managed = False
        db_table = 'seml_relocated_catalog'
    
    # override method for location point and timezone aware
    def save(self, *args, **kwargs):
        
        if self.source_lat is not None and self.source_lon is not None:
            self.location_reloc = Point(self.source_lon, self.source_lat)

        # timezone_jkt = ZoneInfo("Asia/Jakarta")
        # for field in self._meta.fields:
        #     if isinstance(field, models.DateTimeField):
        #         value = getattr(self, field.name)
        #         if value and value.tzinfo is None:
        #             setattr(self, field.name, make_aware(value, timezone=timezone_jkt))

        super().save(*args, **kwargs)


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
        managed = False
        db_table = 'seml_picking_catalog'
    
    # # override method for timezone aware
    # def save(self, *args, **kwargs):
    #     timezone_jkt = ZoneInfo("Asia/Jakarta")
    #     for field in self._meta.fields:
    #         if isinstance(field, models.DateTimeField):
    #             value = getattr(self, field.name)
    #             if value and value.tzinfo is None:
    #                 setattr(self, field.name, make_aware(value, timezone=timezone_jkt))

    #     super().save(*args, **kwargs)


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

    # special spatial field
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_initial_catalog'
    
    # override method for location point and timezone aware
    def save(self, *args, **kwargs):
        if self.source_lat is not None and self.source_lon is not None:
            self.location_init = Point(self.source_lon, self.source_lat)

        # timezone_jkt = ZoneInfo("Asia/Jakarta")
        # for field in self._meta.fields:
        #     if isinstance(field, models.DateTimeField):
        #         value = getattr(self, field.name)
        #         if value and value.tzinfo is None:
        #             setattr(self, field.name, make_aware(value, timezone=timezone_jkt))

        super().save(*args, **kwargs)


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

    # special spatial field
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_relocated_catalog'
    
    # override method for location point and timezone aware
    def save(self, *args, **kwargs):
        if self.source_lat is not None and self.source_lon is not None:
            self.location_reloc = Point(self.source_lon, self.source_lat)

        # timezone_jkt = ZoneInfo("Asia/Jakarta")
        # for field in self._meta.fields:
        #     if isinstance(field, models.DateTimeField):
        #         value = getattr(self, field.name)
        #         if value and value.tzinfo is None:
        #             setattr(self, field.name, make_aware(value, timezone=timezone_jkt))
                    
        super().save(*args, **kwargs)


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
        managed = False
        db_table = 'serd_picking_catalog'
    
    # # override method for timezone aware
    # def save(self, *args, **kwargs):
    #     timezone_jkt = ZoneInfo("Asia/Jakarta")
    #     for field in self._meta.fields:
    #         if isinstance(field, models.DateTimeField):
    #             value = getattr(self, field.name)
    #             if value and value.tzinfo is None:
    #                 setattr(self, field.name, make_aware(value, timezone=timezone_jkt))

    #     super().save(*args, **kwargs)


# station model
class SemlStation(models.Model):
    id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'

class SerdStation(models.Model):
    id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
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
    id = models.AutoField(primary_key=True)
    site_project = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=225, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'project_updates'
    def __str__(self):
        return self.title