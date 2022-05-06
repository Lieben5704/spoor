# -*- coding: utf-8 -*-
                          #replace dbc with dcc
"""
Created on Mon Jan 27 09:50:58 2020

@author: paulinep

This file was updated on 21 May 2020. Added Comfort Check, Updated Layout 
1 July 2021 - Fix email funtionality after gmail security change
"""

import os 
from random import randint 

import flask ##from example

from dash import Dash, html, dcc, Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html

# from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

#bootstrap components
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

###https://github.com/lavr/python-emails
#import for sending mails
import emails  #added 1 July 2021


global df
global df2
global df3
global df4
global cz
global orient
global p_h
global g


#read the data

df4=pd.read_csv('glazing_groups2020_05_13.csv') 
df6=pd.read_csv('occupant_distance_pictures.csv')
df7=pd.read_csv('AllowableGlazingTempsSet.csv')


#colours used in the app
colors={'light_back':'#ffffff', 'background':'#f0f1f2','text':'#5d5f61','text2':'#3a3a3d','single':'#7f9fff','singlelowe':'#fff47f','double':'#ffbd7f','doublelowe':'#ff7f7f',
        'rational':'#edf2f2','line':'#000000','grey':'#c9c9c9','dark':'#636363','light':'#e2eb71','venetian':'#81b0b8',
        'dist05':'#f50000','dist1':'#5f59cf','dist15':'#59cf5f',
        'inputs':'#2200ff','outputs':'#3d9999','background2':'#adc4c4','background3':'#ededed','green1':'#00FF00','amber1':'#FFBD00','red1':'#FF0000','light_blue':'#cce7e8'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#added for live web#
server = flask.Flask(__name__)  
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000))) #


#added server:
app = Dash(__name__, server=server,
                external_stylesheets=external_stylesheets,
                )

app.title="Spoormaker Glazing Tool"

