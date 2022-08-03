from collections import defaultdict
import collections
import imp
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from wordlist_app import get_wordlist


def wordcombos_dict(wordlist, length):
    wordcombos = defaultdict(list)
    for word in wordlist:
        for i in range(length):
            wordcombos[word[:i]+ "*" + word[i+1:]].append(word)
    return wordcombos

def possible_words_dict(wordlist, length):
    wordcombos = wordcombos_dict(wordlist, length)
    possible_words = defaultdict(list)
    for word in wordlist:
        for i in range(length):
            intermediate_word = word[:i] + "*" + word[i+1:]
            for w in wordcombos[intermediate_word]:
                if w is not word:
                    possible_words[word].append(w)
    return possible_words


def solver(wordlist, startword, endword):
    startword = startword.lower()
    endword = endword.lower()

    #Check if they are in the word list:
    startcheck = startword in wordlist
    endcheck = endword in wordlist

    if (startcheck == False):
        return ["Those are not words in the approved list.","Please try a different 5 letter word."]
    
    if (endcheck == False):
        return ["Those are not words in the approved list.","Please try a different 5 letter word."]

    length = len(startword)
    possible_words = possible_words_dict(wordlist, length)

    path_queue = collections.deque([startword])
    visited ={startword: True}
    
    first = True
    while path_queue:
        current_path = [path_queue.popleft()]
        if first == False:
            current_path = current_path[0]
        l = len(current_path)
        current_word = current_path[l-1]
        varations = possible_words[current_word]
        first = False
        for word in varations:
            if word not in visited:
                if word == endword:
                    final_path = current_path.copy()
                    final_path.append(word)
                    return final_path

                visited[word] = True
                new_path = current_path.copy()
                new_path.append(word)
                path_queue.append(new_path)


def enter_clicked(wordlist):
    startingword = startword.get()
    endingword = endword.get()
    response = solver(wordlist, startingword, endingword)

    length = str(len(response))
    response.insert(0," ")
    response.insert(0,f'This word ladder takes {length} steps.')

    
    showinfo(
        title='Answer',
        message="\n".join(response)
    )

wordlist = get_wordlist()

root =tk.Tk()
root.geometry("300x150")
root.resizable(False,False)
root.title("Enter two five letter words and see the word ladder!")

startword = tk.StringVar()
endword = tk.StringVar()

#Enter words frame
words_input = ttk.Frame(root)
words_input.pack(padx=10, pady=10, fill='x', expand=True)

#start word
startword_label = ttk.Label(words_input, text="Starting Word:")
startword_label.pack(fill='x', expand=True)

startword_entry = ttk.Entry(words_input, textvariable=startword)
startword_entry.pack(fill='x', expand=True)
startword_entry.focus()


#end word
endword_label = ttk.Label(words_input, text="Ending Word:")
endword_label.pack(fill='x', expand=True)

endword_entry = ttk.Entry(words_input, textvariable=endword)
endword_entry.pack(fill='x', expand=True)

#Enter button
enter_button = ttk.Button(words_input, text="Enter", command=lambda: enter_clicked(wordlist))
enter_button.pack(fill='x', expand=True, pady=10)

root.mainloop()











