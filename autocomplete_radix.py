import tracemalloc
import time


class RadixNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class RadixTree:
    def __init__(self):
        self.root = RadixNode()

    # Insert a word into the Radix Tree
    def insert(self, word):
        current = self.root
        while word:
            for key in current.children:
                common_prefix = self.find_common_prefix(key, word)
                # If there is a common prefix between the current child key and word
                if common_prefix:
                    # If the common prefix matches the entire key, move to the child node and remove common prefix from word
                    if common_prefix == key:
                        current = current.children[key]
                        word = word[len(common_prefix):]
                        break
                    # If the common prefix is a partial match, split the node into two nodes
                    else:
                        # Get the remaining part of key and word after the common prefix
                        remaining_key = key[len(common_prefix):]
                        remaining_word = word[len(common_prefix):]
                        # Reassign the remaining key to a new node
                        current.children[common_prefix] = RadixNode()
                        current.children[common_prefix].children[remaining_key] = current.children.pop(key)
                        # If there is a remaining word, create a new node for it and mark it as a word
                        if remaining_word:
                            current.children[common_prefix].children[remaining_word] = RadixNode()
                            current.children[common_prefix].children[remaining_word].is_word = True
                        # If there is no remaining word, mark it as a word
                        else:
                            current.children[common_prefix].is_word = True
                        return
            else:
                current.children[word] = RadixNode()
                current.children[word].is_word = True
                return

    # Search if the word is in the Radix Tree
    def search(self, prefix):
        current = self.root
        suggestions = []
        searched_prefix = ""
        while prefix:
            for key in current.children:
                common_prefix = self.find_common_prefix(key, prefix)
                if common_prefix:
                    # If common prefix matches the entire key, move to the child node and remove common prefix from prefix
                    if common_prefix == key:
                        current = current.children[key]
                        searched_prefix += key
                        prefix = prefix[len(common_prefix):]
                        break
                    # If the common prefix matches the entire prefix, find suggestions starting from the child node
                    elif common_prefix == prefix:
                        self.find_suggestions(current.children[key], searched_prefix, key, suggestions)
                        return suggestions
            else:
                return suggestions
        self.find_suggestions(current, searched_prefix, prefix, suggestions)
        return suggestions

    def find_suggestions(self, current, searched_prefix, prefix, suggestions):
        if current.is_word:
            suggestions.append(searched_prefix + prefix)
        for key, node in current.children.items():
            self.find_suggestions(node, searched_prefix, prefix + key, suggestions)

    # Find common prefix between two strings
    def find_common_prefix(self, s1, s2):
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]:
                return s1[:i]
        return s1[:min_len]


# Load words from file
def load_words(filename):
    words = set()
    with open(filename, 'r') as f:
        for line in f:
            words.update(line.strip().split())
    return words


def print_tree(node, level=0):
    for key, child in node.children.items():
        print("\t" * level + key)
        print_tree(child, level + 1)


# Main function to load words and test the Radix Tree
def main():
    words = load_words("words_alpha.txt")

    tracemalloc.start()
    st = time.time()

    radix_tree = RadixTree()
    for word in words:
        radix_tree.insert(word)

    et = time.time()
    elapsed_time = et - st
    print("Elapsed time: ", elapsed_time, 'seconds')
    print("Memory used: ", tracemalloc.get_traced_memory())
    # stopping the library
    tracemalloc.stop()

    # Test the Radix Tree
    quit_flag = False
    while not quit_flag:
        user_input = input("Enter something: ")
        if user_input == "!":
            quit_flag = True
            continue
        suggestions = radix_tree.search(user_input)
        print(suggestions)


if __name__ == "__main__":
    main()
