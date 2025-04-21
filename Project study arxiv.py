import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from gensim.models import Word2Vec
import numpy as np

class ArxivCrawler:
    def __init__(self, query):
        self.query = query
        self.url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
        #A LLM used for question and answers
        self.model_name = "distilbert-base-cased-distilled-squad"
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.abstracts = self.crawl_arxiv()
        self.word2vec_model = self.train_word2vec_model()

    def train_word2vec_model(self):
        sentences = [abstract.split() for abstract in self.abstracts]
        model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)
        return model

    def crawl_arxiv(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("p", class_="title is-5 mathjax")
        abstracts = []
        for link in links:
            abstract = link.find_next("span", class_="abstract-full has-text-grey-dark mathjax")
            if abstract:
                abstracts.append(abstract.text.strip())
        return abstracts

    def get_embedding(self, word):
        try:
            return self.word2vec_model.wv[word]
        except KeyError:
            return np.zeros(100)

    def get_similarity(self, question, abstract):
        question_embedding = np.mean([self.get_embedding(word) for word in question.split()], axis=0)
        abstract_embedding = np.mean([self.get_embedding(word) for word in abstract.split()], axis=0)
        return np.dot(question_embedding, abstract_embedding) / (np.linalg.norm(question_embedding) * np.linalg.norm(abstract_embedding))

    def get_answer(self, question, context):
        return context

    def search_abstracts(self, question):
        best_answer = ""
        best_similarity = 0
        for abstract in self.abstracts:
            similarity = self.get_similarity(question, abstract)
            if similarity > best_similarity and similarity > 0.5: # threshold for similarity
                best_similarity = similarity
                best_answer = abstract
        return best_answer

crawler = ArxivCrawler("longevity")
question = "🤔 What are the factors that influence longevity?"
answer = crawler.search_abstracts(question)
print(question)
print(f"💡 {answer}")