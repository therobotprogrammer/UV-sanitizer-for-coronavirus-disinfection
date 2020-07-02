from transitions import Machine, State
import random
from transitions.extensions.states import add_state_features, Tags, Timeout
import time, datetime
from PushNotification import PushNotification

import pandas as pd
import datetime
from Plotter import Plotter
import os
import plotly.express as px
import plotly



global_mode = 'debug'
UV_PIN = 7

graph_save_dir = os.getcwd()












class Arduino():
    def __init__(self, mode): 
        self.mode = mode
        
        if self.mode == 'debug':
            print('WARNING: DEBUG MODE')
        else:
            from pyfirmata import Arduino, util
            self.board = Arduino('/dev/ttyACM0')


    def turn_uv_on(self):  
        if self.mode == 'debug':
            print('@Arduino: UV ON')
        else:        
            self.board.digital[UV_PIN].write(1)
    
    
    def turn_uv_off(self):  
        if self.mode == 'debug':
            print('@Arduino: UV OFF')
        else:        
            self.board.digital[UV_PIN].write(0)





class StateTimer():
    def __init__(self, state_name):
        self.name = state_name    
        self.last_start_time = 0
        self.last_end_time = 0        
        self.total_time_in_state = 0
        
        self.is_state_running = False
        
    def get_total_time_in_state(self):
        # assert(last_end_time >= last_start_time)
        if self.is_state_running:
            return self.total_time_in_state + time.time() - self.last_start_time
        else: 
            return self.total_time_in_state
    
    def start_state_timer(self):
        self.last_start_time = time.time()
        self.is_state_running = True

    def stop_state_timer(self):
        self.last_end_time = time.time()
        self.total_time_in_state += int(self.last_end_time  - self.last_start_time)
        self.is_state_running = False
                