##define the layout of the app
app.layout = html.Div(className='main-background',children=[
                        html.Div(className="col-lg-5 col-md-11 col-sm-11 heading-sec container",children=[        
                            html.Div(className="row justify-content-center heading-sec-row ",children=[
                                html.Img(src='/assets/SP_icon.jpg'),
                                html.H2('SPOORMAKER'),
                                html.Div(className="heading-spacer"),
                                html.H2('SUMMER COMFORT TOOL'),
                                ]),
                            html.Div(className="col-12 text-center",children=[
                                html.H4(className="text-muted",children=[
                                    html.P('THIS TOOL IS INTENDED FOR USE IN THE EARLY DESIGN PHASE OF AIR-CONDITIONED BUILDINGS IN SOUTH AFRICA'),
                                    html.A('CONTACT',href="#contact-page"),
                                    html.Span(' SPOORMAKER AND PARTNERS '),
                                    html.Span(children=['FOR GLAZING SELECTIONS, SANS10400XA RATIONAL ASSESSMENTS, THERMAL COMFORT ASSESSMENTS']),
                                    ]),
                                ]),

                            ]),
                         

                        html.Div(className='row main-page justify-content-center',children=[    
                            html.Div(className='col-lg-5 col-md-11 row container input-sec',children=[    
                                html.H2(className='col-6',children=['INPUTS: ']),  
                                html.H2(className='col-6',children='OUTPUTS:'),     
                                html.Div(className='col-6',children=[
                                    html.H6("City:"), #style={'color':colors['text2']}
                                    dcc.Dropdown(
                                        id='climatic-zone',
                                        options=[
                                            {'label': 'Johannesburg', 'value': 1},
                                            {'label': 'Pretoria', 'value': 2},
                                            {'label': 'Cape Town', 'value': 4},
                                            {'label': 'Durban', 'value': 5}
                                            ],
                                        value=1
                                        ),
                                    html.H6("Orientation:"),
                                    dcc.Dropdown(
                                        id='orientation',
                                        options=[
                                            {'label': 'North', 'value': 'North'},
                                            {'label': 'North East', 'value': 'NorthEast'},
                                            {'label': 'East', 'value': 'East'},
                                            {'label': 'South East', 'value': 'SouthEast'},
                                            {'label': 'South', 'value': 'South'},
                                            {'label': 'South West', 'value': 'SouthWest'},
                                            {'label': 'West', 'value': 'West'},
                                            {'label': 'North West', 'value': 'NorthWest'}
                                            ],
                                        value='North'
                                        ),  
                                    html.H6("GlazingType:"),
                                    dcc.Dropdown(
                                        id='glass-type',
                                        options=[
                                            {'label':i,'value':i} for i in df4.GlassTypeDescription.unique()
                                        ],
                                        value='Single Low E (SHGC 0.62)'   
                                        ),
                                    html.H6("Window size:"), #,style={'textAlign':'left','color':colors['text2']}
                                    dcc.Dropdown(
                                        id='window-size',
                                        options = [
                                           {'label':i,'value':i} for i in df7.WindowSize.unique()  ####sillheight
                                            ],
                                        value= "1.8m x 1.8m"
                                        ), 
                                    
                                    # html.H6("Shading P/H:"),
                                    # dcc.Dropdown(className='',
                                    #         id='p_h',
                                    #         options=[
                                    #             {'label': '0', 'value': 0 },
                                    #             {'label': '0.2', 'value': 0.2 },
                                    #             {'label': '0.4', 'value': 0.4 },
                                    #             {'label': '0.6', 'value': 0.6 },
                                    #             {'label': '0.8', 'value': 0.8 },
                                    #             {'label': '1.0', 'value': 1.0 },
                                    #             {'label': '1.2', 'value': 1.2 },
                                    #             {'label': '1.4', 'value': 1.4 },
                                    #             {'label': '1.6', 'value': 1.6 },
                                    #             {'label': '1.8', 'value': 1.8 },
                                    #             {'label': '2.0', 'value': 2.0 },
                                    #             ],
                                    #         value=0
                                    #         ),
                                    # html.H6(className='', children=["Shading G:"]),
                                    # dcc.Dropdown(className='',
                                    #         id='g-max',
                                    #         options=[
                                    #             {'label': '0-100', 'value': 100 },
                                    #             {'label': '100-500', 'value': 500 },
                                    #             {'label': '500-1200', 'value': 1200 },  
                                    #             {'label': '>1200', 'value': 10000 },                                            
                                                
                                    #         ],
                                    #         value=100
                                    #         ), 
                                    html.H6(className="",children="Occupant Distance to Facade[m]:"),       
                                    dcc.Dropdown(
                                      id='occupant-distance',
                                      options=[
                                        {'label':i,'value':i} for i in df7.OccupantDistance.unique()
                                        ],
                                      value=1 
                                      ),                                         
                                            
                                    html.H6("Sill Height:"),#,style={'textAlign':'left','color':colors['text2']}
                                    dcc.Dropdown(
                                        id='sill-height',
                                        options=[
                                            {'label':i,'value':i} for i in df7.sill_height.unique()
                                            ],
                                        value=0.9   
                                        ),      
                                        
                                    html.H6("Internal Blind Type:"),
                                     
                                    dcc.Dropdown(
                                        id='blind-type',
                                        options=[
                                            {'label': 'Light Roller', 'value': 'LightBlind'},
                                            {'label': 'Medium Roller', 'value': 'MediumBlind'},                                                    
                                            {'label': 'Dark Roller', 'value': 'DarkRollerBlind'},                                                    
                                            {'label': 'Venetian', 'value': 'VenetianBlind'},                                                    
                                        ],
                                        value = 'MediumBlind'
                                        ),                                                 
                                ]),
    

                                html.Div(className='col-6',children=[                                   
                                    html.H6("Estimated Comfort Level:"),
                                    html.Div(className='container shadow-none border bg-light text-dark',children=[  
                                        html.H6(id='comfort-output'),
                                        html.Img(className="result-icon ",id='display-comfort'),
                                        html.H6("for a person directly in front of the window"),
                                        ]),                                    
                                    html.Img(className="row app-pics",id='display-window'),
                                    html.Img(className="row app-pics",id='display-dist', src='children'), 
                                    #html.Img(className="row app-pics",src='/assets/SANS204_2.png'),                                
                                    html.Img(className="row app-pics",id='display-blind'),
                                    ]),
                            ]),

                              
                                ]),                   
                        

                            html.Div(className='contact-background',children=[
                                html.Div(className='contact-details  col-md-6 col-sm-11  offset-sm-1 offset-lg-6 ',children=[   
                                    html.H2('CONTACT US:',id="contact-page"),                
                                    html.Div(className='',children=[
                                        html.Form(children=[        
                                                dcc.Input(className="col-12",
                                                    type="text",
                                                    placeholder="Your Name",
                                                    id="person_name"
                                                    ),
                                                dcc.Input(className="col-6 float-left",
                                                    type="email",
                                                    placeholder="Your Email",
                                                    id="email"
                                                    ),
                                                dcc.Input(className="col-6 float-right",
                                                    type="tel",
                                                    placeholder="Your Phone Number",
                                                    id="phone"
                                                    ),  

                                                html.Br(),
                                                html.Br(),
                                                html.H4("PLEASE CHECK THE SERVICES YOU ARE INTERESTED IN:"),
                                                html.Div(className=" ",children=[
                                                    dcc.Checklist(className="",
                                                    id="checkbox-services",                                              
                                                    options=[
                                                         {"label": "SANS10400XA RATIONAL ASSESSMENTS", "value": "SANS10400XA RATIONAL ASSESSMENTS"},
                                                         {"label": "GLAZING SELECTION/COMFORT STUDIES", "value": "GLAZING SELECTION/COMFORT STUDIES"},
                                                         {"label": "BUILDING PERFORMANCE/OPTIMIZATION", "value": "BUILDING PERFORMANCE/OPTIMIZATION"},
                                                         {"label": "DATACENTRE CFDs", "value": "DATACENTRE CFDs"},
                                                         
                                                    ],
                                                    labelStyle = dict(display='block')
                                                    ),
                                                    ]),
                                                html.Br(),
                                               
                                                dcc.Textarea(className="col-12",
                                                    id="message",
                                                    placeholder="Type your message here.",                                                                  
                                                    rows=4
                                                    ),
                                                html.Button(className="",
                                                    id="submit-1",
                                                    children=["Send your message"]                                                   
                                                    ),
                                                html.H6(className="text-light", 
                                                    id="message_sent",                                                   
                                                    children=["You will receive an email message to confirm that your message was sent successfully"]), 
            
                                        ]),#end form
                                    html.Br(),
                                    html.H2('SPOORMAKER AND PARTNERS:'),
                                    html.P(className="",children=[
                                       html.Span('|   '),
                                       html.A('http://www.spoormaker.co.za ',href="https://www.spoormaker.co.za"),
                                       html.Span('|   +27 12 663 3125   |'),
                                        ]),     
                                    html.H2(children=[
                                        html.A("OTHER SERVICES:",href="https://www.spoormaker.co.za/what-we-offer"),

                                        ]),
                                    # html.Br(),
                                    html.P(className="row other-services",children=[
                                            html.A('| MECHANICAL | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=12"),
                                            html.A('| ELECTRICAL | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=13"),
                                            html.A('| WET SERVICES | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=16"),
                                            html.A('| FIRE PROTECTION | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=15"),
                                            html.A('| ENERGY MANAGEMENT & WATER MANAGEMENT | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=14"),
                                            html.A('| MEFP QUANTITY SURVEYING BUILDING TOOLS | ',href="https://www.spoormaker.co.za/what-we-offer?nid_entityreference_filter=17"),  
                                            ]),    
                                    ]), 
                                ]),
                            ]),
                                                             
                            html.Div(className='col-12 page-footer ',children=[ 
                                html.P(className='small &copy',children=['Spoormaker & Partners do not accept responsibility for any inaccuracies within the Spoormaker Summer Comfort Tool and shall not be liable for any errors, expense and/or loss resulting from the use of the Spoormaker Summer Comfort Tool.']),
                                html.P(className='small &copy',children=['©Copyright 2022, SPOORMAKER AND PARTNERS'])
                            ]),                                              
                        ])                           
        
                                
@app.callback(
    Output(component_id="message-sent",component_property="children"), 
    [Input("submit-1", "n_clicks"),
    Input('person_name','value'),
    Input('email','value'),
    Input('phone','value'),
    Input('message','value'),
    Input('checkbox-services','value')]
)
def on_button_click(n,name,email,phone,message,services):
    
    if n != None:
        if email == None:
            feedback="No email address was given"  

            return feedback

        message1="""
        <p>Thank you for your enquiry!
        <p>Your message was sent successfully       
        <p>Your Message: {}  
        <p>Services marked as areas of interest: {}
        <br>
        <p>We have your details as:
        <p>Name: {}
        <p>Email:{}
        <p>Phone: {}
        <p>Should you not hear from us within 48 hours, please call our office at 012 663 31 25
        <p>Kind regards 
        <p>Pauline Prinsloo

            """.format(message,services,name,email,phone)

        # sender_email = "paulinep@spoormaker.co.za"##1 Jun 2021
        # receiver_email = email,"paulinep@spoormaker.co.za","paulinep@dtm-gauteng.co.za"  ##1 MAY 2022
        # message = emails.html(html=message1,
        #                subject="Spoormaker Building Physics Enquiry",
        #                mail_from=('Spoormaker Building Physics Department', sender_email))


        username1 ='btgscan@letsinvest.co.za'
        password1 = 'N3wy0rk!@#$'
        server1 = 'mail.letsinvest.co.za'
        port1 = 587
        receiver_email = email,"paulinep@spoormaker.co.za","paulinep@dtm-gauteng.co.za" 

        message = emails.html(html=message1,
                       subject="Spoormaker Building Physics Enquiry",
                       mail_from=('Spoormaker Building Physics Department', username1))

        try:
            #initializing the server connection
            r = message.send(to=receiver_email, smtp={'host': server1, 'port':port1,'user':username1,'password':password1,'timeout': 5})
            assert r.status_code == 250
            
            feedback=["Email sent successfully"]
           
            r.quit()
            return feedback

        except:
            feedback="Error, email was not sent"
    
            return feedback                            

     
                                                        

                 
@app.callback(
    Output(component_id='comfort-output', component_property='children'),
    [Input(component_id='occupant-distance', component_property='value'),
     Input(component_id='sill-height', component_property='value'),
     Input(component_id='window-size', component_property='value'),
     Input(component_id='glass-type', component_property='value'),
     Input(component_id='blind-type', component_property='value'),
     
     Input('orientation', 'value'),
     #Input('p_h', 'value'),
     ]    
)  
def update_output_div(occupant_distance, sill_height, window_size,glass_type,blind_type,orient):
#def update_output_div(occupant_distance, sill_height, window_size,glass_type,blind_type,orient,p_h):
    
    
###check comfort due to radiant heat
    p_h=0 ######################################################  delete this line if p/h is reintroduced
    if (orient ==  'North' and p_h > 0.5) or (orient ==  ('South' or 'SouthEast')):
        solar_rad='400'    
        blind_ref=solar_rad+'Temp_'+blind_type
        surface_temp = df4[df4['GlassTypeDescription'] ==glass_type][blind_ref].item()
    else: 
        solar_rad='783'    
        blind_ref=solar_rad+'Temp_'+blind_type
        surface_temp = df4[df4['GlassTypeDescription'] ==glass_type][blind_ref].item()
                                              
    allowable_glass_temp = df7[df7["OccupantDistance"]==occupant_distance][df7["WindowSize"]==window_size][df7["sill_height"]==sill_height]['Max_surf_temp'].values[0]
    
    if allowable_glass_temp > surface_temp:
        comfort_level = "Comfort problems are unlikely"
    elif (surface_temp - allowable_glass_temp) <= 1.5:
        comfort_level = "Comfort problems could be experienced"
    elif (surface_temp - allowable_glass_temp) > 1.5:
        comfort_level = "Comfort problems are likely"        

###this section was removed as it is a summer comfort tool
#### check winter comfort - more than 55% glazing with single or single low e = discomfort
    # if orient ==  ('South' or 'SouthEast' or 'SouthWest') and float((df7[df7["OccupantDistance"]==occupant_distance][df7["WindowSize"]==window_size][df7["sill_height"]==sill_height]['percentage_glazing'].values[0])  > 0.55) and (df4[df4['GlassTypeDescription'] ==glass_type]['U_value_excl_frame'].values[0] > 3) :
    #     comfort_level = "Comfort problems are likely"    

     
    return comfort_level


@app.callback(
    Output('display-comfort', 'src'),
    [Input('comfort-output', 'children'),
   ])
def comfort_image(comfort_output):

    
    if comfort_output == "Comfort problems are unlikely":
        image_location = '/assets/happy.png'
    elif comfort_output == "Comfort problems could be experienced":
        image_location = '/assets/neutral.png'
    elif comfort_output == "Comfort problems are likely" :
        image_location = '/assets/sad.png'            

    return image_location


@app.callback(
    Output('display-dist', 'src'),
    [Input('occupant-distance', 'value'),
     Input('sill-height', 'value')])
def callback_image(occupant_d, sill_h):
    occupant_distance=float(occupant_d)
    sill_height=float(sill_h)
    image_location = '/assets/' + df6[df6['occupant_distance']==occupant_distance][(df6['sill_height']==sill_height)]['image'].values[0]

    return image_location


@app.callback(
    Output('display-blind', 'src'),
    [Input('blind-type', 'value')])
def callback_image2(blind_type):
    
    if blind_type=='LightBlind': image_location2 = '/assets/light_blind.png'
    if blind_type=='MediumBlind': image_location2 = '/assets/medium_blind.png'
    if blind_type=='DarkRollerBlind': image_location2 = '/assets/dark_blind.png'
    if blind_type=='VenetianBlind': image_location2 = '/assets/venetian_blind.png'        
    return image_location2

@app.callback(
    Output('display-window', 'src'),
    [Input('window-size', 'value'),
     Input('sill-height', 'value')])
def callback_image_window(window_size,sill_h):

    
    sill_height=float(sill_h)

    image_location3 = '/assets/' + df7[df7['sill_height']==sill_height][(df7['WindowSize']==window_size)]['image'].values[0]

    return image_location3



if __name__ == '__main__':
    app.server.run(debug=True,threaded=True)