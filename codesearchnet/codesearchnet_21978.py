def setupUI(self):
        '''Create graphical objects for menus.'''
        
        labelSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        labelSizePolicy.setHorizontalStretch(0)
        labelSizePolicy.setVerticalStretch(0)
        menuSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        menuSizePolicy.setHorizontalStretch(0)
        menuSizePolicy.setVerticalStretch(0)
        
        logTypeLayout = QHBoxLayout()
        logTypeLayout.setSpacing(0)
        
        typeLabel = QLabel("Log Type:")
        typeLabel.setMinimumSize(QSize(65, 0))
        typeLabel.setMaximumSize(QSize(65, 16777215))
        typeLabel.setSizePolicy(labelSizePolicy)
        logTypeLayout.addWidget(typeLabel)
        self.logType = QComboBox(self)
        self.logType.setMinimumSize(QSize(100, 0))
        self.logType.setMaximumSize(QSize(150, 16777215))
        menuSizePolicy.setHeightForWidth(self.logType.sizePolicy().hasHeightForWidth())
        self.logType.setSizePolicy(menuSizePolicy)
        logTypeLayout.addWidget(self.logType)
        logTypeLayout.setStretch(1, 6)
        
        programLayout = QHBoxLayout()
        programLayout.setSpacing(0)
        
        programLabel = QLabel("Program:")
        programLabel.setMinimumSize(QSize(60, 0))
        programLabel.setMaximumSize(QSize(60, 16777215))
        programLabel.setSizePolicy(labelSizePolicy)
        programLayout.addWidget(programLabel)
        self.programName = QComboBox(self)
        self.programName.setMinimumSize(QSize(100, 0))
        self.programName.setMaximumSize(QSize(150, 16777215))
        menuSizePolicy.setHeightForWidth(self.programName.sizePolicy().hasHeightForWidth())
        self.programName.setSizePolicy(menuSizePolicy)
        programLayout.addWidget(self.programName)
        programLayout.setStretch(1, 6)
        
        # Initial instance allows adding additional menus, all following menus can only remove themselves.
        if self.initialInstance:
            self.logButton = QPushButton("+", self)
            self.logButton.setToolTip("Add logbook")
        else:
            self.logButton = QPushButton("-")
            self.logButton.setToolTip("Remove logbook")
        
        self.logButton.setMinimumSize(QSize(16, 16))  # 24x24
        self.logButton.setMaximumSize(QSize(16, 16))  # 24x24
        self.logButton.setObjectName("roundButton")
        # self.logButton.setAutoFillBackground(True)
        # region = QRegion(QRect(self.logButton.x()+15, self.logButton.y()+14, 20, 20), QRegion.Ellipse)
        # self.logButton.setMask(region)
        
        self.logButton.setStyleSheet("QPushButton {border-radius: 8px;}")
        
        self._logSelectLayout = QHBoxLayout()
        self._logSelectLayout.setSpacing(6)
        self._logSelectLayout.addLayout(logTypeLayout)
        self._logSelectLayout.addLayout(programLayout)
        self._logSelectLayout.addWidget(self.logButton)
        self._logSelectLayout.setStretch(0, 6)
        self._logSelectLayout.setStretch(1, 6)