import os.path

# Create .txt file with credentials and retrieve the info for further proceedings
def recordcredentials():
    try:
        # Check if the file already exists
        if os.path.isfile('login_info_for_reddit.txt'):
            filewithcredentials = open('login_info_for_reddit.txt','r').read().split('\n')
            USERNAME = filewithcredentials[0]
            PASSWORD = filewithcredentials[1]
            return USERNAME,PASSWORD
        else:
            # Otherwise create credentials file
            USERNAME = input('Enter your login: ')
            PASSWORD = input('Enter your pass: ')
            with open('login_info_for_reddit.txt','w') as f:
                f.write(USERNAME)
                f.write('\n')
                f.write(PASSWORD)
                f.close()
            return USERNAME,PASSWORD
    except:
        # If smth is wrong - delete the file.
        print('Error. Please, rerun the file.')
        os.remove('login_info_for_reddit.txt')