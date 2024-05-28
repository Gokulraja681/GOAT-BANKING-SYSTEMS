from flask import *
import random
import pymongo
from bson import ObjectId

app = Flask(__name__)
app.secret_key = '060801'

mongocon = pymongo.MongoClient('mongodb://localhost:27017')
mydb = mongocon['Banking']
mycol = mydb['Data']



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

"------------------------------------------------------------------------"
# Creating some initiaters for the Signup and signin
class SS:
    def __init__(self):
        self.fname = ""
        self.lname = ""
        self.gmail = ""
        self.pswd = ""
    
rg = SS()


@app.route('/signup', methods = ["POST", "GET"])
# Signup module with required parameters
def signup():
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    if request.method == "POST":
        rg.fname = request.form.get('fname')
        rg.lname = request.form.get('lname')
        temp_mail = request.form['gmail']
        existing_user = mycol.find_one({'gmail': temp_mail})
        if existing_user:
            msg2 = 'Account already exists'
        else:
            rg.gmail = temp_mail
            p = request.form['p']
            if len(p) < 8:
                msg = 'Password must contain 8 characters'
            else:
                rg.pswd = request.form['pswd']
                if rg.pswd != p:
                    msg1 = 'password not matched with each other'
                else:
                    rg.pswd = p
                    mydoc = {
                        'fname': rg.fname,
                        'lname': rg.lname,
                        'gmail': rg.gmail,
                        'pswd' : rg.pswd
                    }
                    mycol.insert_one(mydoc)
                    return redirect(url_for('signin'))
    return render_template('signup.html', msg=msg, msg1=msg1, notify=notify, msg2=msg2)


# Account Profile module for testing
@app.route('/details', methods = ["GET", "POST"])
def details():
    if request.method == "GET":
        all_details = mycol.find()
        return render_template('details.html', all_details = all_details)


# Signin Page module
@app.route('/signin', methods = ["POST", "GET"])
def signin():
    msg = None
    msg1 = None
    if request.method == "POST":
        s_gmail = request.form.get('s_gmail')            
        s_pswd = request.form.get('s_pswd')
        user = mycol.find_one({'gmail': s_gmail})
        if user and user['pswd'] == s_pswd:
            session['user'] = str(user['_id'])
            return redirect(url_for('index'))
        else:
            msg = "Enter mail or password is not matched"
    return render_template('signin.html', msg = msg, msg1 = msg1)

@app.route('/forget_password', methods=["POST", "GET"])
def forget_password():
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    
    if request.method == "POST":
        f_gmail = request.form.get('f_gmail')
        change_mail = mycol.find_one({'gmail': f_gmail})

        if change_mail:
            user_id = change_mail['_id']
            p = request.form['p']
            if len(p) < 8:
                msg1 = "Password must contain 8 characters"
            else:
                f_pswd = request.form['f_pswd']
                if f_pswd != p:
                    msg2 = "Password not matched"
                else:
                    mycol.update_one({'_id': ObjectId(user_id)}, {'$set': {'pswd': f_pswd}})
                    return redirect(url_for('signin'))
        else:
            msg = "Please enter a valid mail-id"
    return render_template('forget_password.html', msg=msg, msg1=msg1, msg2=msg2, notify=notify)
"---------------------------------------------------------------------------------"


@app.route('/index')
def index():
    return render_template('index.html')


#Creating Some initiaters for the datas
class GORA:
    def __init__(self):
        self.name = ""
        self.father_name = ""
        self.dob = ""
        self.gender = ""
        self.mbno = ""
        self.pin = ""
        self.amount = 0
        self.acn = 0

gr = GORA()


