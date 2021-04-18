import streamlit as st
import pandas as pd
import numpy as np
from textblob import TextBlob

#st.beta_set_page_config(page_title="Chrome Reviews",page_icon=':smiley:')
#database
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password =?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def chrome_rev():
    st.sidebar.title("Upload Your File")
    DATA_URL = st.sidebar.file_uploader("Choose a file", type=['xlsx', 'csv'])

    st.sidebar.markdown("---")


    # Function that tries to read file as a csv
    # if selected file is not a csv file then it will load as an excel file


    st.title("Chrome Reviews")
    st.markdown(" Dashboard 💥")

    if DATA_URL:
        df = pd.read_csv(DATA_URL)
    #DATA_URL = ("886b0f99596a_2020-05-06-HCG.xlsx")
        #@st.cache(persist=True)
        #df = pd.read_excel(DATA_URL)
        if st.checkbox("Show Raw Data", False):
            st.subheader('Raw Data')
            st.write(df)


        def sentiment_calc(text):
            try:
                return TextBlob(text).sentiment.polarity
            except:
                return None

        df['sentiment'] = df['Text'].apply(sentiment_calc)


        most_negative = df[df.sentiment == -1]
        most_positive = df[df.sentiment == 1]

        goodreview_lowrating = df.loc[(df.sentiment == 1)&(df['Star'] < 3)]
        badreview_goodrating = df.loc[(df.sentiment == -1)&(df['Star'] >= 3)]

        st.header("Good Review But Lower Rating")
        st.write(goodreview_lowrating)

        st.header("Bad Review But Higher Rating")
        st.write(badreview_goodrating)


def main():
    st.title("Chrome Reviews 🌐")
    menu = ["Home","Login","Signup"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice =="Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section 🛎️")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')

        if st.sidebar.checkbox("Login"):
            #if password =='12345':
            create_usertable()
            result = login_user(username,password)
            if result:
                st.success("Logged In As {}".format(username))

                task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
                if task =="Add Post":
                    st.subheader("Chrome Reviews Data Analysis Using TextBlob! ")
                elif task == "Analytics":
                    st.subheader("Analytics 📈")
                    chrome_rev()
                elif task == "Profiles":
                    st.subheader("User Profle")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Userame/Password")


    elif choice == "Signup":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,new_password)
            st.success("You have successfully created an Account!")
            st.info("Go to Login Menu to login")



if __name__ =='__main__':
    main()
