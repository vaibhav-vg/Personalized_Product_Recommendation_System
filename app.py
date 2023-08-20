import streamlit as st
import pickle
import pandas as pd

st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://img.freepik.com/premium-vector/background-with-colorful-shopping-bags-vector-illustration-sale-discount-concept_653240-59.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True)

user_recommendation_dict = pickle.load(open('popularity.pkl', 'rb'))

user_recommendation = pd.DataFrame(user_recommendation_dict)

pivot_df_dict = pickle.load(open('pivot_df.pkl', 'rb'))

pivot_df = pd.DataFrame(pivot_df_dict)

preds_df_dict = pickle.load(open('preds_df.pkl', 'rb'))

preds_df = pd.DataFrame(preds_df_dict)

st.title("Product Recommendation System")

option = st.selectbox('Product Category', ('Electronics', 'Beauty', 'Cosmetics'))

genre = st.radio("Type of User", ('New User', 'Existing User'))

if genre == 'New User':
    user_id = st.number_input('Enter UserID', format="%i", value=0)
    user_recommendation['userId'] = user_id
    if st.button('Get Recommendations'):
        cols = user_recommendation.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendation[cols]
        st.write(user_recommendation)

else:
    user_id = st.number_input('Enter UserID', format="%i", value=0)
    num = st.number_input('Number of Recommendations', format="%i", value=0)
    if st.button('Get Recommendations'):
        user_idx = user_id - 1
        sorted_user_ratings = pivot_df.iloc[user_idx].sort_values(ascending=False)
        sorted_user_predictions = preds_df.iloc[user_idx].sort_values(ascending=False)
        sorted_user_ratings = pd.DataFrame(sorted_user_ratings)
        sorted_user_predictions = pd.DataFrame(sorted_user_predictions)
        sorted_user_ratings.rename(columns={user_idx: 'user_ratings'}, inplace=True)
        sorted_user_predictions.rename(columns={user_idx: 'user_predictions'}, inplace=True)
        temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
        # temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1).drop_duplicates()
        temp.index.name = 'Recommended Items'
        temp = temp.loc[temp.user_ratings == 0]
        temp = temp.sort_values('user_predictions', ascending=False)
        display = ('\nBelow are the recommended items for user(user_id = {}):\n'.format(user_id))
        display2 = (temp.head(num))
        st.write(display)
        st.write(display2)
