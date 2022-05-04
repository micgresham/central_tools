#!/usr/bin/env python3

import json
import re


def sqlboolean(bool_val):

   elif (bool_val.upper() == '0'):
     return(0)
   elif (bool_val.upper() == '1'):
     return(1)
   elif (bool_val.upper() == 'TRUE'):
     return(1)
   elif (bool_val.upper() == 'FALSE'):
     return(0)

print(sqlboolean('false'))
print(sqlboolean('False'))
print(sqlboolean('0'))
print(sqlboolean('true'))
print(sqlboolean('True'))
print(sqlboolean('1'))
print(sqlboolean(True))
