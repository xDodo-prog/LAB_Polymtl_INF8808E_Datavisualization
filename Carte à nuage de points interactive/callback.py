'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html


def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle no clicks on the map
    return None, None, None, None
    


def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle clicks on the map base
    return title, mode, theme, style


def map_marker_clicked(figure, curve, point, title, mode, theme, style): 
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle clicks on the markers
    
  # Retrieve the title text from the clicked marker's custom data
    clicked_title = figure['data'][curve]['customdata'][0][point]

    # Create a Dash HTML Div for the title with marker color styling
    updated_title = html.Div(
        clicked_title,
        style={'color': figure['data'][curve]['marker']['color']}
    )

    # Extract the mode and theme info linked to the clicked marker
    updated_mode = figure['data'][curve]['customdata'][2][point]
    theme_text = figure['data'][curve]['customdata'][1][point]

    # If theme exists, convert it into an HTML list
    if theme_text:
        theme_lines = theme_text.split('\n')
        updated_theme = html.Div([
            html.P('Theme:'),
            html.Ul([html.Li(item) for item in theme_lines])
        ])
    else:
        updated_theme = None

    # Define styling for the panel container
    updated_style = {
        'border': '1px solid black',
        'padding': '10px'
    }

    return updated_title, updated_mode, updated_theme, updated_style