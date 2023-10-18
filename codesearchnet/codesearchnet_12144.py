def _epd_function(coeffs, fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd):
    '''
    This is the EPD function to fit using a smoothed mag-series.

    '''

    return (coeffs[0]*fsv*fsv +
            coeffs[1]*fsv +
            coeffs[2]*fdv*fdv +
            coeffs[3]*fdv +
            coeffs[4]*fkv*fkv +
            coeffs[5]*fkv +
            coeffs[6] +
            coeffs[7]*fsv*fdv +
            coeffs[8]*fsv*fkv +
            coeffs[9]*fdv*fkv +
            coeffs[10]*np.sin(2*pi_value*xcc) +
            coeffs[11]*np.cos(2*pi_value*xcc) +
            coeffs[12]*np.sin(2*pi_value*ycc) +
            coeffs[13]*np.cos(2*pi_value*ycc) +
            coeffs[14]*np.sin(4*pi_value*xcc) +
            coeffs[15]*np.cos(4*pi_value*xcc) +
            coeffs[16]*np.sin(4*pi_value*ycc) +
            coeffs[17]*np.cos(4*pi_value*ycc) +
            coeffs[18]*bgv +
            coeffs[19]*bge +
            coeffs[20]*iha +
            coeffs[21]*izd)