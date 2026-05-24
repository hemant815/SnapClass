from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource

def load_voiceEncoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):

    try:
        encoder = load_voiceEncoder()

        # audio,sample_rate = librosa(io.BytesIO(audio_bytes),sr=16000)
        audio, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()
    except Exception as e:
        st.error("voice recg eror")
        return None
    
def identify_speaker(new_embedding, candidate_dic,threshold=0.66):
    if new_embedding is None or not  candidate_dic:
        return None ,0.0
    best_sid = None
    best_score = 0.0

    for sid, store_embedding in candidate_dic.items():
        if store_embedding:
            similarity = np.dot(new_embedding, store_embedding)
            best_score = similarity
            best_sid = sid
        
    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score
def process_bulk(audio_bytes, candidates_dict, threshold=0.66):
    try:
        encoder = load_voiceEncoder()

        # audio, sr = librosa.load(io.BytesIO(),sr=16000)
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identify_result = {}

        for start, end in segments:
            if (end-start) < sr*0.5:
                continue

            segments_audio = audio[start:end]
            wav = preprocess_wav(segments_audio)

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict,threshold)


            if sid:
                if sid not in identify_result or score > identify_result[sid]:
                    identify_result[sid] = score 

        return identify_result
    
    except Exception as e:
        st.error('bulk processing error')
        return {}