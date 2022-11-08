from tkinter import *
import os
import json

images_path = os.path.join(".","images")
classes_images_path = os.path.join(images_path, "all_classes")
mutations_images_path = os.path.join(images_path, "all_mutations")
mutations_data_path = os.path.join(".", "mutations_data.json")

all_classes = ["Newbies", "Tanks", "Fencers", "Tricksters", "Fighters", "Healers", "Throwers", "Shooters", "Cultists", "Mages", "Eggheads", "Summons"]
print(len(all_classes))

def import_mutations():
    with open(mutations_data_path, "r") as f:
        return json.loads(f.read())

ALL_MUTATIONS = import_mutations()

def stay_clicked(button, button_list):
    def clicked_rec():
        if button["relief"] == "raised":
            button.configure(relief="sunken",bg="black")
        else:
            button.configure(relief="raised",bg="white")
        nb_buttons_clicked = sum(b.button["relief"] == "sunken" for b in button_list)
        for b in button_list:
            b.activate_or_not(nb_buttons_clicked)
    return clicked_rec
    

class MutationButton():
    
    def __init__(self, col, row, name, floor, root, button_list):
        self.col = col
        self.row = row
        self.floor = floor
        self.photo = PhotoImage(file = os.path.join(mutations_images_path, f"{name}.png"))
        self.button = Button(root, image=self.photo, borderwidth=10, padx=10, pady=10, state="disabled" if floor > 1 else "normal")
        self.button.configure(command=stay_clicked(self.button, button_list))
        self.grid()

    def grid(self):
        self.button.grid(column=self.col, row=self.row)

    def activate_or_not(self, nb_buttons_clicked):
        if (nb_buttons_clicked+3)//2 >= self.floor:
            self.button.configure(state="normal")
        else:
            self.button.configure(state="disabled")

def generate_buttons(classes_run, root):
    mutations_buttons = []
    classes_logos = []
    classes_logos.append(PhotoImage(file=os.path.join(classes_images_path, f"Newbies.png")).zoom(2,2))
    text = Label(root, image=classes_logos[0])
    text.grid(column=0,row=0)
    neutral_frame = Frame(root, relief="ridge", borderwidth=5)
    neutral_frame.grid(column=1, row=0, sticky="w")
    col = 0
    for mut in ALL_MUTATIONS:
        if mut["is_neutral"]:
            mutations_buttons.append(MutationButton(col, 0, mut["name"], mut["Brawl Floor"], neutral_frame, mutations_buttons))
            col += 1
    
    classes_frames = []
    for class_id in range(len(classes_run)):
        classes_logos.append(PhotoImage(file=os.path.join(classes_images_path, f"{classes_run[class_id]}.png")).zoom(2,2))
        class_logo = Label(root, image=classes_logos[-1])
        class_logo.grid(column=0,row=class_id+1)
        classes_frames.append(Frame(root,relief="ridge", borderwidth=5))
        classes_frames[-1].grid(column=1, row=class_id+1, sticky="w")
        unique_cpt = -1
        rare_cpt = -1
        common_cpt = -1
        for mut in ALL_MUTATIONS:
            if classes_run[class_id] in mut["classes"]:
                if len(mut["classes"]) == 10:
                    row = 2
                    common_cpt += 1
                    col = common_cpt
                elif len(mut["classes"]) == 1:
                    row = 0
                    unique_cpt += 1
                    col = unique_cpt
                else:
                    row = 1
                    rare_cpt += 1
                    col = rare_cpt
                mutations_buttons.append(MutationButton(col, row, mut["name"], mut["Brawl Floor"], classes_frames[-1], mutations_buttons))
    return mutations_buttons, classes_logos
    
    
def get_classes_run(continuation):
    
    # Create window
    root = Tk()
    root.title("Classes Selector")
    #root.geometry('528x200')

    # create buttons for classes
    buttons = []
    photos = []
    for i in range(len(all_classes)):
        photo = PhotoImage(file = os.path.join(classes_images_path, f"{all_classes[i]}.png")).zoom(2,2)
        photos.append(photo)
        btn = Button(root, image=photo, borderwidth=5)
        btn.configure(command=stay_clicked(btn,[]))
        btn.grid(column=i, row=1)
        buttons.append(btn)

    opening_message = Label(root, text="Choose the classes you want to run")
    opening_message.grid(column=0,row=0,columnspan=len(all_classes))

    # Destroy current window and run continuation function
    def launch():
        classes_run = []
        for i in range(len(buttons)):
            if buttons[i]["relief"] == "sunken":
                classes_run.append(all_classes[i])
        root.destroy()
        continuation(classes_run)
    
    run_button = Button(root, text="Launch Helper", command=launch)
    run_button.grid(column=0, row=2, columnspan=len(all_classes))
    
    root.mainloop()

def do_run(classes_run):
    print(classes_run)
    root = Tk()
    root.title("Despot's Game Brawl Mutation Helper")
    #root.geometry('700x500')

    mutation_buttons = generate_buttons(classes_run, root)
    
    root.mainloop()

#do_run(["Tricksters", "Mages"])

get_classes_run(do_run)
