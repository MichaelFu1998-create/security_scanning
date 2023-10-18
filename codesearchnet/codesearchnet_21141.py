def nav_to_vcf_dir(ftp, build):
    """
    Navigate an open ftplib.FTP to appropriate directory for ClinVar VCF files.

    Args:
        ftp:   (type: ftplib.FTP) an open connection to ftp.ncbi.nlm.nih.gov
        build: (type: string) genome build, either 'b37' or 'b38'
    """
    if build == 'b37':
        ftp.cwd(DIR_CLINVAR_VCF_B37)
    elif build == 'b38':
        ftp.cwd(DIR_CLINVAR_VCF_B38)
    else:
        raise IOError("Genome build not recognized.")