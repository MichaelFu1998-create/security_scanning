def PyJsStrictEq(a, b):
    '''a===b'''
    tx, ty = Type(a), Type(b)
    if tx != ty:
        return false
    if tx == 'Undefined' or tx == 'Null':
        return true
    if a.is_primitive():  #string bool and number case
        return Js(a.value == b.value)
    if a.Class == b.Class == 'PyObjectWrapper':
        return Js(a.obj == b.obj)
    return Js(a is b)