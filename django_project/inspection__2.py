# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AccountEmailverification(models.Model):
    email = models.CharField(max_length=2555)
    token = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailverification'


class AccountUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    organization = models.CharField(max_length=100)
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_userprofile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FrontpageSite(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontpage_site'


class HealthCheckDbTestmodel(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'health_check_db_testmodel'


class ProjectHypocataloguplaod(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    description = models.CharField(max_length=225)
    file_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'project_hypocataloguplaod'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_relocated_catalog'


class SemlStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_relocated_catalog'


class SerdStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_station'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AccountEmailverification(models.Model):
    email = models.CharField(max_length=2555)
    token = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailverification'


class AccountUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    organization = models.CharField(max_length=100)
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_userprofile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FrontpageSite(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontpage_site'


class HealthCheckDbTestmodel(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'health_check_db_testmodel'


class ProjectHypocataloguplaod(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    description = models.CharField(max_length=225)
    file_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'project_hypocataloguplaod'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_relocated_catalog'


class SemlStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_relocated_catalog'


class SerdStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_station'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AccountEmailverification(models.Model):
    email = models.CharField(max_length=2555)
    token = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailverification'


class AccountUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    organization = models.CharField(max_length=100)
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_userprofile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FrontpageSite(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frontpage_site'


class HealthCheckDbTestmodel(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'health_check_db_testmodel'


class ProjectUpdates(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    description = models.CharField(max_length=225)
    file_name = models.CharField(max_length=50)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'project_updates'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_relocated_catalog'


class SemlStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seml_station'


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
    location_init = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_initial_catalog'


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
    location_reloc = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_relocated_catalog'


class SerdStation(models.Model):
    station_code = models.CharField(max_length=10, blank=True, null=True)
    network_code = models.CharField(max_length=10, blank=True, null=True)
    station_lat = models.FloatField(blank=True, null=True)
    station_lon = models.FloatField(blank=True, null=True)
    station_elev_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serd_station'
