def volume_render(field, outfile, maxopacity=1.0, cmap='bone',
        size=600, elevation=45, azimuth=45, bkg=(0.0, 0.0, 0.0),
        opacitycut=0.35, offscreen=False, rayfunction='smart'):
    """
    Uses vtk to make render an image of a field, with control over the
    camera angle and colormap.

    Input Parameters
    ----------------
        field : np.ndarray
            3D array of the field to render.
        outfile : string
            The save name of the image.
        maxopacity : Float
            Default is 1.0
        cmap : matplotlib colormap string
            Passed to cmap2colorfunc. Default is bone.
        size : 2-element list-like of ints or Int
            The size of the final rendered image.
        elevation : Numeric
            The elevation of the camera angle, in degrees. Default is 45
        azimuth : Numeric
            The azimuth of the camera angle, in degrees. Default is 45
        bkg : Tuple of floats
            3-element tuple of floats on [0,1] of the background image color.
            Default is (0., 0., 0.).
    """
    sh = field.shape

    dataImporter = vtk.vtkImageImport()
    dataImporter.SetDataScalarTypeToUnsignedChar()
    data_string = field.tostring()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))

    dataImporter.SetDataExtent(0, sh[2]-1, 0, sh[1]-1, 0, sh[0]-1)
    dataImporter.SetWholeExtent(0, sh[2]-1, 0, sh[1]-1, 0, sh[0]-1)

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(int(255*opacitycut), maxopacity)

    volumeProperty = vtk.vtkVolumeProperty()
    colorFunc = cmap2colorfunc(cmap)
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    volumeMapper = vtk.vtkVolumeRayCastMapper()
    if rayfunction == 'mip':
        comp = vtk.vtkVolumeRayCastMIPFunction()
        comp.SetMaximizeMethodToOpacity()
    elif rayfunction == 'avg':
        comp = vtk.vtkVolumeRayCastCompositeFunction()
    elif rayfunction == 'iso':
        comp = vtk.vtkVolumeRayCastIsosurfaceFunction()
        comp.SetIsoValue(maxopacity/2)
    else:
        comp = vtk.vtkVolumeRayCastIsosurfaceFunction()
    volumeMapper.SetSampleDistance(0.1)
    volumeMapper.SetVolumeRayCastFunction(comp)

    if rayfunction == 'smart':
        volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    light = vtk.vtkLight()
    light.SetLightType(vtk.VTK_LIGHT_TYPE_HEADLIGHT)
    light.SetIntensity(5.5)
    light.SwitchOn()

    renderer = vtk.vtkRenderer()
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderWin.SetOffScreenRendering(1);

    if not hasattr(size, '__iter__'):
        size = (size, size)

    renderer.AddVolume(volume)
    renderer.AddLight(light)
    renderer.SetBackground(*bkg)
    renderWin.SetSize(*size)

    if offscreen:
        renderWin.SetOffScreenRendering(1)

    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.Initialize()
    renderWin.Render()
    renderInteractor.Start()

    #writer = vtk.vtkFFMPEGWriter()
    #writer.SetQuality(2)
    #writer.SetRate(24)
    #w2i = vtk.vtkWindowToImageFilter()
    #w2i.SetInput(renderWin)
    #writer.SetInputConnection(w2i.GetOutputPort())
    #writer.SetFileName('movie.avi')
    #writer.Start()
    #writer.End()

    writer = vtk.vtkPNGWriter()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(renderWin)
    writer.SetInputConnection(w2i.GetOutputPort())

    renderWin.Render()
    ac = renderer.GetActiveCamera()
    ac.Elevation(elevation)
    ac.Azimuth(azimuth)
    renderer.ResetCameraClippingRange()
    renderWin.Render()
    w2i.Modified()
    writer.SetFileName(outfile)
    writer.Write()