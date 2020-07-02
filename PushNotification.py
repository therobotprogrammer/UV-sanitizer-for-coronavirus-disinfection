# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:30:38 2020

@author: prana
"""




import requests
import datetime
import pytz



class PushNotification():  
    # Push Notifications
   
    def __init__(self):    
        user_key = ""
        token =""
        self.setup_pushover_credintials(user_key,token)
        
        self.local_timezone =  'Asia/Kolkata'
    
    
    def setup_pushover_credintials(self,user_key, token):
        self.pushover_user_key = user_key
        self.pushover_token = token
    
    def send_notification(self,msg_string, send_time = True):
        
        ''' 
            Credit for function: binga Phani Srikanth
            http://forums.fast.ai/t/training-metrics-as-notifications-on-mobile-using-callbacks/17330
        
            This function sends message to my mobile using Pushover.
        '''          
        
        url = "https://api.pushover.net/1/messages.json"
        data = {
            'user'  : self.pushover_user_key,
            'token' : self.pushover_token,
            'sound' : "gamelan"
        }
        
        
        if send_time:
            msg_string = msg_string + '  ' + self.get_time_string()
            
        data['message'] = msg_string
        #data['message'] = data['message'] + "\n" + str(datetime.now())

        r = requests.post(url = url, data = data)
        
        
        
    def get_time_string(self):
        
        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone(pytz.timezone(self.local_timezone))  
                
        # year = str(local_time.year)  
        # month = str(local_time.month) 
        # day = str(local_time.day) 
        hour = str(local_time.hour)
        minute = str(local_time.minute)
        
        # time_string = year + '-' + month + '-' + day + '-' + hour + '-' + minute
        time_string = '  @' + hour + ':' + minute + 'hrs'


        return time_string
    
    


if __name__ == "__main__": 
    
    postman = PushNotification()
    postman.send_notification('Hello from python  ')
    
    
    













    
    
    