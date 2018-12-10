from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

app = Flask(__name__)
app.secret_key = '2y14ZhoB0P'

conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='PriCoSha',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    return redirect('/home')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    email = request.form['email']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM Person WHERE email = %s and password = SHA2(%s, 256)'
    cursor.execute(query, (email, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['email'] = email
        return redirect(url_for('home'))
    else:
        error = 'Invalid login or email'
        return render_template('login.html', error=error)

@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM Person WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()
    error = None
    if(data):
        error = "This Person already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, SHA2(%s, 256), %s, %s)'
        cursor.execute(ins, (email, password, fname, lname))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    if 'email' in session:
        email = session['email']
        cursor = conn.cursor()
        query = 'SELECT item_id, email_post, post_time, event_name, event_description, event_date, event_location\
        FROM ContentItem WHERE  (\
        is_pub=1 OR (is_pub=0 AND item_id IN ( \
            SELECT item_id FROM Share WHERE fg_name IN ( \
                SELECT fg_name FROM Belong WHERE email=%s ))) \
        )\
        AND post_time > DATE_SUB(NOW(), INTERVAL 24 HOUR) \
        ORDER BY post_time DESC'
        cursor.execute(query, (email))
        query_data = cursor.fetchall()
        
        tags = "select item_id, fname, lname from Person join Tag on (email=email_tagged) where status=\'True\'"
        cursor.execute(tags)
        tags_data = cursor.fetchall()
        
        ratings = "select email,item_id,emoji from Rate"
        cursor.execute(ratings)
        ratings_data = cursor.fetchall()
        cursor.close()

        if 'comment_error' in session:
            comment_error = '%s' % session['comment_error']
            session['counter'] += 1
            if (session['counter'] == 2):
                session.pop('comment_error')
                session.pop('counter')
        else: 
            comment_error = None
        return render_template('home.html', email=email, posts=query_data, tags=tags_data, ratings=ratings_data, comment_error=comment_error)
    else:
        cursor = conn.cursor()
        query = 'SELECT item_id, email_post, post_time, event_name, event_description, event_date, event_location\
        FROM ContentItem WHERE is_pub=1 AND post_time > DATE_SUB(NOW(), INTERVAL 24 HOUR) \
        ORDER BY post_time DESC'
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return render_template('home.html', posts=data)

@app.route('/post')
def forPost():
    email_post = session['email']
    cursor = conn.cursor()
    Visibility = 'SELECT fg_name FROM Friendgroup WHERE owner_email = %s'
    cursor.execute(Visibility, (email_post))
    data = cursor.fetchall()
    cursor.close()    
    return render_template('postContent.html',options = data,email = email_post)

@app.route('/postContent', methods=['GET', 'POST'])
def post():
    email_post = session['email']
    cursor = conn.cursor()
    event_name = request.form['event_name']
    event_desp = request.form['event_desp']
    event_date = request.form['event_date']
    event_loc = request.form['event_loc']
    event_fg = request.form.getlist('visibility')

    query = 'INSERT INTO ContentItem VALUES (NULL,%s,CURRENT_TIMESTAMP,%s,%s,%s,%s,%s)'
    if 'public' in event_fg:
        cursor.execute(query, (email_post,event_name,event_desp,event_date,event_loc,'1'))
    else:
        cursor.execute(query, (email_post,event_name,event_desp,event_date,event_loc,'0'))
        query = 'select item_id from ContentItem'
        cursor.execute(query)
        id = cursor.fetchall()[-1]['item_id']
        for fg in event_fg:
            share =  'INSERT INTO Share VALUES(%s,%s,%s)'
            cursor.execute(share, (email_post, fg, id))

    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/add_tag', methods=['POST'])
def add_tags():
    email_post = session['email']
    cursor = conn.cursor()
    item_id = request.json['id']
    new_tag = request.json['tag']
    temp_q1 = 'select * from Tag where email_tagged=%s and email_tagger=%s and item_id=%s'
    cursor.execute(temp_q1, (new_tag,email_post,item_id))
    data1 = cursor.fetchall()

    if (len(data1) == 0):
        query = 'INSERT INTO Tag VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP)'
        if (email_post == new_tag):
            cursor.execute(query, (new_tag,email_post,item_id,'True'))
        else:
            temp_q2 = 'select * from ContentItem where item_id=%s and (is_pub=1 or (is_pub=0 and item_id in ( \
                            select item_id FROM Share WHERE fg_name IN ( \
                                select fg_name from Belong WHERE email=%s ))))'
            cursor.execute(temp_q2, (item_id, new_tag))
            data2 = cursor.fetchall()
            if (len(data2) != 0):
                cursor.execute(query, (new_tag,email_post,item_id,'False'))

    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/tags', methods=['GET'])
def tags():
    email_post = session['email']
    cursor = conn.cursor()
    query = 'select * from ContentItem natural join Tag where email_tagged=%s and status=\'False\''
    cursor.execute(query, (email_post))
    data = cursor.fetchall()
    cursor.close()
    return render_template('tags.html',email=email_post,posts=data)

@app.route('/tags', methods=['POST'])
def manage_tags():
    email_post = session['email']
    cursor = conn.cursor()
    item_id = request.json['id']
    tagger = request.json['tagger']

    if (request.json['do'] == 'accept'):
        query = 'update Tag set status=\'True\' where item_id=%s and email_tagged=%s and email_tagger=%s'
    else:
        query = 'delete from Tag where item_id=%s and email_tagged=%s and email_tagger=%s'

    cursor.execute(query, (item_id, email_post, tagger))
    conn.commit()
    cursor.close()
    return redirect(url_for('tags'))

@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    email_signed = session['email']
    cursor = conn.cursor()
    item_id = request.json['item_id']
    query_check = 'Select item_id from Signup where item_id=%s and email_signed=%s'
    query_insert = 'INSERT INTO Signup VALUES (%s, %s)'
    cursor.execute(query_check,(item_id,email_signed))
    data = cursor.fetchall()

    if (len(data) == 0):
        cursor.execute(query_insert,(item_id,email_signed))

    conn.commit()
    cursor.close()
    return redirect('/home')

@app.route('/DeleteEvent', methods=['GET', 'POST'])
def DeleteEvent():
    email_signed = session['email']
    cursor = conn.cursor()
    item_id = request.json['item_id']
    delete_signup= 'delete from Signup where item_id=%s '
    delete_tag= 'delete from Tag where item_id=%s '
    delete_rating= 'delete from Rate where item_id=%s '
    delete_share= 'delete from Share where item_id=%s '
    delete_ContentItem= 'delete from ContentItem where item_id=%s'
    cursor.execute(delete_signup,(item_id))
    cursor.execute(delete_tag,(item_id))
    cursor.execute(delete_share,(item_id))
    cursor.execute(delete_rating,(item_id))
    cursor.execute(delete_ContentItem,(item_id))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/myEvents', methods=['GET', 'POST'])
def myEvent():
    email = session['email']
    cursor = conn.cursor();
    query = 'SELECT item_id, email_post, post_time, event_name, event_description, event_date, event_location\
    FROM ContentItem WHERE\
    item_id in ( \
        select item_id from Signup where email_signed=%s)'
    cursor.execute(query,(email))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('event.html',myEvents = data,email=email)

@app.route('/cancelEvents', methods=['GET', 'POST'])
def CancelEvent():
    email_signed = session['email']
    cursor = conn.cursor();
    item_id = request.json['item_id']
    delete_signup= 'delete from Signup where item_id=%s '
    cursor.execute(delete_signup,(item_id))
    conn.commit()
    cursor.close()
    return redirect(url_for('myEvent'))

@app.route('/add_comment', methods=['POST'])
def add_comments():
    email_post = session['email']
    cursor = conn.cursor()
    item_id = request.json['id']
    new_comment = request.json['comment']
    test_query = 'SELECT * FROM Rate WHERE email=%s and item_id=%s'
    cursor.execute(test_query,(email_post,item_id))
    test=cursor.fetchone()
    if (test):
        session['comment_error'] = 'You have already posted a comment for this event'
        session['counter'] = 0
    else:
        query = 'INSERT INTO Rate VALUES (%s,%s,CURRENT_TIMESTAMP,%s)'
        cursor.execute(query, (email_post,item_id,new_comment))

    conn.commit()
    cursor.close()
    return redirect('/home')

@app.route('/friendgroup')
def forAddFriend():
    if 'error' in session:
        error = session['error']
    else: 
        error = None
    email = session['email']

    cursor = conn.cursor()
    group = 'SELECT fg_name,owner_email From Belong NATURAL JOIN Friendgroup WHERE email=%s'
    cursor.execute(group, (email))
    query_data = cursor.fetchall()

    member = 'SELECT owner_email, fg_name, email FROM Belong JOIN Friendgroup USING (owner_email,fg_name)'
    cursor.execute(member)
    member_data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('friendGroup.html', email=email, posts=query_data,member=member_data, error=error)

@app.route('/friendGroup', methods=['GET', 'POST'])
def friendgroup():
    email = session['email']
    cursor = conn.cursor()
    fg_name = request.json['fg_name']
    first_name = request.json['First_Name']
    last_name = request.json['Last_Name']
    Specified_email=request.json['Specified_email']

    toadd_email = 'SELECT email FROM Person WHERE fname=%s AND lname=%s'
    cursor.execute(toadd_email,(first_name,last_name))
    Toadd_email=cursor.fetchall()

    if 'error' in session:
        session.pop('error')
    if (not Toadd_email):
        session['error'] = 'Please enter valid first name and last name'

    else:
        if (len(Toadd_email)==1):
            test_query = 'SELECT * FROM Belong WHERE email = %s AND owner_email=%s AND fg_name=%s'
            cursor.execute(test_query, (str(Toadd_email[0]['email']), email, fg_name))
            test_data = cursor.fetchall()
            if (len(test_data)==0):
                insert_query = 'INSERT INTO Belong VALUES(%s, %s, %s)'
                cursor.execute(insert_query, (Toadd_email[0]['email'], email, fg_name))
            else:
                session['error'] = 'This Person already exists in the group'

        elif (len(Toadd_email)>1):
            test_query = 'SELECT * FROM Belong WHERE email = %s AND owner_email=%s AND fg_name=%s'
            cursor.execute(test_query, (Specified_email, email, fg_name))
            if not Specified_email:
                session['error'] = 'Please specify email'
            else:
                test_data = cursor.fetchall()
                if (len(test_data)==0):
                    insert_query = 'INSERT INTO Belong VALUES(%s, %s, %s)'
                    cursor.execute(insert_query, (Specified_email, email, fg_name))
                else:
                    session['error'] = 'This Person already exists in the group'

    conn.commit()
    cursor.close()
    return redirect(url_for('forAddFriend'))

@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
