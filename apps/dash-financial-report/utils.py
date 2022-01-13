from dash import html, dcc

APP_CONSTANTS = {
    "graph_color" : '#23359d'
}


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        [
                            html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="logo",)
                        ],
                        href="/",
                    )
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Business Impact Analysis Dashboard")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/overview",
                className="tab first",
            ),
            dcc.Link(
                "Price Performance",
                href="/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Portfolio & Management",
                href="/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "Fees & Minimums", href="/fees", className="tab"
            ),
            dcc.Link(
                "Distributions",
                href="/distributions",
                className="tab",
            ),
            dcc.Link(
                "News & Reviews",
                href="/news-and-reviews",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def generateRelationshipDict(dframe):
    depts_relationship = {}
    for index, row in dframe.iterrows():
        # Get current row column details
        curr_core_function = row.CoreFunction
        curr_other_core_function = row.OtherCoreFunction
        curr_ipop = row.InputOrOutput
        # Iterate through the OtherDepts column
        
        for r in row.OtherDepts:
            
            # If the department already exists in the dictionary, append
            if r in depts_relationship.keys():
                for cf in curr_core_function:
                    if cf not in depts_relationship[r]["CoreFunction"]:
                        depts_relationship[r]["CoreFunction"].append({
                            cf: curr_ipop
                            })
                for ocf in curr_other_core_function:
                    if ocf not in depts_relationship[r]["OtherCoreFunction"]\
                    and ocf!='None':
                        depts_relationship[r]["OtherCoreFunction"].append({
                            ocf: curr_ipop
                            })
            # Else, add a new    
            else:
                depts_relationship[r] = {
                    'CoreFunction':[{c:curr_ipop} 
                        for c in curr_core_function],
                    'OtherCoreFunction': [{c:curr_ipop} 
                        for c in curr_other_core_function if c!='None']
                    }
    return depts_relationship

def getAcronym(word, character_lim=7):
    '''
    Creates acronym based on character limit
    '''
    if len(word) > character_lim:
        word = "".join(e[0] for e in word.split())
    return word

def checkDepartmentEssential(dept, list):
    '''
    Classifies a department as core or non-core
    '''

def generateNodes(data_dictionary, root_label='JPW',
                  color='#003366'):
    root_node = {'id': 0, 
                 'label': root_label ,
                 'color': '#FFFFFF',
                 'font': {
                             'face': 'Helvetica Neue',
                             'size': 10,
                             'color': '#000000'
                            },
                 }
    additional_nodes = [{'id': i, 
                         'label':  getAcronym(key),
                         'color':color,
                         'title': key,
                         'shape': 'circle',
                         'font': {
                             'face': 'Helvetica Neue',
                             'size': 10,
                             'color': '#FFFFFF'
                            },
                         'widthConstraint': {
                             
                             }
                         } 
                    for i, key in enumerate(data_dictionary)]
    additional_nodes.append(root_node)
    return additional_nodes

def generateEdges(data_dictionary, scalefactor = 0.5):
    '''
    Generate to and fro edges
    '''
    edges = []
    for i, dept in enumerate(data_dictionary):
        # Counts for scaling the intensity
        core_function_count = 0
        other_function_count = 0
        # Classifying input and output edges
        input, output = [], []
        for cf in data_dictionary[dept]['CoreFunction']:
            if list(cf.values())[0].lower() == 'input from':
                input.append(list(cf.keys())[0])
            else:
                output.append(list(cf.keys())[0])
            core_function_count +=1
        for ocf in data_dictionary[dept]['OtherCoreFunction']:
            if list(ocf.values())[0].lower() == 'input from':
                input.append(list(ocf.keys())[0])
            else:
                output.append(list(ocf.keys())[0])
            other_function_count +=1
        # Check if input or output is empty
        if not input:
            pass
        else:
            input_from = {
                'id':f'{i}-0', 
                'from': i,
                'to': 0,
                'title': f'{input}',
                'arrows': {
                    'to': {
                        'enabled' : True,
                        'scaleFactor': scalefactor
                    }
                },
                'chosen':{
                    'label': True
                }
            }
            edges.append(input_from)
        if not output:
            pass
        else:
            output_to = {
                'id':f'0-{i}', 
                'from': 0,
                'to': i,
                'title': f'{output}',
                'arrows': {
                    'to': {
                        'enabled' : True,
                        'scaleFactor': scalefactor
                    }
                },
                'chosen':{
                    'label': True
                }
            }
            edges.append(output_to)
    return edges
    
