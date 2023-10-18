def smart_range(*args):
    '''
    smart_range(1,3,9)==[1,3,5,7,9]
    '''
    if len(args)==1:#String
        string_input = True
        string = args[0].replace(' ','')
        original_args=string.split(',')
        args = []
        for arg in original_args:
            try:
                args.append(ast.literal_eval(arg))
            except (ValueError,SyntaxError):
                try:# Maybe an arithmetic expression?
                    args.append(eval(arg,{'__builtins__':{}}))
                except (NameError,SyntaxError):#Input was actually meant to be a string, e.g. smart_range('a,...,z'), or input was interval type, e.g. smart_range('[1,3]/10')
                    args.append(arg)
    else:
        string_input = False
    arg_start = args[0]
    if len(args)>2:
        arg_step = args[1]
        if len(args)>3:
            raise ValueError('At most 3 arguments: start, step, stop')
    else:
        arg_step = None
    arg_end = args[-1]
    if String.valid(arg_start) and len(arg_start)==1:#Character
        range_type = 'char'
    elif all(Integer.valid(arg) for arg in args):
        range_type = 'integer'
    else: 
        if string_input and original_args[0][0] in ['(','[']:
            range_type = 'linspace'
        else:
            range_type = 'float'

    if range_type == 'char':
        start = ord(arg_start)
        step = (ord(arg_step)- start) if arg_step else 1
        end = ord(arg_end)
        out = [chr(i) for i in range(start,end+step,step)]
        if np.sign(step)*(ord(out[-1])-end)>0:
            del out[-1]
        return out
    elif range_type == 'integer':
        if string_input:
            if len(args)==2 and all('**' in oa for oa in original_args):#Attempt geometric progresesion
                bases,exponents = zip(*[oa.split('**') for oa in original_args])
                if len(set(bases))==1:#Keep attempting geometric progression
                    return [int(bases[0])**exponent for exponent in smart_range(','.join(exponents))]
        start = arg_start
        step = (arg_step - arg_start) if arg_step is not None else 1
        end = arg_end
        out = list(range(start,end+step,step))
        if np.sign(step)*(out[-1]-end)>0:
            del out[-1]
        return out
    elif range_type == 'float':
        if len(args)==2 and all('**' in oa for oa in original_args):#Attempt geometric progresesion
            bases,exponents = zip(*[oa.split('**') for oa in original_args])
            if len(set(bases))==1:#Keep attempting geometric progression
                return [float(bases[0])**exponent for exponent in smart_range(','.join(exponents)) ]
        if len(args) == 2:
            raise ValueError()
        start = arg_start
        step = arg_step - arg_start
        end = arg_end
        out = list(np.arange(start,end+1e-12*step,step))
        return out
    elif range_type == 'linspace':
        lopen,start = (original_args[0][0]=='('),float(original_args[0][1:])
        end,N = original_args[1].split('/')
        end,ropen = float(end[:-1]),(end[-1]==')')
        N = ast.literal_eval(N)+lopen +ropen
        points = np.linspace(start,end,num=N)
        return points[lopen:len(points)-ropen]