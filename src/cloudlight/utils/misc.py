'''
Created on Mar 29, 2010

@author: jose
'''

identity = lambda x : map(None, [x])[0]


class Base:

    alphab = [chr(i) for i in range(33,35)+range(36,125)]
    inv_alphab = dict( zip( alphab, range(len(alphab))) )
    
    def num2base(self, num):
    
        r = ''
        base = len(self.alphab)
    
        if num == 0:
            return self.alphab[0]
    
        while num != 0:
            
            char_num = num % base        
            num /= base
    
            r = self.alphab[char_num] + r
    
        return r
    
    
    def base2num(self, s):
        
        r = 0
        base = len(self.alphab)
    
        if s == self.alphab[0]:
            return r
    
        count = 0
        while len(s) > 0:
            
            r += base**count * self.inv_alphab[s[-1]]

            s = s[:-1]
            
            count += 1
    
        return r
