import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    len_corpus = len(corpus)
    dist = {}
    for unit in corpus:
        dist[unit] = 0
    if len(corpus[page]) == 0:
        for unit in dist:
            dist[unit] = 1/len_corpus

    else:
        for unit in corpus[page]:
            dist[unit] = damping_factor/len(corpus[page])
        for unit in dist:
            dist[unit] += (1-damping_factor)/len_corpus

    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    dist = {}
    for unit in corpus:
        dist[unit] = 0

    for i in range(n):
        if i == 0:
            page = random.choice(list(corpus))
        else:
            dist = transition_model(corpus, page, damping_factor)
            page = random.choices(list(dist), weights=list(dist.values()))[0]
        dist[page] += 1/n

    return dist


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dist = {}
    for unit in corpus:
        dist[unit] = 1/len(corpus)
    
    while True:
        new_dist = {}
        for unit in corpus:
            new_dist[unit] = (1-damping_factor)/len(corpus)
            for page in corpus:
                if unit in corpus[page]:
                    new_dist[unit] += damping_factor*dist[page]/len(corpus[page])
        if all(abs(new_dist[unit] - dist[unit]) < 0.001 for unit in corpus):
            break
        dist = new_dist
    return dist




if __name__ == "__main__":
    main()


print(f"PageRank Results from Sampling (n = {SAMPLES})")
