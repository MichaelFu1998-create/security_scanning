def to_pysat(self, flatten_twod=True, units_label='UNITS', name_label='long_name',
                        fill_label='FILLVAL', plot_label='FieldNam', 
                        min_label='ValidMin', max_label='ValidMax', 
                        notes_label='Var_Notes', desc_label='CatDesc',
                        axis_label = 'LablAxis'):
        """
        Exports loaded CDF data into data, meta for pysat module
        
        Notes
        -----
        The *_labels should be set to the values in the file, if present.
        Note that once the meta object returned from this function is attached
        to a pysat.Instrument object then the *_labels on the Instrument
        are assigned to the newly attached Meta object.
        
        The pysat Meta object will use data with labels that match the patterns
        in *_labels even if the case does not match.

        Parameters
        ----------
        flatten_twod : bool (True)
            If True, then two dimensional data is flattened across 
            columns. Name mangling is used to group data, first column
            is 'name', last column is 'name_end'. In between numbers are 
            appended 'name_1', 'name_2', etc. All data for a given 2D array
            may be accessed via, data.ix[:,'item':'item_end']
            If False, then 2D data is stored as a series of DataFrames, 
            indexed by Epoch. data.ix[0, 'item']
        units_label : str
            Identifier within metadata for units. Defults to CDAWab standard.
        name_label : str
            Identifier within metadata for variable name. Defults to 'long_name',
            not normally present within CDAWeb files. If not, will use values
            from the variable name in the file.
        fill_label : str
            Identifier within metadata for Fill Values. Defults to CDAWab standard.
        plot_label : str
            Identifier within metadata for variable name used when plotting.
            Defults to CDAWab standard.
        min_label : str
            Identifier within metadata for minimim variable value. 
            Defults to CDAWab standard.
        max_label : str
            Identifier within metadata for maximum variable value.
            Defults to CDAWab standard.
        notes_label : str
            Identifier within metadata for notes. Defults to CDAWab standard.
        desc_label : str
            Identifier within metadata for a variable description.
            Defults to CDAWab standard.
        axis_label : str
            Identifier within metadata for axis name used when plotting. 
            Defults to CDAWab standard.
            
                             
        Returns
        -------
        pandas.DataFrame, pysat.Meta
            Data and Metadata suitable for attachment to a pysat.Instrument
            object.
        
        """

        import string
        import pysat
        import pandas

        # copy data
        cdata = self.data.copy()
        #
        # create pysat.Meta object using data above
        # and utilizing the attribute labels provided by the user
        meta = pysat.Meta(pysat.DataFrame.from_dict(self.meta, orient='index'),
                          units_label=units_label, name_label=name_label,
                          fill_label=fill_label, plot_label=plot_label,
                          min_label=min_label, max_label=max_label,
                          notes_label=notes_label, desc_label=desc_label,
                          axis_label=axis_label)
                          
        # account for different possible cases for Epoch, epoch, EPOCH, epOch
        lower_names = [name.lower() for name in meta.keys()] 
        for name, true_name in zip(lower_names, meta.keys()):
            if name == 'epoch':
                meta.data.rename(index={true_name: 'Epoch'}, inplace=True)
                epoch = cdata.pop(true_name)
                cdata['Epoch'] = epoch

        # ready to format data, iterate over all of the data names
        # and put into a pandas DataFrame
        two_d_data = []
        drop_list = []
        for name in cdata.keys():
            temp = np.shape(cdata[name])
            # treat 2 dimensional data differently
            if len(temp) == 2:
                if not flatten_twod:
                    # put 2D data into a Frame at each time
                    # remove data from dict when adding to the DataFrame
                    frame = pysat.DataFrame(cdata[name].flatten(), columns=[name])
                    drop_list.append(name)

                    step = temp[0]
                    new_list = []
                    new_index = np.arange(step)
                    for i in np.arange(len(epoch)):
                        new_list.append(frame.iloc[i*step:(i+1)*step, :])
                        new_list[-1].index = new_index
                    #new_frame = pandas.DataFrame.from_records(new_list, index=epoch, columns=[name])
                    new_frame = pandas.Series(new_list, index=epoch, name=name)
                    two_d_data.append(new_frame)

                else:
                    # flatten 2D into series of 1D columns
                    new_names = [name + '_{i}'.format(i=i) for i in np.arange(temp[0] - 2)]
                    new_names.append(name + '_end')
                    new_names.insert(0, name)
                    # remove data from dict when adding to the DataFrame
                    drop_list.append(name)
                    frame = pysat.DataFrame(cdata[name].T,
                                            index=epoch,
                                            columns=new_names)
                    two_d_data.append(frame)
        for name in drop_list:
            _ = cdata.pop(name)
        # all of the data left over is 1D, add as Series
        data = pysat.DataFrame(cdata, index=epoch)
        two_d_data.append(data)
        data = pandas.concat(two_d_data, axis=1)
        data.drop('Epoch', axis=1, inplace=True)
        return data, meta