import itertools
import time

# Define Leet Speak substitutions with multiple variations
leet_substitutions = {
    'a': ['4', '@'],
    'e': ['3', '€'],
    'i': ['1', '!', '|'],
    'l': ['1', '|'],
    'o': ['0'],
    's': ['5', '$'],
    'z': ['2'],
    't': ['7']
}

default_fix = ['!', '.']

def generate_wordlist(words):
    wordlist = list(words)
    for idx, word in enumerate(itertools.permutations(words)):
        joined_word = ''.join(word)
        wordlist.append(joined_word)
    return wordlist

def generate_wordlist_with_leet(words):
    wordlist = list(words)
    for word in words:
        modified_words = set()  # To store unique modified words for each original word
        for l in range(1, len(word)):
            for subset in itertools.combinations(range(len(word)), l):
                for substitutions in itertools.product(*[leet_substitutions.get(word[i].lower(), [word[i]]) for i in subset]):
                    temp_word = list(word)
                    for i, substitution in zip(subset, substitutions):
                        temp_word[i] = substitution
                    modified_words.add("".join(temp_word))
        wordlist.extend(modified_words)  # Extend the wordlist with unique modified words
    return wordlist
    
    
def generate_wordlist_with_uppercase(words):
    wordlist = list(words)
    combinations_count = sum(len(list(itertools.combinations(range(len(word)), l))) for word in words for l in range(1, len(word)))
    print("Generating wordlist with uppercase... This may take a moment.")
    start_time = time.time()
    idx = 0
    for word in words:
        modified_words = set()  # To store unique modified words for each original word
        for l in range(1, len(word)):
            for subset in itertools.combinations(range(len(word)), l):
                idx += 1
                progress = idx / combinations_count * 100
                elapsed_time = time.time() - start_time
                time_remaining = (elapsed_time / idx) * (combinations_count - idx)
                print(f"Progress: {progress:.2f}%  Estimated time remaining: {time_remaining:.2f} seconds", end='\r')
                for uppercases in itertools.product(*[(char.upper(), char.lower()) if char.isalpha() else (char,) for char in word]):
                    temp_word = [uppercases[i] if i in subset else char for i, char in enumerate(word)]
                    modified_words.add("".join(temp_word))
        # Add a modified version of the word with all characters uppercase
        modified_words.add(word.upper())
        wordlist.extend(modified_words)  # Extend the wordlist with unique modified words
    print("\nWordlist with uppercase generation complete!")
    return wordlist
    
def generate_wordlist_with_appendix(wordlist, fix, choice):
    modified_wordlist = set()
    if choice == "p":
        for word in wordlist:
            for append in fix:
                modified_wordlist.add(append + word)
    elif choice == "s":
        for word in wordlist:
            for append in fix:
                modified_wordlist.add(word + append)
    elif choice == "b":
        for word in wordlist:
            for append in fix:
                modified_wordlist.add(word + append)
                modified_wordlist.add(append + word)
    
    return modified_wordlist
    
def save_wordlist(wordlist, filename):
    with open(filename, 'w') as file:
        for word in wordlist:
            file.write(word + '\n')
    print("Wordlist saved successfully!")

def main():
    print("\nWelcome to the Wordlist Generator!")
    while True:
        print("Choose an option:")
        print("1. Merge two or more txt wordlist files into one")
        print("2. Create a new wordlist")
        print("3. Exit")
    
        choice = input("\nEnter the number of the option you want to select: ")

        if choice == '1':
            merge_wordlists()
        elif choice == '2':
            create_wordlist()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.")

def merge_wordlists():
    # Get input filenames
    filenames = input("Enter the filenames of the wordlist files you want to merge (separated by space): ").split()
    final_wordlist = set()

    # Read wordlists from files and merge them
    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                words = file.read().split()
                final_wordlist.update(words)
        except FileNotFoundError:
            print(f"File '{filename}' not found. Skipping...")

    # Save the merged wordlist to a file
    filename = input("Enter the filename for the merged wordlist: ")
    save_wordlist(final_wordlist, filename)

def create_wordlist():
    # Get words from user input
    words = input("Enter words (separated by space): ").lower().split()

    # Menu for choosing wordlist generation options
    print("\nChoose which types of wordlists to generate:")
    print("1. Generate wordlist with permutations of entered words (join words)")
    print("2. Generate wordlist with Leet Speak")
    print("3. Generate wordlist with uppercase variations")
    print("4. Generate wordlist with prefix and/or suffix")
    print("5. Back to main menu")
    
    # Get user choices
    choice = input("\nEnter the numbers of the options you want to apply (separated by space): ").split()
    
    if '5' in choice:
        return
    
    fix = set()
    prefix_suffix_choice = ''
    if '4' in choice:
        prefix_suffix_choice = input("Do you want to use prefix (p), suffix (s), or both (b)? ").lower()      
        default = input(f"Do you want to use default list {default_fix} for prefix/suffix (y/n)?")
        if default != "y":
            fix.update(input("Enter words or characters for prefix/suffix (separated by space): ").split())
        else:
            fix.update(default_fix)
            
    filename = input("Enter the filename for the generated wordlist: ")

    # Check user choices and generate corresponding wordlists
    final_wordlist = set(words)
    if '1' in choice:
        final_wordlist.update(generate_wordlist(final_wordlist))
    if '2' in choice:
        final_wordlist.update(generate_wordlist_with_leet(final_wordlist))
    if '3' in choice:
        final_wordlist.update(generate_wordlist_with_uppercase(final_wordlist))
    if '4' in choice:
        final_wordlist.update(generate_wordlist_with_appendix(final_wordlist, fix, prefix_suffix_choice))

    # Convert set to list and sorting
    final_wordlist = list(final_wordlist)
    final_wordlist.sort()
    # Save final wordlist to a file
    save_wordlist(final_wordlist, filename)


if __name__ == "__main__":
    main()
