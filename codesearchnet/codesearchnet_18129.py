def link_zscale(st):
    """Links the state ``st`` psf zscale with the global zscale"""
    # FIXME should be made more generic to other parameters and categories
    psf = st.get('psf')
    psf.param_dict['zscale'] = psf.param_dict['psf-zscale']
    psf.params[psf.params.index('psf-zscale')] = 'zscale'
    psf.global_zscale = True
    psf.param_dict.pop('psf-zscale')
    st.trigger_parameter_change()
    st.reset()