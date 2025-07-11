# Generated by Django 5.2.3 on 2025-07-05 07:43

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SemlCatalogMergedView',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('source_lat_init', models.FloatField(blank=True, null=True)),
                ('source_lon_init', models.FloatField(blank=True, null=True)),
                ('location_init', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('source_depth_m_init', models.FloatField(blank=True, null=True)),
                ('source_origin_dt_init', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s_init', models.FloatField(blank=True, null=True)),
                ('gap_init', models.FloatField(blank=True, null=True)),
                ('remarks_init', models.CharField(blank=True, max_length=10, null=True)),
                ('source_lat_reloc', models.FloatField(blank=True, null=True)),
                ('source_lon_reloc', models.FloatField(blank=True, null=True)),
                ('location_reloc', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('source_depth_m_reloc', models.FloatField(blank=True, null=True)),
                ('source_origin_dt_reloc', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s_reloc', models.FloatField(blank=True, null=True)),
                ('remarks_reloc', models.CharField(blank=True, max_length=10, null=True)),
                ('network_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_lat', models.FloatField(blank=True, null=True)),
                ('station_lon', models.FloatField(blank=True, null=True)),
                ('station_elev_m', models.FloatField(blank=True, null=True)),
                ('p_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('s_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('coda_dt', models.DateTimeField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'seml_catalog_merged_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemlInitialCatalog',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_lat', models.FloatField(blank=True, null=True)),
                ('source_lon', models.FloatField(blank=True, null=True)),
                ('source_depth_m', models.FloatField(blank=True, null=True)),
                ('source_origin_dt', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s', models.FloatField(blank=True, null=True)),
                ('n_phases', models.IntegerField(blank=True, null=True)),
                ('source_gap_degree', models.FloatField(blank=True, null=True)),
                ('x_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('y_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('z_depth_err_m', models.FloatField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
                ('location_init', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'seml_initial_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemlPickingCatalog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('p_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('p_polarity', models.CharField(blank=True, max_length=5, null=True)),
                ('p_onset', models.CharField(blank=True, max_length=5, null=True)),
                ('s_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('coda_dt', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'seml_picking_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemlRelocatedCatalog',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_lat', models.FloatField(blank=True, null=True)),
                ('source_lon', models.FloatField(blank=True, null=True)),
                ('source_depth_m', models.FloatField(blank=True, null=True)),
                ('source_origin_dt', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s', models.FloatField(blank=True, null=True)),
                ('n_phases', models.IntegerField(blank=True, null=True)),
                ('source_gap_degree', models.FloatField(blank=True, null=True)),
                ('x_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('y_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('z_depth_err_m', models.FloatField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
                ('location_reloc', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'seml_relocated_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemlStation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('network_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_lat', models.FloatField(blank=True, null=True)),
                ('station_lon', models.FloatField(blank=True, null=True)),
                ('station_elev_m', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'seml_station',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SerdCatalogMergedView',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('source_lat_init', models.FloatField(blank=True, null=True)),
                ('source_lon_init', models.FloatField(blank=True, null=True)),
                ('location_init', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('source_depth_m_init', models.FloatField(blank=True, null=True)),
                ('source_origin_dt_init', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s_init', models.FloatField(blank=True, null=True)),
                ('gap_init', models.FloatField(blank=True, null=True)),
                ('remarks_init', models.CharField(blank=True, max_length=10, null=True)),
                ('source_lat_reloc', models.FloatField(blank=True, null=True)),
                ('source_lon_reloc', models.FloatField(blank=True, null=True)),
                ('location_reloc', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('source_depth_m_reloc', models.FloatField(blank=True, null=True)),
                ('source_origin_dt_reloc', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s_reloc', models.FloatField(blank=True, null=True)),
                ('remarks_reloc', models.CharField(blank=True, max_length=10, null=True)),
                ('network_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_lat', models.FloatField(blank=True, null=True)),
                ('station_lon', models.FloatField(blank=True, null=True)),
                ('station_elev_m', models.FloatField(blank=True, null=True)),
                ('p_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('s_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('coda_dt', models.DateTimeField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'serd_catalog_merged_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SerdInitialCatalog',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_lat', models.FloatField(blank=True, null=True)),
                ('source_lon', models.FloatField(blank=True, null=True)),
                ('source_depth_m', models.FloatField(blank=True, null=True)),
                ('source_origin_dt', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s', models.FloatField(blank=True, null=True)),
                ('n_phases', models.IntegerField(blank=True, null=True)),
                ('source_gap_degree', models.FloatField(blank=True, null=True)),
                ('x_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('y_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('z_depth_err_m', models.FloatField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'serd_initial_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SerdPickingCatalog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('p_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('p_polarity', models.CharField(blank=True, max_length=5, null=True)),
                ('p_onset', models.CharField(blank=True, max_length=5, null=True)),
                ('s_arrival_dt', models.DateTimeField(blank=True, null=True)),
                ('coda_dt', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'serd_picking_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SerdRelocatedCatalog',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_lat', models.FloatField(blank=True, null=True)),
                ('source_lon', models.FloatField(blank=True, null=True)),
                ('source_depth_m', models.FloatField(blank=True, null=True)),
                ('source_origin_dt', models.DateTimeField(blank=True, null=True)),
                ('source_err_rms_s', models.FloatField(blank=True, null=True)),
                ('n_phases', models.IntegerField(blank=True, null=True)),
                ('source_gap_degree', models.FloatField(blank=True, null=True)),
                ('x_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('y_horizontal_err_m', models.FloatField(blank=True, null=True)),
                ('z_depth_err_m', models.FloatField(blank=True, null=True)),
                ('magnitude', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'serd_relocated_catalog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SerdStation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('station_code', models.CharField(blank=True, max_length=10, null=True)),
                ('network_code', models.CharField(blank=True, max_length=10, null=True)),
                ('station_lat', models.FloatField(blank=True, null=True)),
                ('station_lon', models.FloatField(blank=True, null=True)),
                ('station_elev_m', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'serd_station',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=25, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=25, null=True)),
                ('description', models.CharField(blank=True, max_length=225, null=True)),
                ('file_name', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
