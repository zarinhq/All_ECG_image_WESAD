import pickle
import numpy as np
import os
import datetime
import tensorflow as tf
from pathlib import Path
class DataManager:
    # Path to the WESAD dataset
    ROOT_PATH = './WESAD/'
    #ROOT_PATH = r'C:\WESAD'
    
    # pickle file extension for importing
    FILE_EXT = '.pkl'

    # IDs of the subjects
    SUBJECTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]

    # Label values defined in the WESAD readme
#     BASELINE = 1
#     STRESS = 2

    RAW_SENSOR_VALUES = ['ECG']

    # Dictionaries to store the two sets of data
#     BASELINE_DATA = []
#     STRESS_DATA = []

    def __init__(self, ignore_empatica=True, ignore_additional_signals=True):
        # denotes that we will be excluding the empatica data 
        # after loading those measurements
        self.ignore_empatica = ignore_empatica

    def get_subject_path(self, subject):
        """ 
        Parameters:
        subject (int): id of the subject
        
        Returns:
        str: path to the pickle file for the given subject number
             iff the path exists 
        """
        
        # subjects path looks like data_set + '<subject>/<subject>.pkl'
        path = os.path.join(DataManager.ROOT_PATH, 'S'+ str(subject), 'S' + str(subject) + DataManager.FILE_EXT)
        print('Loading data for S'+ str(subject))
        #print('Path=' + path)
        if os.path.isfile(path):
            return path
        else:
            print(path)
            raise Exception('Invalid subject: ' + str(subject))

    def load(self, subject):
        """ 
        Loads and saves the data from the pkl file for the provided subject
        
        Parameters:
        subject (int): id of the subject
        
        Returns: Baseline and stress data
        dict: {{'EDA': [###, ..], ..}, 
               {'EDA': [###, ..], ..} }
        """
       
        # change the encoding because the data appears to have been
        # pickled with py2 and we are in py3
        with open(self.get_subject_path(subject), 'rb') as file:
            data = pickle.load(file, encoding='latin1')
            return self.extract_and_reform(data, subject)

    def extract_and_reform(self, data, subject):
        """ 
        Extracts and shapes the data from the pkl file
        for the provided subject.
        
        Parameters:
        data (dict): as loaded from the pickle file
        
        Returns: Baseline and stress data
        dict: {{'EDA': [###, ..], ..}, 
               {'EDA': [###, ..], ..} }
        """
                
        if self.ignore_empatica:
            del data['signal']['wrist']
            
        all_data_types = dict()
        
        for value in DataManager.RAW_SENSOR_VALUES: 
            all_data_types[value] = data['signal']['chest'][value]
            
        
        return all_data_types