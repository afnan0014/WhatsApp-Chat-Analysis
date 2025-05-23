import streamlit as st
import preprocces,help
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocces.preprocess(data)
    st.dataframe(df)
    


    # fetch unique userss
    users_list = df['users'].unique().tolist()
    
    users_list.sort()
    users_list.insert(0,"Overall")

    selected_users = st.sidebar.selectbox("Show analysis ",users_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = help.fetch_stats(selected_users,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = help.monthly_timeline(selected_users,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = help.daily_timeline(selected_users, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = help.week_activity_map(selected_users,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = help.month_activity_map(selected_users, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        users_heatmap = help.activity_heatmap(selected_users,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(users_heatmap)
        st.pyplot(fig)

        # finding the busiest userss in the group(Group level)
        if selected_users == 'Overall':
            st.title('Most Busy Userss')
            x,new_df = help.most_busy_userss(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = help.create_wordcloud(selected_users,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

       # most common words
        most_common_df = help.most_common_words(selected_users, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df['Word'], most_common_df['Count'])
        plt.xticks(rotation='vertical')

        st.title('Most common words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = help.emoji_helper(selected_users,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)










