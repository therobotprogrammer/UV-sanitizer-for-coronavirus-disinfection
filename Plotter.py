#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:38:25 2019

@author: pt
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cufflinks as cf
import plotly.io as pio
import plotly.express as px
import plotly
import plotly.graph_objects as go
import numpy as np

cf.go_offline()
pio.renderers
pio.renderers.default = "browser"


class Plotter:    
    def __init__(self, top_save_directory, print_plot_id = True):   
        if not os.path.isdir(top_save_directory):
            os.makedirs(top_save_directory)            
        self.top_save_directory = top_save_directory  
        self.current_directory  = top_save_directory        
        self.print_plot_id = print_plot_id
        self.current_plot_id = 0
        
        self.color_list =             ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure,\
            beige', 'bisque', 'black', 'blanchedalmond', 'blue,\
            blueviolet', 'brown', 'burlywood', 'cadetblue,\
            chartreuse', 'chocolate', 'coral', 'cornflowerblue,\
            cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan,\
            darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen,\
            darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange,\
            darkorchid', 'darkred', 'darksalmon', 'darkseagreen,\
            darkslateblue', 'darkslategray', 'darkslategrey,\
            darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue,\
            dimgray', 'dimgrey', 'dodgerblue', 'firebrick,\
            floralwhite', 'forestgreen', 'fuchsia', 'gainsboro,\
            ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green,\
            greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo,\
            ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen,\
            lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan,\
            lightgoldenrodyellow', 'lightgray', 'lightgrey,\
            lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen,\
            lightskyblue', 'lightslategray', 'lightslategrey,\
            lightsteelblue', 'lightyellow', 'lime', 'limegreen,\
            linen', 'magenta', 'maroon', 'mediumaquamarine,\
            mediumblue', 'mediumorchid', 'mediumpurple,\
            mediumseagreen', 'mediumslateblue', 'mediumspringgreen,\
            mediumturquoise', 'mediumvioletred', 'midnightblue,\
            mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy,\
            oldlace', 'olive', 'olivedrab', 'orange', 'orangered,\
            orchid', 'palegoldenrod', 'palegreen', 'paleturquoise,\
            palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink,\
            plum', 'powderblue', 'purple', 'red', 'rosybrown,\
            royalblue', 'rebeccapurple', 'saddlebrown', 'salmon,\
            sandybrown', 'seagreen', 'seashell', 'sienna', 'silver,\
            skyblue', 'slateblue', 'slategray', 'slategrey', 'snow,\
            springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',\
            'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',\
            'yellow', 'yellowgreen']
        
        self.color_scales = ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
             'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
             'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
             'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
             'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
             'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
             'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd']
        
        
    def set_current_dir(self, local_folder_name): 
        if local_folder_name == '':
            current_directory = self.top_save_directory            
        elif os.path.isdir(local_folder_name):
            current_directory = self.local_folder_name           
        else:
            current_directory = os.path.join(self.top_save_directory , local_folder_name)            
        if not os.path.isdir(current_directory):
            os.makedirs(current_directory)  
        print(current_directory)
        print()
        self.current_directory = current_directory
        
        
    def save_and_show(self, plt, file_name, dpi = 1200): 
        plt.savefig(file_name, dpi)
        plt.show()
        
        
    def plot_cat_cat(self, x,y):            
        message = 'Plotter_cat_cat' + x.name + 'vs_target_'+ y.name
        print(message)        
        plt.figure()
        ax = sns.catplot(x= x, hue = y, kind = 'count', height=6)    
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")
        plt.tight_layout()
        file_name = os.path.join(self.current_directory + '/' + message + '.jpg')
        plt.savefig(file_name, dpi = 1200)
        plt.show()
    
        
    def plot_cat_cont(self, x,y, kde = True):
        message = 'Plotter_cat_cont_' + x.name + 'vs_target_'+ y.name
        print(message)
        plt.figure()
        temp_df = pd.DataFrame()        
        temp_df[x.name] = x
        temp_df[y.name] = y
        sns.FacetGrid(temp_df, hue = y.name, height=6).map(sns.kdeplot, y.name , vertical = False).add_legend()   
        plt.tight_layout()
        file_name = os.path.join(self.current_directory + '/' + message + '.jpg')
        plt.savefig(file_name, dpi = 1200)
        plt.show()
        
    
    def plot_cont_cont(self, x,y):
        message = 'Plotter_cat_cont' + x.name + 'vs_target_'+ y.name
        print(message)
        plt.figure()
        ax = sns.scatterplot(x = x, y = y, hue = y)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")
        plt.tight_layout()
        file_name = os.path.join(self.current_directory + '/' + message + '.jpg')
        plt.savefig(file_name, dpi = 1200)
        plt.show()


    def plot_cont_cat(self, x,y):
        message = 'Plotter_cat_cont' + x.name + 'vs_target_'+ y.name
        print(message)
        plt.figure()      
        #To Do: resolve this workaround or use plotly. Facetgrid.map doesnt work without this
        temp_df = pd.DataFrame()
        temp_df[x.name] = x
        temp_df[y.name] = y
        sns.FacetGrid(temp_df, hue = x.name, height=6).map(sns.kdeplot, y.name , vertical = False).add_legend()   
        plt.tight_layout() 
        file_name = os.path.join(self.current_directory + '/' + message + '.jpg')
        plt.savefig(file_name, dpi = 1200)
        plt.show()
        
        
    def box_plot_df(self, df_local, message = ''):
        filename = os.path.join(self.current_directory, message + '_box_plot.html')   
        fig = df_local.iplot(kind='box', boxpoints='outliers', title = message + ' - Box Plot', asFigure = True, asUrl = True)
        plotly.offline.plot(fig, show_link = True, filename = filename)  


    def box_plot_plotly_express(self, df_local, message = ''):
        fig = px.box(df_local)        
        filename = os.path.join(self.current_directory, message + '_box_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)
        

    def time_plot(self, df, x_name, y_name, message = ''):        
        fig = px.line(df, x_name, y_name, title = message)
        fig.update_xaxes(rangeslider_visible=True)

        filename = os.path.join(self.current_directory, message + '_timed_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)

        
    def violin(self, df_local, message = ''):       
        fig = go.Figure()
        for column in df_local.columns:
            temp = pd.DataFrame()
            temp[column] = df_local[column]
            temp['x'] = column            
            fig.add_trace(go.Violin(x=temp['x'],
                                    y=temp[column],
                                    name=column,
                                    box_visible=True,
                                    meanline_visible=True))            
        filename = os.path.join(self.current_directory, message + '_violin.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)    
        

    def box_plot_with_mean(self, df_local = None, message = '', x_label = '', y_label = ''):       
        fig = go.Figure(  )
        for idx, column in enumerate(df_local.columns):
            temp = pd.DataFrame()
            temp[column] = df_local[column]
            temp['x'] = column          
            fig.add_trace(go.Box(x=temp['x'],
                                    y=temp[column],
                                    name=column,
                                    boxpoints = 'outliers',
                                    boxmean = True,                           
                                    ) )
        fig.update_layout(
                            title=go.layout.Title(
                                text=message,
                                xref="paper",
                                font=dict(
                                        family="Courier New, monospace",
                                        size=24,
                                        color="#7f7f7f"
                                    ),
                                xanchor = 'auto'
                            ),
                            xaxis=go.layout.XAxis(
                                title=go.layout.xaxis.Title(
                                    text=x_label,
                                    font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="#7f7f7f"
                                    )
                                )
                            ),
                            yaxis=go.layout.YAxis(
                                title=go.layout.yaxis.Title(
                                    text=y_label,
                                    font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="#7f7f7f"
                                    )
                                )
                            )
                        )    
        filename = os.path.join(self.current_directory, message + '_box_with_mean.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)   

    
    def parallel_coordinates(self, input_df, target, message, labels_dict = None):
        combined_local_df = input_df.join( target, how = 'outer')      
        if isinstance(target, pd.DataFrame):    
            target_name = target.columns[0]
        else:
            #target is a series
            target_name = target.name
        fig = px.parallel_coordinates(combined_local_df, color=target_name, labels=labels_dict,
                                     color_continuous_scale=px.colors.diverging.Tealrose,
                                     color_continuous_midpoint=2 )
        filename = os.path.join(self.current_directory, message + '_parallel_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)


    def parallel_coordinates_wrapper(self, parameters, scores, score_name_to_plot, message = '', labels_dict = None):        
        parameters_local = parameters.copy()
        scores_local = scores[score_name_to_plot].copy()        
        temp_df = parameters_local.join(scores_local, how = 'outer')    
        temp_df = temp_df.sort_values('mean_test_score', ascending = False)  
        combined_local_df = temp_df      
        fig = px.parallel_coordinates(combined_local_df, color=score_name_to_plot, labels=labels_dict,
                                     color_continuous_scale=px.colors.diverging.Tealrose,
                                     color_continuous_midpoint=2 )
        filename = os.path.join(self.current_directory, message + '_parallel_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)
        

    def parallel_categories(self, parameters, scores, score_name_to_plot = 'mean_test_score', message = ''): 
        parameters_local = parameters.copy()
        scores_local = scores[score_name_to_plot].copy()        
        temp_df = parameters_local.join(scores_local, how = 'outer')    
        temp_df = temp_df.sort_values('mean_test_score', ascending = False)       
        fig = px.parallel_categories(temp_df, color = 'mean_test_score', color_continuous_scale=px.colors.sequential.Inferno)
        filename = os.path.join(self.current_directory, message + '_parallel_categories_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)        


    def line_plot(self, df, x, y, color = '', message = '' ):        
        df = df.sort_values(by = x)
        if color == '':
            fig = px.line(df, x=x, y=y, title = message)    
        else:
            fig = px.line(df, x=x, y=y, color=color, title = message)               
        fig.update_xaxes(title = x.split('__')[-1])
        filename = os.path.join(self.current_directory, message + '_line_plot.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)    
            
            
    def plot3d(self, x,y,z, color='rgb(204, 204, 204)', message = 'Title', x_label = '', y_label = ''):
        if type(color) == pd.DataFrame:
            color = color[0].values
        trace = go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode='markers',
            marker=dict(
                size=12,
                        # set color to an array/list of desired values
                color=color,
                colorscale='Viridis',   # choose a colorscale
                opacity=0.8
            )
        )        
        traces = [trace]
        layout = go.Layout(         
            title=dict(
                        text = message,
                        
                        font=dict(
                                    family='Courier New, monospace',
                                    size=36,
                                    color='#7f7f7f'
                                )
                        ), 
            xaxis=dict(
                        title = x_label,
                        
                        titlefont=dict(
                                        family='Courier New, monospace',
                                        size=18,
                                        color='#7f7f7f'
                                    )
                        ),
            yaxis=dict(
                        title= y_label,
                        titlefont=dict(
                                        family='Courier New, monospace',
                                        size=18,
                                        color='#7f7f7f'
                                    )
                        )
        )
        fig = go.Figure(data=traces, layout=layout)   
        filename = os.path.join(self.current_directory, message +  '.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)    
        return traces


    def plot2d(self, x,y, threshold = '', color = 'rgb(255, 215, 0)', message = 'Title', x_label = '', y_label = ''):
        if threshold != '':
            threshold = threshold + 1        
            if threshold > len(x):
                threshold  = len(x)
            color = list(np.full(threshold, 1)) + list(np.full(y.shape[0] - threshold, 0))
        trace1 = go.Scatter(
            x = x,    
            y = y,
            mode='markers',
            marker=dict(
                size=16,
                color = color, #set color equal to a variable
                colorscale='Viridis',
                showscale=True
            )
        )
        traces = [trace1]     
        layout = go.Layout(         
            title=dict(
                        text = message,
                        
                        font=dict(
                                    family='Courier New, monospace',
                                    size=48,
                                    color='#7f7f7f'
                                )
                        ),                    
            xaxis=dict(
                        title = x_label,
                        
                        titlefont=dict(
                                        family='Courier New, monospace',
                                        size=18,
                                        color='#7f7f7f'
                                    )
                        ),                    
            yaxis=dict(
                        title= y_label,
                        titlefont=dict(
                                        family='Courier New, monospace',
                                        size=18,
                                        color='#7f7f7f'
                                    )
                        ),                               
        )
        fig = go.Figure(data=traces, layout=layout)
        filename = os.path.join(self.current_directory, message +  '.html')   
        plotly.offline.plot(fig, show_link = True, filename = filename)    
        return traces
    
    
    def plot_series(self, y, threshold = '', message = ''):
        x_labels = list(range(0, y.shape[0]))
        self.plot2d(x_labels, y , threshold = threshold, message = message)
    
    
    def plot_dataframe(self, df_local, message = ''): 
        df_local_continuous_only = df_local.select_dtypes(exclude = 'category')      
        ax = df_local.plot.kde()
        ax.set_title(message)
        ax.legend(ncol = 7, prop={'size': 9})
        df_local_continuous_only.iplot(kind='box', boxpoints='outliers', title = message + 'Box Plot - Continuous Data')



if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/pt/Documents/auto_eda')   
    import plotly.express as px
    import plotly

    iris = px.data.iris()    
    target = iris['species_id']
    iris_df = iris.drop(['species', 'species_id'], axis = 1)   
    
    plot_dir = '/media/pt/hdd/Auto EDA Results/unit_tests/plots'
    plotter = Plotter(plot_dir)    
    plotter.parallel_coordinates(iris_df, target, message = 'iris')

    # database = SaveAndLoad('/media/pt/hdd/Auto EDA Results/regression/results/pickles')   
    # target = database.load('y_train')  
    # combined_continuous_df = database.load('combined_continuous_df')

    # plotter = Plotter(plot_dir)    
    # plotter.parallel_coordinates(combined_continuous_df, target, message = 'House Price - continuous data')

