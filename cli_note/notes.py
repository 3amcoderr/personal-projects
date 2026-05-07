import json
import os
import argparse
from datetime import datetime

FILE = "notes.json"

# step 1

def load_notes():
    if not os.path.exists(FILE):
        return []
    with open(FILE, 'r') as f:
        return json.load(f)
    


def save_notes(notes):
    with open(FILE, 'w') as f:
        json.dump(notes, f, indent= 2)



def add_note(text):
    notes = load_notes()
    notes.append({
        "text": text,
        "last_edited": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })
    save_notes(notes)
    print("Note added!")



def list_notes():
    notes = load_notes()
    for i, note in enumerate(notes, start = 1):
        print(f"{i} . {note['text']} ({note['last_edited']})")



def delete_note(index):
    notes = load_notes()
    try:
        removed = notes.pop(index - 1)
        save_notes(notes)
        print(f"deleted: {removed}")
    except:
        print("invalid note no. entered")



def edit_note(index, new_text):
    notes = load_notes()
    try:
        note = notes[index - 1]

        if isinstance(note, str):  
            notes[index - 1] = {
                "text": new_text,
                "last_edited": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        else:
            note["text"] = new_text
            note["last_edited"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        save_notes(notes)
        print("Note updated!")
    except IndexError:
        print("Invalid note number")




def search_notes(query):
    notes = load_notes()
    found = False 

    for i, note in enumerate(notes, start=1):
        text = note if isinstance(note, str) else note["text"]

        if query.lower() in text.lower():
            if isinstance(note, str):
                print(f"{i}. {text}")
            else:
                print(f"{i}. {text} (last edited: {note['last_edited']})")
            found = True 

    if not found:
        print("No matching notes found")


# step 2

def main():

    parser = argparse.ArgumentParser(description="A Simple note taking CLI")
    subparser = parser.add_subparsers(dest="command")

    #add
    add_parser = subparser.add_parser("add")
    add_parser.add_argument("text")


    # list
    subparser.add_parser("list")

    # update
    add_parser = subparser.add_parser("delete")
    add_parser.add_argument("index", type=int)

    # edit
    add_parser = subparser.add_parser("edit")
    add_parser.add_argument("index", type= int )
    add_parser.add_argument("text")

    # search
    search_parser = subparser.add_parser("search")
    search_parser.add_argument("query")
    

    args = parser.parse_args()

    if args.command == "add":
        add_note(args.text)
    elif args.command == "list":
        list_notes()
    elif args.command == "delete":
        delete_note(args.index)
    elif args.command == "edit":
        edit_note(args.index, args.text)
    elif args.command == "search":
        search_notes(args.query)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
