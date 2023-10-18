def is_instance(self):
        """return True if callback is an instance of a class"""
        ret = False
        val = self.callback
        if self.is_class(): return False

        ret = not inspect.isfunction(val) and not inspect.ismethod(val)
#         if is_py2:
#             ret = isinstance(val, types.InstanceType) or hasattr(val, '__dict__') \
#                 and not (hasattr(val, 'func_name') or hasattr(val, 'im_func'))
# 
#         else:
#             ret = not inspect.isfunction(val) and not inspect.ismethod(val)

        return ret