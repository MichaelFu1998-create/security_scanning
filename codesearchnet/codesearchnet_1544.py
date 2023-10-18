def processClubAttendance(f, clubs):
  """Process the attendance data of one club
  
  If the club already exists in the list update its data.
  If the club is new create a new Club object and add it to the dict
  
  The next step is to iterate over all the lines and add a record for each line.
  When reaching an empty line it means there are no more records for this club.
  
  Along the way some redundant lines are skipped. When the file ends the f.next()
  call raises a StopIteration exception and that's the sign to return False,
  which indicates to the caller that there are no more clubs to process.
  """
  try:
    # Skip as many empty lines as necessary (file format inconsistent)
    line = f.next()
    while line == ',,,,,,,,,,,,,,,,,,,\n':
      line = f.next()
    
    # The first non-empty line should have the name as the first field
    name = line.split(',')[0]
    
    # Create a new club object if needed
    if name not in clubs:
      clubs[name] = Club(name)
    
    # Get the named club
    c = clubs[name]
    
    c.processAttendance(f)      
    return True
  except StopIteration:
    return False