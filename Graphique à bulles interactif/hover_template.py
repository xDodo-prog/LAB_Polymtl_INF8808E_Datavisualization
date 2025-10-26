'''
    Provides the template for the tooltips.
'''


def get_bubble_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    # TODO : Generate tooltip

    return '<span style="font-weight:bold">Country : </span><span>%{customdata[0]}</span><br><span style="font-weight:bold">Population : </span><span>%{customdata[3]}</span><br><span style="font-weight:bold">GDP : </span><span>%{customdata[1]} $ (USD)</span><br><span style="font-weight:bold">CO2 : </span><span>%{customdata[2]} metric tonnes</span><extra></extra>'
    
