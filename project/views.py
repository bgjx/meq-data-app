from django.shortcuts import render
from django.shortcuts import get_object_or_404
from frontpage.models import Site
import project.models as mdl
import plotly.graph_objects as go
from plotly.io import to_html
import pandas as pd
from datetime import datetime
import project.utils as utl

def project_site(request, site_slug = None):
    site = get_object_or_404(Site, slug=site_slug)

    # find the spesific models matching the site_slug and type of catalog
    db_table_wcc = utl.get_model(mdl, site_slug, "wcc")
    data_wcc = db_table_wcc.values()
    df_wcc = pd.DataFrame(list(data_wcc))

    db_table_nll = utl.get_model(mdl, site_slug, "nll")
    data_nll = db_table_nll.values()
    df_nll = pd.DataFrame(list(data_nll))

    # create visualizattion
    df_show_wcc = df_wcc.tail(10)
    df_show_nll = df_nll.tail(10)


    table_html_wcc = utl.plot_table(df_show_wcc)
    table_html_nll = utl.plot_table(df_show_nll)
    context = {
        'site': site,
        'table_html_wcc': table_html_wcc,
        'table_html_nll': table_html_nll
    }

    return render(request, 'project/site-analytics.html', context)