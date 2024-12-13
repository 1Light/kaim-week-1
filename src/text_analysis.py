from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora
from gensim.models import LdaModel
import pandas as pd
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
nltk.download('stopwords')
print("Stopwords downloaded.")

def perform_sentiment_analysis(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Initialize VADER Sentiment Analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Step 1: Perform sentiment analysis on the headlines
    df['sentiment_score'] = df['headline'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

    # Step 2: Classify sentiment as Positive, Negative, or Neutral
    df['sentiment'] = df['sentiment_score'].apply(
        lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
    )

    # Step 3: Count the occurrences of each sentiment
    sentiment_counts = df['sentiment'].value_counts()

    # Print out the sentiment counts
    print("Sentiment Analysis Results:")
    print(sentiment_counts)

    # Create the 'results/text_analysis' folder if it doesn't exist
    os.makedirs('results/text_analysis', exist_ok=True)

    # Create a plot to visualize sentiment distribution
    sentiment_counts.plot(kind='bar', title='Sentiment Distribution', color=['green', 'red', 'blue'])
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot as an image in the 'results/text_analysis' folder
    plt.savefig('results/text_analysis/sentiment_distribution.png', dpi=300)
    plt.close()  # Close the plot to free up memory

def perform_topic_modeling(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    print("file is here")

    # Ensure there are no missing values in the 'headline' column
    df.dropna(subset=['headline'], inplace=True)

    # Preprocess the headlines
    stop_words = set(stopwords.words('english'))
    print("gonna start cleaning")
    df['cleaned_headlines'] = df['headline'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    print("cleaned")

    # Tokenize and create a dictionary of words
    tokenized_headlines = [headline.split() for headline in df['cleaned_headlines']]
    print("tokenized")
    dictionary = corpora.Dictionary(tokenized_headlines)

    # Create a bag of words (bow)
    print("creating bows")
    bow_corpus = [dictionary.doc2bow(headline) for headline in tokenized_headlines]
    print("creating LDA model")

    # Create the LDA model (you can tune the number of topics)
    lda = LdaModel(bow_corpus, num_topics=3, id2word=dictionary, passes=15)
    print("created LDA model")

    # Print topics
    print("Topic Modeling Results:")
    topics = lda.print_topics(num_words=5)
    for topic in topics:
        print(topic)

    # Plotting the topics (simple word cloud-like visualization)
    topic_words = [topic[1].split(' + ') for topic in topics]
    topic_words_flat = [word.split('*')[1].strip().strip('"') for sublist in topic_words for word in sublist]

    # Count frequency of each word across all topics for visualization
    vectorizer = CountVectorizer(stop_words='english')
    word_count_matrix = vectorizer.fit_transform(topic_words_flat)
    word_count = word_count_matrix.sum(axis=0).A1
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_count))

    # Plotting the word frequencies
    plt.figure(figsize=(10, 6))
    plt.bar(word_freq.keys(), word_freq.values(), color='blue')
    plt.xticks(rotation=90)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Word Frequency in LDA Topics')
    plt.tight_layout()

    # Save the plot as an image in the 'results/text_analysis' folder
    os.makedirs('results/text_analysis', exist_ok=True)
    plt.savefig('results/text_analysis/topic_modeling_word_freq.png', dpi=300)

# Define the file path
file_path = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')

# Call the function to perform topic modeling
perform_sentiment_analysis(file_path)