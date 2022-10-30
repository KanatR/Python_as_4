from enum import unique
from wsgiref.validate import validator
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import create_engine, false, select, Table, Column, Integer, String, MetaData, ForeignKey
import requests


app = Flask (__name__)

#app.config['SECTER_KEY'] = 'Thisissupposetobesecret!'
app.config['SECRET_KEY'] = 'any secret string'
Bootstrap(app)




meta = MetaData()

users = Table ( 'users', meta,
    Column('user_id', Integer,primary_key = True ),
    Column('username', String(250),nullable = false),
    Column('password', String(250),nullable = false)
)
nft = Table ( 'nft', meta,
    Column('nft_id', Integer,primary_key = True ),
    Column('address', String(250),nullable = false,),
    Column('info', String(250),nullable = false)
)

engine = create_engine('postgresql+psycopg2://postgres:19Rjy0203@127.0.0.1:5432/user')
meta.create_all(engine)
conn = engine.connect()




class LoginForm(FlaskForm):
    username = StringField('username',validators = [InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators = [InputRequired(),Length(min=4,max=80)])

class RegisterForm(FlaskForm):
    username = StringField('username',validators = [InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators = [InputRequired(),Length(min=4,max=80)])

class IndexForm(FlaskForm):
    address = StringField('address',validators = [InputRequired(),Length(min=4,max=80)])
  


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user_username_query = users.select().where(users.c.username == form.username.data ) 
        result = conn.execute(user_username_query)

        for row in result:
         if row.username == form.username.data:
            user_password_query = users.select().where(users.c.password == form.password.data )
            result2 = conn.execute(user_password_query)
            for row2 in result2:
                if row2.password == form.password.data:
                    return   redirect(url_for('index')) #render_template('index.html')   redirect(url_for('index'))

    return render_template('login.html',form = form)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_ist_query = users.insert().values(username = form.username.data ,password = form.password.data )
        conn.execute(user_ist_query )
    return render_template('signup.html',form = form)    


@app.route('/index',methods = ['GET','POST'])    
def index():
    form = IndexForm()
    if form.validate_on_submit():
        #nft_address_query = nft.select().where(nft.c.address == form.address.data ) 
        #result = conn.execute(nft_address_query )
        #if result:
         #       for row in result:
                
          #       print(row.info)
        #else:
                address = form.address.data
                url = "https://solana-gateway.moralis.io/nft/mainnet/" + address + "/metadata"
                headers = {
                     "accept": "application/json",
                     "X-API-Key": "SWnpmagdLrYt67aFhsaBRRzoubD59cdQkydkZLeljvVREBpWGmpLktfRLZXcvudp"
                }
                response = requests.get(url, headers=headers) 
                #ins_nft_query = nft.insert().values(address = form.address.data,info = response)
                #conn.execute(ins_nft_query)
                print(response.text) 
                nft_result =  nft.select().where(nft.c.address == form.address.data )
                for row in nft_result:
                    if row.username == form.address.data:
                        '<h1>'+ response.text + '</h1>'
                    else:
                        ins_nft_query = nft.insert().values(address = form.address.data,info = response.text)  
                        conn.execute(ins_nft_query) 
                        '<h1>'+ response.text + '</h1>'  
    return render_template('index.html',form = form)
#################################################################################################################################################



if __name__ == '__main__':
    app.run(debug=True)   