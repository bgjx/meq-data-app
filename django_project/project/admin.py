from django.contrib import admin
from project.models import (SemlInitialCatalog,
                            SemlRelocatedCatalog, 
                            SemlPickingCatalog,
                            SemlStation,
                            SerdInitialCatalog,
                            SerdRelocatedCatalog, 
                            SerdPickingCatalog,
                            SerdStation,
                            Updates)

from project.config import (REQUIRED_HYPO_COLUMNS_NAME,
                            REQUIRED_PICKING_COLUMNS_NAME,
                            REQUIRED_STATION_COLUMNS_NAME)

# Register your models here.
# seml model
@admin.register(SemlInitialCatalog)
class SemlInitialCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_HYPO_COLUMNS_NAME))

@admin.register(SemlRelocatedCatalog)
class SemlRelocatedCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_HYPO_COLUMNS_NAME))

@admin.register(SemlPickingCatalog)
class SemlPickingCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_PICKING_COLUMNS_NAME))

@admin.register(SemlStation)
class SemlStationAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_STATION_COLUMNS_NAME))

# serd model
@admin.register(SerdInitialCatalog)
class SerdInitialCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_HYPO_COLUMNS_NAME))

@admin.register(SerdRelocatedCatalog)
class SerdRelocatedCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_HYPO_COLUMNS_NAME))

@admin.register(SerdPickingCatalog)
class SerdPickingCatalogAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_PICKING_COLUMNS_NAME))

@admin.register(SerdStation)
class SerdStationAdmin(admin.ModelAdmin):
    list_display = (tuple(REQUIRED_STATION_COLUMNS_NAME))


# Updates
@admin.register(Updates)
class UpdatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_project', 'username', 'title', 'type', 'description', 'file_name', 'updated_at')