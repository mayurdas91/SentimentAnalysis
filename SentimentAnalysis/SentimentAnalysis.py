import tkinter as tk
from tkinter import scrolledtext, messagebox
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from gensim.summarization import summarize

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Function to analyze sentiment
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores

# Function to plot sentiment
def plot_sentiment(sentiment_scores):
    labels = ['Positive', 'Negative', 'Neutral', 'Compound']
    scores = [sentiment_scores['pos'], sentiment_scores['neg'], sentiment_scores['neu'], sentiment_scores['compound']]
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, scores, color=['green', 'red', 'blue', 'purple'])
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.show()

# Function to summarize text
def summarize_text(text):
    try:
        summary = summarize(text, ratio=0.2)
    except ValueError:
        summary = "Text is too short to summarize"
    return summary

# Function to determine overall sentiment
def determine_overall_sentiment(sentiment_scores):
    compound = sentiment_scores['compound']
    if compound >= 0.05:
        return "Overall sentiment is positive.", "green"
    elif compound <= -0.05:
        return "Overall sentiment is negative.", "red"
    else:
        return "Overall sentiment is neutral.", "blue"

# Function to handle the analysis button click
def analyze_blog():
    blog_text = text_area.get('1.0', tk.END).strip()
    
    if not blog_text:
        messagebox.showwarning("Input Error", "Please paste the blog text into the text box.")
        return
    
    # Analyze sentiment
    sentiment_scores = analyze_sentiment(blog_text)
    
    # Determine overall sentiment
    overall_sentiment, overall_color = determine_overall_sentiment(sentiment_scores)
    
    # Display sentiment scores with appropriate colors
    result_text.delete('1.0', tk.END)
    
    pos_text = f"Positive: {sentiment_scores['pos']:.2f}\n"
    neg_text = f"Negative: {sentiment_scores['neg']:.2f}\n"
    neu_text = f"Neutral: {sentiment_scores['neu']:.2f}\n"
    comp_text = f"Compound: {sentiment_scores['compound']:.2f}\n\n"
    
    result_text.insert(tk.END, pos_text, 'green' if sentiment_scores['pos'] > 0.1 else 'red')
    result_text.insert(tk.END, neg_text, 'red' if sentiment_scores['neg'] > 0.1 else 'green')
    result_text.insert(tk.END, neu_text, 'blue')
    result_text.insert(tk.END, comp_text, overall_color)
    result_text.insert(tk.END, overall_sentiment, overall_color)
    
    # Plot sentiment scores
    plot_sentiment(sentiment_scores)
    
    # Summarize text
    summary = summarize_text(blog_text)
    summary_text.delete('1.0', tk.END)
    summary_text.insert(tk.END, summary)

# Create main window
window = tk.Tk()
window.title("MD's Blog Sentiment Analyzer")

# Create and place text area for blog input
tk.Label(window, text="Paste your blog text below:").pack()
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20)
text_area.pack()

# Create and place result display area
tk.Label(window, text="Sentiment Analysis Result:").pack()
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10)
result_text.pack()

# Create and place summary display area
tk.Label(window, text="Summary:").pack()
summary_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10)
summary_text.pack()

# Create and place Analyze button
analyze_button = tk.Button(window, text="Analyze Blog", command=analyze_blog)
analyze_button.pack()

# Configure tags for colored text
result_text.tag_configure('green', foreground='green')
result_text.tag_configure('red', foreground='red')
result_text.tag_configure('blue', foreground='blue')

# Start the GUI event loop
window.mainloop()