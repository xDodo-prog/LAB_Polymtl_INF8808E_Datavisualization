'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
import hover_template

from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.
    '''

    # Create an empty scatter plot
    fig = px.scatter()  # empty figure

    # Add annotation text in the center of the figure
    fig.add_annotation(
        text='No data to display. Select a cell in the heatmap for more information.',
        xref='paper', yref='paper',
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=THEME["dark_color"]),
        align='center'
    )

    # Update layout to hide axes and apply theme background colors
    fig.update_layout(
        dragmode=False,  # Disable dragging
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor=THEME["background_color"],
        paper_bgcolor=THEME["background_color"]
    )

    # Add a rectangle behind the text for better readability
    add_rectangle_shape(fig)

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    # Add background rectangle shape to enhance visibility of the annotation
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=0, x1=1,  # full width
        y0=0.25, y1=0.75,  # partial height
        fillcolor=THEME["pale_color"],
        line=dict(width=0),  # no border
        layer="below"  # place behind all other elements
    )
    return fig


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicate the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    if len(line_data) == 1:
        # Single data point: use scatter plot
        fig = px.scatter(
            line_data,
            x="Date_Plantation",
            y="Counts",
            labels={"Counts": "Trees"},
            title=f"{arrond} - {year}"
        )
    else:
        # Multiple data points: use line chart
        fig = px.line(
            line_data,
            x="Date_Plantation",
            y="Counts",
            labels={"Counts": "Trees"},
            title=f"{arrond} - {year}"
        )

    # Customize layout and axis formatting
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Trees",
        xaxis_tickformat="%d\n%b",  # Day as 2-digit number and abbreviated month
        dragmode=False  # Disable interactive dragging
    )

    # Apply hover template and line color from the theme
    fig.update_traces(
        hovertemplate=hover_template.get_linechart_hover_template(),
        line_color=THEME["line_chart_color"]
    )

    return fig
