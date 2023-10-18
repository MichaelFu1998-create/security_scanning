def objectlist_flat(self, lt, replace):
        '''
            Similar to the dict constructor, but handles dups
            
            HCL is unclear on what one should do when duplicate keys are
            encountered. These comments aren't clear either:
            
            from decoder.go: if we're at the root or we're directly within
                             a list, decode into dicts, otherwise lists
                
            from object.go: there's a flattened list structure
        '''
        d = {}

        for k, v in lt:
            if k in d.keys() and not replace:
                if type(d[k]) is list:
                    d[k].append(v)
                else:
                    d[k] = [d[k], v]
            else:
                if isinstance(v, dict):
                    dd = d.setdefault(k, {})
                    for kk, vv in iteritems(v):
                        if type(dd) == list:
                            dd.append({kk: vv})
                        elif kk in dd.keys():
                            if hasattr(vv, 'items'):
                                for k2, v2 in iteritems(vv):
                                    dd[kk][k2] = v2
                            else:
                                d[k] = [dd, {kk: vv}]
                        else:
                            dd[kk] = vv
                else:
                    d[k] = v

        return d