# Account Creation Module
@app.route('/account_creation', methods = ["POST", "GET"])
def account_creation():
    msg2 = None
    data = None
    if request.method == "POST":
        if 'user' in session:
            user_id = session['user']
            data = mycol.find_one({'_id': ObjectId(user_id)})
            type = request.form['type']
            currency_type = request.form['currency_type']
            prefix = request.form['prefix']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gr.father_name = request.form.get('father_name')
            mother_name = request.form['mother_name']
            gr.dob = request.form.get('dob')
            gr.gender = request.form.get('gender')
            gr.mbno = request.form.get('mbno')
            temporary_address = request.form['temporary_address']
            permanent_address = request.form['permanent_address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postal = request.form['postal']
            country = request.form['country']
            marital_status = request.form['marital_status']
            occupation = request.form['occupation']
            b = random.randint(24620100014670, 29999999999999)
            gr.acn = b
            gr.amount = int(request.form.get('amount'))
            if gr.amount < 1000:
                msg2 = "For account creation initial deposit amount is 1000"
            else:
                mydoc={
                    'First_Name': first_name,
                    'Last_Name': last_name,
                    'Father_Name': gr.father_name,
                    'Mother_Name': mother_name,
                    'DOB': gr.dob,
                    'Gender': gr.gender,
                    'Mbno': gr.mbno,
                    'Account_Number': gr.acn,
                    'Amount': gr.amount,
                    'Currency_Type': currency_type,
                    'Account_Type' : type,
                    'Prefix' : prefix,
                    'Temporary_Address': temporary_address,
                    'Permanent_Address': permanent_address,
                    'City': city,
                    'State': state,
                    'Postal': postal,
                    'Country': country,
                    'Occupation': occupation,
                    'Marital_Status': marital_status
                    }
                mycol.update_one({'_id': ObjectId(user_id)}, {'$set': mydoc})
                return redirect(url_for('profile'))
        else:
            return 'something went worng!'
    return render_template('account_creation.html', msg2=msg2, data = data)


#Accout Pin Creation
@app.route('/pin_creation', methods = ['POST','GET'])
def pin_creation():
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    msg5 = None
    msg6 = None
    data = None
    if request.method == 'POST':
        if 'user' in session:
            user_id = session['user']
            data = mycol.find_one({'_id': ObjectId(user_id)})
            original_pin = data['Pin']
            acn = request.form['acn']
            if acn == '':
                msg1 = 'Please enter Account Number'
            elif not acn .isnumeric:
                msg2 =  'Please enter valid Account Number'
            else:
                acn = int(acn)
                mbno = request.form['mbno']
                if (acn != data['Account_Number']) or (mbno != data['Mbno']):
                    msg3 = 'Mobile Number or Account Number not matched with each other'
                else:
                    create_pin = request.form['create_pin']
                    if len(create_pin) != 6:
                        msg4 = 'pin must contain 6 characters'
                    else:
                        pin = request.form['pin']
                        if (pin != create_pin):
                            msg5 = 'Pin not matched with each other'
                        elif original_pin:
                            msg6 = 'Pin already exists for this Account Number!'
                        else:
                            mycol.update_one({'_id': ObjectId(user_id)},
                                             {'$set': {'Pin': pin}})
                            return redirect(url_for('profile'))
        else:
            return "something went wrong"
    return render_template('pin_creation.html', msg = msg, msg1=msg1, msg2 = msg2,
                           msg3 = msg3, msg4 = msg4, msg6 = msg6,
                            msg5 = msg5, data = data)


# Account Holder's Profile Module
@app.route('/profile', methods=["GET"])
def profile():
    if request.method == 'GET':
        if 'user' in session:
            user_id = session['user']
            data = mycol.find_one({'_id': ObjectId(user_id)})
            return render_template('profile.html', data = data)
        else:
            return 'User not logged in'
    else:
        return 'something went Worng'


# Account Profile Edit module
@app.route('/edit_profile', methods = ['POST', 'GET'])
def edit_profile():
    if request.method == 'POST':
        return render_template('edit_profile.html')


# Account Withdrawal Module
@app.route('/withdrawal', methods = ["POST", "GET"])
def withdrawal():
    amt = 0
    total = 0
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    notify = None
    data = None

    if 'user' in session:
        user_id = session['user']
        data = mycol.find_one({'_id': ObjectId(user_id)})
        
        if request.method == "POST":
            amt  = int(request.form.get('amt'))
            if amt < 500:
                msg = "Minimum Deposit Amount is 500"
            elif amt > data['Amount']:
                msg3 = "Doesn't have enough balance"
            else:
                pin = request.form.get('pin')
                if pin != data['Pin']:
                    msg1 = "Please enter your pin correctly"
                else:
                    total = data['Amount'] - amt
                    notify = f"{amt} has been debited from your account !"
                    msg2 = "Amount Withdrawal is Successful !"
                    mycol.update_one({'_id': ObjectId(user_id)}, {'$set': {
                        'Amount': total
                    }})
    return render_template('withdrawal.html', msg = msg, msg1 = msg1, 
                           msg2 = msg2, notify = notify, msg3 = msg3, data = data)


# Amount Deposit Module
@app.route('/deposit', methods=["POST", "GET"])
def deposit():
    amt = 0
    total = 0
    msg = None
    msg1 = None
    msg2 = None
    notify = None
    data = None

    if 'user' in session:
        user_id = session['user']
        data = mycol.find_one({'_id': ObjectId(user_id)})

        if request.method == "POST":
            amt = int(request.form.get('amt'))

            if amt < 500:
                msg = "Minimum Deposit amount is 500"
            else:
                pin = request.form.get('pin')

                if pin != data['Pin']:
                    msg1 = 'Please enter your Pin correctly'
                else:
                    total = data['Amount'] + amt
                    mycol.update_one({'_id': ObjectId(user_id)}, 
                                     {'$set': {'Amount': total}})
                    notify = "Amount deposited successfully"

    return render_template('deposit.html', msg=msg, msg1=msg1, 
                           msg2=msg2, notify=notify, data=data)


# Tranfering Money
@app.route('/transfer_money', methods=['POST', 'GET'])
def transfer_money():
    data = None
    receiver_account = None
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    msg5 = None
    if 'user' in session:
        user_id = session['user']
        data = mycol.find_one({'_id': ObjectId(user_id)})
        if request.method == 'POST':
            receiver = request.form['receiver']
            if receiver == '':
                msg4 = 'Please enter account number first'
            elif not receiver.isnumeric():
                msg = 'Please enter a valid receiver account number'
            else:
                receiver = int(receiver)
                amount = request.form['amt']
                if amount == '':
                    msg1 = 'Please enter amount first'
                else:
                    amount = int(amount)
                    if data['Amount'] < amount:
                        msg2 = 'Insufficient Amount'
                    else:
                        pin = request.form['pin']
                        if pin != data['Pin']:
                            msg5 = 'Pin not matched !'
                        else:
                            receiver_account = mycol.find_one({'Account_Number': receiver})
                            if receiver_account:
                                mycol.update_one({'_id': ObjectId(user_id)},
                                                 {'$inc':{'Amount': -amount}})
                                mycol.update_one({'_id': receiver_account['_id']},
                                                 {'$inc': {'Amount': amount}})
                            else:
                                msg3 = 'User Account not exists'
    return render_template('transfer_money.html', msg = msg, msg1 = msg1,
                           data=data, receiver_account = receiver_account,
                           msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5)


# Balance Enquiry Module
@app.route('/balance_enquiry', methods = ["GET", "POST"])
def balance_enquiry():
    msg = None
    if request.method == "GET":
        msg = "Your Account Current Balance Details"
        if 'user' in session:
            user_id = session['user']
            data = mycol.find_one({'_id': ObjectId(user_id)})
            return render_template('balance_enquiry.html', data = data, msg = msg)
        else:
            return 'something went wrong'


# Change the Pin
@app.route('/change_pin', methods = ["GET", "POST"])
def change_pin():
    msg = None
    msg1 = None
    msg2 = None
    msg3 = None
    msg4 = None
    data = None
    if request.method == "POST":

        if 'user' in session:
            user_id = session['user']
            data = mycol.find_one({'_id': ObjectId(user_id)})

            if data:
                mbno = request.form.get('mbno')

                if mbno != data['Mbno']:
                    msg = "Entered Mobile number is not matched"
                else:
                    acn  = int(request.form.get('acn'))

                    if acn != data['Account_Number']:
                        msg1 = "Entered Account Number is not matched"
                    else:
                        re_pin = request.form.get('re_pin')

                        if len(re_pin) != 6:
                            msg2 = "Pin should contain 6 characters"
                        else:
                            pin = request.form.get('pin')

                            if pin != re_pin:
                                msg3 = "Pin not matched with each other"
                            else:
                                msg4 = "Pin has been Changed Successfully"
                                mycol.update_one({'_id': ObjectId(user_id)},
                                                 {'$set': {'Pin': pin}})
                                return redirect(url_for('profile'))
            else:
                return 'User data not found'    
        else:
            return 'something went wrong!' 
                                  
    return render_template('change_pin.html', msg = msg, msg1 = msg1, msg2 = msg2,
                           msg3 = msg3, msg4 = msg4)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))


if __name__ == "__main__":
    app.run(debug=True)