class NarcolepticSuperhero(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...


    def __init__(self, name):
        self.arduino = Arduino('debug')

        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name
        self.uv_dose_to_administer_mins = 5*60
        self.uv_dose_to_administer = self.uv_dose_to_administer_mins * 60

        # What have we accomplished today?
        self.kittens_rescued = 0
        self.state_timers = None

        
        self.states =    [
                        {'name': 'WAITING_FOR_OBJECTS', 'on_enter': ['reset_and_create_state_timers'] },
                        {'name': 'SANITIZING', 'timeout': 10*60, 'on_timeout': 'high_temp', 'on_enter': ['start_uv_timer'], 'on_exit':['stop_uv_timer'] },
                        {'name': 'COOLING', 'timeout': 5*60, 'on_timeout': 'low_temp', 'on_enter': ['start_cooling_timer'], 'on_exit':['stopping_cooling_timer'] },
                        {'name': 'CYCLE_COMPLETE', 'on_enter': ['wrap_up']},
                    ] 


        self.transitions = [
            ['lid_close', 'WAITING_FOR_OBJECTS', 'SANITIZING'],
            ['high_temp', ['SANITIZING', 'COOLING'], 'COOLING'],
            ['low_temp', 'COOLING', 'SANITIZING'],
            ['dosage_cycle_complete', ['SANITIZING', 'COOLING'], 'CYCLE_COMPLETE']
        ]


        @add_state_features(Tags, Timeout)
        class CustomStateMachine(Machine):
            pass
        
        
        # Initialize the state machine
        self.machine = CustomStateMachine(model=self, states=self.states, transitions = self.transitions, initial='WAITING_FOR_OBJECTS')
        
        self.reset_and_create_state_timers()
        
        
    def reset_and_create_state_timers(self):
        if self.state_timers is not None:
            del self.state_timers
            
        self.state_timers = {}
        
        for state in self.states:
            name = state['name']
            timer_obj = StateTimer(name)
            self.state_timers[name] = timer_obj
        
        
            

    @property
    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")
        
    def stop_uv_timer(self):
        print('>>>stopped UV timer')
        state_name = self.state
        curr_state_timer = self.state_timers[state_name]        
        curr_state_timer.stop_state_timer()     
        
        self.arduino.turn_uv_off()
        
        print('>>>>>> Total time in state', curr_state_timer.get_total_time_in_state())
        

        
    def start_uv_timer(self):
        print('>>>starting UV timer')
        print(self.state) 
        
        state_name = self.state
        curr_state_timer = self.state_timers[state_name]        
        curr_state_timer.start_state_timer()
        
        self.arduino.turn_uv_on()
        
        
    def start_cooling_timer(self):
        state_name = self.state
        curr_state_timer = self.state_timers[state_name]        
        curr_state_timer.start_state_timer()
        print()

    def stopping_cooling_timer(self):
        # print('>>>stopping cooling timer') 
        state_name = self.state
        curr_state_timer = self.state_timers[state_name]        
        curr_state_timer.stop_state_timer()   
        print()

        

        
            

        
    def get_uv_dose_administered_till_now(self):
        dose_administered_till_now = uv_box.state_timers['SANITIZING'].get_total_time_in_state()

        if dose_administered_till_now >= (self.uv_dose_to_administer):
            is_administered = True
        else:
            is_administered = False

        time_administered_str = str(datetime.timedelta(seconds=int(dose_administered_till_now)))

        self.dose_monitor = {
                            'is_administered': is_administered, 
                            'time_administered': int(dose_administered_till_now), 
                            'time_remaining': int(self.uv_dose_to_administer - dose_administered_till_now),
                            'time_administered_str': time_administered_str,  
                            'percentage_complete':  int( (dose_administered_till_now / self.uv_dose_to_administer) * 100 )                           
                        }
        
        if self.dose_monitor['is_administered']:
            assert self.dose_monitor['percentage_complete'] >= 100
            
            
        return self.dose_monitor
    
    def wrap_up(self):
        self.send_push_notification()
        self.make_graphs()
        
    
    def send_push_notification(self):
        postman = PushNotification()
        postman.send_notification('Cycle Complete')

    def make_graphs(self):   
        row_list = []

        for state_name in ['SANITIZING', 'COOLING']:
            # state_name = state['name']
            state_timer = self.state_timers[state_name]
            row_dict = {'state' : state_name, 'total_time_in_state': state_timer.total_time_in_state }
            row_list.append(row_dict)
            
        df = pd.DataFrame(row_list)        
        # df = df.drop(columns = ['WAITING_FOR_OBJECTS'])

        fig = px.pie(df, values='total_time_in_state', names='state', title='Time spend in states')
        plotly.offline.plot(fig, show_link = True)
        
        print('done making graphs')

            
    # def dosage_cycle_complete(self):
    #     print('Cycle Completed')
        

       


uv_box = NarcolepticSuperhero("Cardboard Box")
uv_box.lid_close()
last_dose = uv_box.get_uv_dose_administered_till_now() 

log_dose_administered_list = []




while True:     
    dose = uv_box.get_uv_dose_administered_till_now() 
    
    if dose['time_administered']!= last_dose['time_administered']:
        print(dose['is_administered'], '  time_administered: ', dose['time_administered_str'], '   percentage_complete:', dose['percentage_complete'])
        
        dose_log_row = {
                            'timestamp': datetime.datetime.now().isoformat(), 
                            'dose_administered_amount': dose['time_administered'],
                            'percentage_complete': dose['percentage_complete'],
                            'state': uv_box.state
                        }
        log_dose_administered_list.append(dose_log_row)
        
        last_dose = dose

    # print(dose['is_administered'], '  time administered: ', dose['time_administered'], '   percentage_complete:', dose['percentage_complete'] )


    if dose['is_administered']:
        uv_box.dosage_cycle_complete()
        print('>>>>>>>>>> ', uv_box.state)
        break
    
    time.sleep(.1)


uv_dose_log_dataframe = pd.DataFrame(log_dose_administered_list) 






plotter_maker = Plotter(graph_save_dir)
plotter_maker.time_plot(uv_dose_log_dataframe, 'timestamp', 'dose_administered_amount')    
  













# import pandas as pd
# import os
# import plotly.express as px
# import plotly


# df = uv_dose_log_dataframe

# fig = px.line(df, 'timestamp', 'dose_administered_amount')
# fig.update_xaxes(rangeslider_visible=True)

# plotly.offline.plot(fig, show_link = True)
  

# uv_box.state
# uv_box.high_temp()
# uv_box.state
# uv_box.low_temp()
# uv_box.state
# uv_box.dosage_cycle_complete()
# uv_box.state










