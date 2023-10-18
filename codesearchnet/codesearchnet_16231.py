def main():
    """Test the functionality of the rController object"""
    import time

    print('Testing controller in position 1:')
    print('Running 3 x 3 seconds tests')

    # Initialise Controller
    con = rController(1)

    # Loop printing controller state and buttons held
    for i in range(3):
        print('Waiting...')
        time.sleep(2.5)
        print('State: ', con.gamepad)
        print('Buttons: ', con.buttons)
        time.sleep(0.5)

    print('Done!')