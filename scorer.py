
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

dataset = pd.read_csv("data/UpdatedResumeDataSet.csv")

def get_ats_score(resume_text):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([resume_text] + dataset["Resume"].tolist())
    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    score = round(similarity.max() * 100, 2)
    return score

def rank_resume(resume_text):
    score = get_ats_score(resume_text)
    if score > 90:
        return "Top 5"
    elif score > 85:
        return "Top 10"
    elif score > 75:
        return "Top 20"
    elif score > 65:
        return "Top 25"
    elif score > 50:
        return "Top 50"
    elif score > 40:
        return "Top 60"
    elif score > 30:
        return "Top 80"
    else:
        return "Below Average"
