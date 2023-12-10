from transformers import pipeline

sentimentclassifier = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")

def sentiment_analysis(text):
    return sentimentclassifier(text)