# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#  
#  __computeAngles method is based on a function developed 
#  by Prasanth Nair (https://github.com/phn/angles)
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  



import numpy as np
from math import floor, ceil



class NumpyNormalizeAngles(object):

    def __init__(self, usenumpy=True):
        """
        If usenumpy=True Numpy is used (default)
        
        """
        
        self.__usenumpy = usenumpy
    
    
    def getValues(self, angles, lower=0, upper=360):
        """
        Normalize angles
        
        """
        
        if self.__usenumpy:
            
            if not isinstance(angles, np.ndarray):
                print "---Error: angles is not a numpy array\n\tTry with usenumpy=False"
                return
            
            vect_norm = np.vectorize(self.__computeAngles)
            norm_angles = vect_norm(angles, lower, upper)
        
        else:
            if isinstance(angles, np.ndarray):
                print "---Error: angles is a numpy array\n\tTry with usenumpy=True (default option)"
                return
            
            norm_angles = self.__computeAngles(angles, lower, upper)
        
        return norm_angles
        
    
    def __computeAngles(self, num, lower, upper, b=False):
        """
        Normalize angle to range (lower, upper).
        
        This method is based on a function developed by Prasanth Nair
        https://github.com/phn/angles
        
        """
        
        # abs(num + upper) and abs(num - lower) are needed, instead of
        # abs(num), since the lower and upper limits need not be 0. We need
        # to add half size of the range, so that the final result is lower +
        # <value> or upper - <value>, respectively.
        res = num
        if not b:
            if lower >= upper:
                raise ValueError("Invalid lower and upper limits: (%s, %s)" %
                                 (lower, upper))
    
            res = num
            
            if num > upper or num == lower:
                num = lower + abs(num + upper) % (abs(lower) + abs(upper))
                
            if num < lower or num == upper:
                num = upper - abs(num - lower) % (abs(lower) + abs(upper))
    
            res = lower if num == upper else num
        else:
            total_length = abs(lower) + abs(upper)
            
            if num < -total_length:
                num += ceil(num / (-2 * total_length)) * 2 * total_length
                
            if num > total_length:
                num -= floor(num / (2 * total_length)) * 2 * total_length
                
            if num > upper:
                num = total_length - num
                
            if num < lower:
                num = -total_length - num
    
            res = num
    
        res *= 1.0  # Make all numbers float, to be consistent
    
        return res

