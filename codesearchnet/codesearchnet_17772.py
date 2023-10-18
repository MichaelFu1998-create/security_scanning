def log_calls(function):
    '''
    Decorator that logs function calls in their self.log
    '''
    def wrapper(self,*args,**kwargs):  
        self.log.log(group=function.__name__,message='Enter') 
        function(self,*args,**kwargs)
        self.log.log(group=function.__name__,message='Exit') 
    return wrapper