'''This is a phone number management app'''
import sys
import math
from flask import Flask, session, render_template, request, redirect
from contact_list_editor import ContactListEditor

FILE_PATH = 'contact_list.csv'
app = Flask(__name__)
app.secret_key = 'myapp'

@app.route('/', methods=['GET'])
def home():
    ''' This function is to display home page on the browser'''
    if session.get('is_logined', False) is None:
        return redirect('/login')

    editor = ContactListEditor(FILE_PATH)
    editor.load_from_file()
    contact_list = []
    search_content = request.args.get('search')
    # app.logger.info(search_content)
    per_page = int(request.args.get('per_page', 5))
    page_index = int(request.args.get('page_index', 1))

    if search_content is None:
        contact_list = editor.get_contact_list()
    else:
        contact_list = editor.search(search_content)

    max_pages = math.ceil(len(contact_list)/per_page)
    print(max_pages, file=sys.stderr)
    start_index = (page_index - 1) * per_page
    contact_list = contact_list[start_index : start_index + per_page]
    return render_template(
        'home.html',
        contact_list=contact_list,
        page_index=page_index,
        per_page=per_page,
        max_pages=max_pages
    )

@app.route('/add', methods=['POST'])
def add():
    ''' This function is to add new contact into database and back to home page'''
    editor = ContactListEditor(FILE_PATH)
    name = request.form['name']
    phone_number = request.form['phone_number']
    editor.load_from_file()
    editor.add(name, phone_number)
    editor.save_to_file()
    return redirect('/')

@app.route('/new')
def new():
    """
    This function is to redirect to new page to fill in
    information once clicked add new contact button
    """
    return render_template('new.html')

@app.route('/delete/<record_id>')
def delete(record_id):
    """
    This function is to delete existing contact record
    from database and back to home page
    """
    editor = ContactListEditor(FILE_PATH)
    editor.load_from_file()
    editor.delete(record_id)
    editor.save_to_file()
    return redirect('/')

@app.route('/update/<record_id>')
def update(record_id):
    ''' This function is to redirect to update page to edit the record's information '''
    editor = ContactListEditor(FILE_PATH)
    editor.load_from_file()
    contact_list = editor.get_contact_list()
    old_data = contact_list[int(record_id) - 1]
    old_name = old_data[1]
    old_phone_number = old_data[2]
    return render_template(
        'update.html',
        id=int(record_id),
        old_name=old_name,
        old_phone_number=old_phone_number
    )

@app.route('/update_info', methods=['POST'])
def update_info():
    ''' This function is to update information in the database and back to home page '''
    record_id = request.form['id']
    new_name = request.form['name']
    new_phone_number = request.form['phone_number']
    editor = ContactListEditor(FILE_PATH)
    editor.load_from_file()
    editor.update(record_id, new_name, new_phone_number)
    editor.save_to_file()
    return redirect('/')

@app.route('/login')
def login():
    ''' This function is to display login page '''
    msg = session.get('login_msg', '')
    return render_template('login.html', msg=msg)

@app.route('/login_verify', methods=['POST'])
def result():
    ''' This function is to verify login username and password '''
    username = request.form['username']
    password = request.form['password']
    if username == 'admin@gmail.com' and password == 'password':
        session['is_logined'] = True
        session['login_msg'] = ''
    else:
        session['is_logined'] = False
        session['login_msg'] = 'Username or password is wrong!'

    return redirect('/')

@app.route('/logout')
def logout():
    ''' This function is to logout from the app '''
    session['is_logined'] = False
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
