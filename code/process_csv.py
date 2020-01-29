import numpy as np
import cv2 
import json
import copy
import random
from collections import Counter
import pickle
import csv
import os
import argparse
import pandas as pd

df = pd.read_csv('features.csv')
# print(df.head())
# print(df.info())
# print(df.describe())

print(df.columns)

df = df.set_index(['inv_numb', 'node'])
print(df)