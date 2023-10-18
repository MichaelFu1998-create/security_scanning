def name(self):
        '''
        Returns the name of the Firebase. If a Firebase instance points to
        'https://my_firebase.firebaseio.com/users' its name would be 'users'
        '''
        i = self.__url.rfind('/')
        if self.__url[:i] == 'https:/':
            return "/"
        return self.__url[i+1:]