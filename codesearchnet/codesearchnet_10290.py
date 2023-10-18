def _define_canned_commands():
    """Define functions for the top level name space.

    Definitions are collected here so that they can all be wrapped in
    a try-except block that avoids code failing when the Gromacs tools
    are not available --- in some cases they are not necessary to use
    parts of GromacsWrapper.

    .. Note:: Any function defined here **must be listed in ``global``**!
    """
    global trj_compact, rmsd_backbone, trj_fitted, trj_xyfitted

    trj_compact = tools.Trjconv(ur='compact', center=True, boxcenter='tric', pbc='mol',
                                input=('protein','system'),
                                doc="""
Writes a compact representation of the system centered on the protein""")

    rmsd_backbone = tools.G_rms(what='rmsd', fit='rot+trans',
                                input=('Backbone','Backbone'),
                                doc="""
Computes RMSD of backbone after fitting to the backbone.""")

    trj_fitted = tools.Trjconv(fit='rot+trans',
                               input=('backbone', 'system'),
                               doc="""
Writes a trajectory fitted to the protein backbone.

Note that this does *not* center; if center is required, the *input*
selection should have the group to be centered on in second position,
e.g. ``input = ('backbone', 'Protein', System')``.
""")


    # Gromacs 4.x
    trj_xyfitted = tools.Trjconv(fit='rotxy+transxy',
                                 input=('backbone', 'protein','system'),
                                 doc="""
Writes a trajectory fitted to the protein in the XY-plane only.

This is useful for membrane proteins. The system *must* be oriented so
that the membrane is in the XY plane. The protein backbone is used
for the least square fit, centering is done for the whole protein.

Note that centering together with fitting does not always work well
and that one sometimes need two runs of trjconv: one to center and
one to fit.

.. Note:: Gromacs 4.x only""")