def load_words(filename):
    words = []
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                words.append(word)
    return words

def find_matches(words, prefix):
    suggestions = []
    for word in words:
        if word.startswith(prefix):
            suggestions.append(word)
    return suggestions

# Main program
print('--- Simple Autocomplete ---')
print('Enter QP to quit.\n')

word_list = load_words('words.txt')

while True:
    prefix = input('Enter prefix: ')
    if prefix == 'QP':
        print('Thanks for using... :)')
        break

    matches = find_matches(word_list, prefix)
    if matches:
        print('Suggested words:')
        for word in matches:
            print(word)
    else:
        print('No match found...')
    print()