from django.contrib.gis.db import models

# Create your models here.
class SemlCatNll(models.Model):
    event_id = models.IntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    utm_x_m = models.FloatField(blank=True, null=True)
    utm_y_m = models.FloatField(blank=True, null=True)
    depth_m = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    second = models.FloatField(blank=True, null=True)
    dt_origin = models.DateTimeField(blank=True, null=True)
    rms_error = models.FloatField(blank=True, null=True)
    ml_mag = models.FloatField(blank=True, null=True)
    mw_mag = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'seml_cat_nll'


class SemlCatPick(models.Model):
    event_id = models.IntegerField(blank=True, null=True)
    station = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minutes_p = models.IntegerField(blank=True, null=True)
    p_arr_sec = models.FloatField(blank=True, null=True)
    p_polarity = models.CharField(max_length=10, blank=True, null=True)
    p_onset = models.CharField(max_length=10, blank=True, null=True)
    minutes_s = models.IntegerField(blank=True, null=True)
    s_arr_sec = models.FloatField(blank=True, null=True)
    s_polarity = models.CharField(max_length=10, blank=True, null=True)
    s_onset = models.CharField(max_length=10, blank=True, null=True)
    ts_tp = models.FloatField(blank=True, null=True)
    minutes_origin = models.IntegerField(blank=True, null=True)
    seconds_origin = models.FloatField(blank=True, null=True)
    p_travel = models.FloatField(blank=True, null=True)
    s_travel = models.FloatField(blank=True, null=True)
    vp_vs = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_cat_pick'


class SemlCatWcc(models.Model):
    event_id = models.IntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    utm_x_m = models.FloatField(blank=True, null=True)
    utm_y_m = models.FloatField(blank=True, null=True)
    depth_m = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    second = models.FloatField(blank=True, null=True)
    dt_origin = models.DateTimeField(blank=True, null=True)
    rms_error = models.FloatField(blank=True, null=True)
    ml_mag = models.FloatField(blank=True, null=True)
    mw_mag = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_cat_wcc'


class SerdCatNll(models.Model):
    event_id = models.IntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    utm_x_m = models.FloatField(blank=True, null=True)
    utm_y_m = models.FloatField(blank=True, null=True)
    depth_m = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    second = models.FloatField(blank=True, null=True)
    dt_origin = models.DateTimeField(blank=True, null=True)
    rms_error = models.FloatField(blank=True, null=True)
    ml_mag = models.FloatField(blank=True, null=True)
    mw_mag = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_cat_nll'


class SerdCatPick(models.Model):
    event_id = models.IntegerField(blank=True, null=True)
    station = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minutes_p = models.IntegerField(blank=True, null=True)
    p_arr_sec = models.FloatField(blank=True, null=True)
    p_polarity = models.CharField(max_length=10, blank=True, null=True)
    p_onset = models.CharField(max_length=10, blank=True, null=True)
    minutes_s = models.IntegerField(blank=True, null=True)
    s_arr_sec = models.FloatField(blank=True, null=True)
    s_polarity = models.CharField(max_length=10, blank=True, null=True)
    s_onset = models.CharField(max_length=10, blank=True, null=True)
    ts_tp = models.FloatField(blank=True, null=True)
    minutes_origin = models.IntegerField(blank=True, null=True)
    seconds_origin = models.FloatField(blank=True, null=True)
    p_travel = models.FloatField(blank=True, null=True)
    s_travel = models.FloatField(blank=True, null=True)
    vp_vs = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_cat_pick'


class SerdCatWcc(models.Model):
    event_id = models.IntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    utm_x_m = models.FloatField(blank=True, null=True)
    utm_y_m = models.FloatField(blank=True, null=True)
    depth_m = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    second = models.FloatField(blank=True, null=True)
    dt_origin = models.DateTimeField(blank=True, null=True)
    rms_error = models.FloatField(blank=True, null=True)
    ml_mag = models.FloatField(blank=True, null=True)
    mw_mag = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_cat_wcc'


# station model
class SemlStation(models.Model):
    sta_id = models.CharField(max_length=100, primary_key=True)
    sta = models.CharField(max_length=10, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'

class SerdStation(models.Model):
    sta_id = models.CharField(max_length=100, primary_key=True)
    sta = models.CharField(max_length=10, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_station'