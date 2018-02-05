# Semantic-Search-Application
Implemented a semantic search application that will produce improved results using NLP features and techniques. It includes a keyword-based strategy and an improved strategy using NLP feature and techniques. The following are the tasks that are performed:

Task 1: Creating a corpus of News articles. Corpus contains at least:
    a. 1,000 articles
    b. 100,000 words
Here the corpus is taken from http://www.nltk.org/nltk_data/

Task 2: Implement a shallow NLP pipeline to perform the following:
  a. Keyword search index creation
       Segment the News articles into sentences
       Tokenize the sentences into words
       Index the word vector per sentence into search index such as Lucene or SOLR
  b. Natural language query parsing and search
       Segment an user’s input natural language query into sentences
       Tokenize the sentences into words
       Run a search/match with the search query word vector against the sentence word vector (present in the Lucene/SOLR search index) created from the corpus
   c. Evaluate the results of at least 10 search queries for the top-10 returned sentence matches

Task 3: Implement a deeper NLP pipeline to perform the following:
  a. Semantic search index creation
       Segment the News articles into sentences
       Tokenize the sentences into words
       Lemmatize the words to extract lemmas as features
       Stem the words to extract stemmed words as features
       Part-of-speech (POS) tag the words to extract POS tag features
       Syntactically parse the sentence and extract phrases, head words, OR dependency parse relations as features
       Using WordNet, extract hypernymns, hyponyms, meronyms, AND holonyms as features
       Index the various NLP features as separate search fields in a search index such as Lucene or SOLR
  b. Natural language query parsing and search
       Run the above described deeper NLP on an user’s input natural language and extract search query features
       Run a search/match against the separate or combination of search index fields created from the corpus
  c. Evaluate the results of at least 10 search queries for the top-10 returned sentence matches

Note: you are free to implement or use a third-party tool such as:
1. NLTK: http://www.nltk.org/
2. Stanford NLP: http://nlp.stanford.edu/software/corenlp.shtml
3. Apache OpenNLP: http://opennlp.apache.org/

Task 4: Improve the shallow NLP pipeline results using a combination of deeper NLP pipeline features
