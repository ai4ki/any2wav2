import os
import streamlit as st

# Global Streamlit settings
st.set_page_config(page_title="AnyToWave")

with open("./css/style_purple.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
        <style>
            [data-testid="stHeader"]::before {
                content: "ai4ki";
                font-family: Arial, sans-serif;
                font-weight: bold;
                font-size: 40px;
                color: #3b1f82;
                position: relative;
                left: 30px;
                top: 10px;
            }
        </style>
        """,
    unsafe_allow_html=True,
)


def save_uploaded_file(uploaded_file):
    try:
        with open(uploaded_file.name, 'wb') as f_audio:
            f_audio.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


st.markdown("### Lade eine Audiodatei hoch:")
audiofile = st.file_uploader(label="Lade eine Audiodatei hoch:",
                             type=['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'webm', 'wma'],
                             label_visibility="collapsed")
st.markdown("")
convert = st.button("Audiodatei konvertieren")

if convert:
    if audiofile is not None:
        audiofile_name = os.path.splitext(audiofile.name)[0]
        if save_uploaded_file(audiofile):
            wave_filename = f"{audiofile_name}.wav"
            os.system(f'ffmpeg -i "{audiofile.name}" -ar 16000 -ac 1 -c:a pcm_s16le "{wave_filename}"')

            with open(wave_filename, "rb") as wav:
                st.download_button(label="Wave-Datei herunterladen",
                                   data=wav,
                                   file_name=wave_filename)

            os.remove(wave_filename)
            os.remove(audiofile.name)
        else:
            st.warning(f"Beim Upload ist etwas schief gegangen -- versuche es noch einmal!")
