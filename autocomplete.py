import tracemalloc
import time


# Implement TrieNode
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


# Implement a Trie with insert, search, and starts_with methods
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a word into the Trie
    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_word = True

    # Search if the word is in the Trie
    def search(self, prefix):
        current = self.root
        suggestions = []
        for char in prefix:
            if char not in current.children:
                return suggestions
            current = current.children[char]
        self.find_suggestions(current, prefix, suggestions)
        return suggestions

    # Recursively find all word suggestions with the given prefix
    def find_suggestions(self, current, prefix, suggestions):
        if current.is_word:
            suggestions.append(prefix)
        for char, node in current.children.items():
            self.find_suggestions(node, prefix + char, suggestions)


#  Load words from file
def load_words(filename):
    words = set()
    with open(filename, 'r') as f:
        for line in f:
            words.update(line.strip().split())
    return words


# Main function to load words and test the Trie
def main():
    words = load_words("words_alpha.txt")

    tracemalloc.start()
    st = time.time()

    trie = Trie()
    for word in words:
        trie.insert(word)

    et = time.time()
    elapsed_time = et - st
    print("Elapsed time: ", elapsed_time, 'seconds')
    print("Memory used: ", tracemalloc.get_traced_memory())
    # stopping the library
    tracemalloc.stop()

    # Test the Trie
    quit_flag = False
    while not quit_flag:
        user_input = input("Enter something: ")
        if user_input == "!":
            quit_flag = True
            continue
        suggestions = trie.search(user_input)
        print(suggestions)


if __name__ == "__main__":
    main()
