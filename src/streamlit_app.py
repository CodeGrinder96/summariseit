import asyncio

import streamlit as st
from utils.summariser_utils import Summariser
from utils.youtube_utils import YoutubeVideo


def configure_page() -> None:
    st.set_page_config(page_title='Podcast Summariser')
    

def configure_overview() -> None:
    st.title('Podcast Summariser')
    

def configure_summarisation_functionality() -> None:
    url = st.text_input('Enter podcast link (Youtube only)')
    
    if url and 'youtube' in url:
        youtube_video = YoutubeVideo(url=url)
        if youtube_video.is_valid:
            video_id = youtube_video.id
            st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)
            
            language = st.selectbox(
                label='Select desired language',
                options=('English', 'Dutch', 'French', 'German', 'Vietnamese'),
                index=None,
                placeholder="Select desired language ...",
                label_visibility='hidden'
            )
            
            if st.button('Get key takeaways', use_container_width=True):
                transcript = youtube_video.get_transcript()
                summariser = Summariser()
                summary = asyncio.run(summariser.get_summary_async(transcript, language))
                st.write(summary)
        else:
            st.error('Please enter a valid url')
    elif url and 'youtube'not in url:
        st.warning('We currently only support Youtube')
    else:
        st.warning('Please enter a link')
        
    
if __name__ == '__main__':
    configure_page()
    configure_overview()
    configure_summarisation_functionality()