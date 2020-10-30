class ContactListEditor:
    ''' to edit contact_list.csv file '''
    def __init__(self, file_path):
        self._contact_list = []
        self._file_path = file_path

    def set_file_path(self, file_path):
        self._file_path = file_path

    def get_file_path(self):
        return self._file_path

    def get_contact_list(self):
        return self._contact_list

    def save_to_file(self):
        '''This function is used to save all contacts into the file, overwrite original contact list.'''
        with open(self._file_path, mode='w', encoding='utf-8') as contact_file:
            contact_file.seek(0)
            for _, item in enumerate(self._contact_list):
                name = item[1]
                number = item[2]
                line = name + ',' + number + '\n'
                contact_file.write(line)

    def load_from_file(self):
        '''This function is used to load all contacts from thr file into a list. '''
        with open(self._file_path, 'r+', encoding='utf-8') as contact_file:
            id = 0
            for line in contact_file:
                id += 1
                item = line.strip().split(',')
                item.insert(0, id)
                self._contact_list.append(tuple(item))
        return self._contact_list

    def add(self, new_contact_name, new_contact):
        '''This function is used to add new phone number into contact list not file.'''
        id = len(self._contact_list) + 1
        new_line = (id, new_contact_name, new_contact)
        self._contact_list.append(new_line)

    def delete(self, id):
        ''' this function is used to delete existing phone number according to its id. '''
        del self._contact_list[(int(id) - 1)]

    def update(self, id, new_name, new_phone_number):
        ''' this function is used to change and update existing phone number according to its id. '''
        self._contact_list[int(id) - 1] = (int(id), new_name, new_phone_number)

    def search(self, search_content):
        '''This function is used to search phone numbers in the file.'''
        selected_list = []
        for _, item in enumerate(self._contact_list):
            line = str(item)
            if search_content in line:
                selected_list.append(item)
        return selected_list