'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px

import hover_template as hover

COLOR_TEMPLATE = {
    'Noyau villageois': px.colors.qualitative.Plotly[0],
    'Passage entre rues résidentielles': px.colors.qualitative.Plotly[1],
    'Rue bordant un bâtiment public ou institutionnel': px.colors.qualitative.Plotly[2],
    'Rue commerciale de quartier, d’ambiance ou de destination': px.colors.qualitative.Plotly[3],
    'Rue en bordure ou entre deux parcs ou place publique': px.colors.qualitative.Plotly[4],
    'Rue entre un parc et un bâtiment public ou institutionnel': px.colors.qualitative.Plotly[5],
    'Rue transversale à une rue commerciale': px.colors.qualitative.Plotly[6],
}
def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        The opacity of the map background color should be 0.2.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''
    # TODO : Draw the map base
    fig = px.choropleth_mapbox(
        geojson=montreal_data,
        locations=locations,
        color=z_vals,
        color_continuous_scale=colorscale,
        opacity=0.2,
        featureidkey='properties.NOM',
    ).update_layout(
        coloraxis_showscale=False,
        margin={"r":0,"t":110,"l":0,"b":0},
    ).update_traces(
        hovertemplate=hover.map_base_hover_template(),
    )

    return fig


def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        The marker size should be 20.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    # TODO : Add the scatter markers to the map base
    interventions = street_df.groupby('properties.TYPE_SITE_INTERVENTION')

    for name, data in interventions :
        fig.add_trace(
            go.Scattermapbox(
                name=name,
                lat=data['properties.LATITUDE'],
                lon=data['properties.LONGITUDE'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=20,
                    color=COLOR_TEMPLATE[name]
                ),
                hovertemplate=hover.map_marker_hover_template(name),
                customdata=[
                    data['properties.NOM_PROJET'],
                    data['properties.OBJECTIF_THEMATIQUE'],
                    data['properties.MODE_IMPLANTATION'],
                ],
            )
        )

    return fig
