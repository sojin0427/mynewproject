import streamlit as st
image=[
    'https://www.youtube.com/watch?v=MP8R6kBykzE'
    ]
urls = [

        'https://www.youtube.com/watch?v=KR8ddnPjCtk', 

        'https://www.youtube.com/watch?v=CgSvahZkJmc', 

        'https://www.youtube.com/watch?v=CgSvahZkJmc'

    ]
st.title('This is my first webapp')
con1, con2 = st.columns((4,1))
with con1:
   with st.expander('Content....'):
        for i in range(len(urls)):
            st.video(urls[0])
        pass
with con2:
    with st.expander('Tips...'):
        st.image(image[0])
        pass

con3, con4 = st.columns((4,1))

with con3:

    with st.expander('Content....'):

        import pandas as pd

        df = pd.read_csv('./data.csv')

        st.write(df)

with con4:

    with st.expander('Tips...'):
        with open('./ml.txt', 'r', encoding='UTF-8') as f:
            mltxt = f.read()
            st.markdown(mltxt)

        st.image(image[0])

        pass