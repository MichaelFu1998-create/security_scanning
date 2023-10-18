def processClubConsumption(f, clubs):
  """Process the consumption a club
  
  - Skip the header line
  - Iterate over lines
    - Read 4 records at a time
      - Parse each line: club, date, time, consumption
      - Get club object from dictionary if needed
      - Aggregate consumption
    - Call club.processConsumption() with data
  """
  try:
    # Skip header line
    line = f.next()
    assert line.endswith('"   ","SITE_LOCATION_NAME","TIMESTAMP","TOTAL_KWH"\n')

    valid_times = range(24)
    t = 0 # used to track time
    club = None
    clubName = None
    lastDate = None
    while True:
      assert t in valid_times
      consumption = 0
      for x in range(4):
        # Read the line and get rid of the newline character
        line = f.next()[:-1]
        fields = line.split(',')
        assert len(fields) == 4
        for i, field in enumerate(fields):
          # Strip the redundant double quotes
          assert field[0] == '"' and field[-1] == '"'
          fields[i] = field[1:-1]
        
        # Ignoring field 0, which is just a running count
        
        # Get the club name  
        name = fields[1]
        
        # Hack to fix inconsistent club names like: "Melbourne CBD - Melbourne Central" vs. "Melbourne Central"
        partialNames = ('Melbourne Central', 'North Sydney', 'Park St', 'Pitt St')
        for pn in partialNames:
          if pn in name:
            name = pn
        
        # Locate the club if needed (maybe )
        if name != clubName:
          clubName = name
          club = clubs[name]
        
        # Split the date (time is counted using the t variable)
        tokens = fields[2].split()
        
        # Verify that t == 0 and consumption == 0 when there is no time in the file
        if len(tokens) == 1:
          assert consumption == 0 and t == 0
        
        # The first (and sometimes only) token is the date
        date = tokens[0]
                
        # Aggregate the consumption
        consumption += float(fields[3])
      
      # Update the Club object after aggregating the consumption of 4 lines 
      club.updateRecord(date, t, consumption)
      
      # Increment time
      t += 1
      t %= 24
  except StopIteration:
    return