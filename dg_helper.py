from tkinter import *
import os
import json

def create_folder(folder):
    """Creates the given folder. Does not raise error if the folder already exists"""
    os.makedirs(folder,exist_ok=True)

images_path = os.path.join(".","images")
classes_images_path = os.path.join(images_path, "all_classes")
mutations_images_path = os.path.join(images_path, "all_mutations")
mutations_data_path = os.path.join(".", "mutations_data_brawl.json")
layouts_folder = os.path.join(".", "layouts")
create_folder(layouts_folder)

def layout_filename(classes_run, is_brawl):
    return "_".join(classes_run) + f"_{'brawl' if is_brawl else 'koth'}.json"

def full_layout_path(classes_run, is_brawl):
    return os.path.join(layouts_folder, layout_filename(classes_run, is_brawl))

all_classes = ["Newbies", "Tanks", "Fencers", "Tricksters", "Fighters", "Healers", "Throwers", "Shooters", "Cultists", "Mages", "Eggheads", "Summons"]
print(len(all_classes))

def import_mutations():
    with open(mutations_data_path, "r") as f:
        return json.loads(f.read())

ALL_MUTATIONS = import_mutations()

def stay_clicked_simple(button):
    def clicked_rec():
        if button["relief"] == "raised":
            button.configure(relief="sunken",bg="black")
        else:
            button.configure(relief="raised", bg="white")
    return clicked_rec

def stay_clicked(button, acm):
    def clicked_rec():
        button.click()
        acm.hide_or_show_floor_buttons()
    return clicked_rec

def show_hide_arrows(main_button, all_buttons):
    def sha():
        if main_button["relief"] == "raised":
            main_button.configure(relief="sunken", text="  Hide Arrows  ")
            for k,cbf in all_buttons.items():
                cbf.show_arrows()
        else:
            main_button.configure(relief="raised", text="Move Mutations")
            for k,cbf in all_buttons.items():
                cbf.hide_arrows()
    return sha

def move_button(i, button_list, is_left):
    def mb():
        swapi = i
        if is_left:
            swapi -= 1
        button_list[swapi],button_list[swapi+1] = button_list[swapi+1], button_list[swapi]
        button_list[swapi].grid(swapi, button_list)
        button_list[swapi].enable_disable_arrows(len(button_list)-1)
        button_list[swapi+1].grid(swapi+1, button_list)
        button_list[swapi+1].enable_disable_arrows(len(button_list)-1)
    return mb


class MutationButton():
    
    def __init__(self, col, row, name, floor, root, all_buttons, buttons_list):
        self.col = col
        self.row = row
        self.name = name
        self.floor = floor
        self.photo = PhotoImage(file = os.path.join(mutations_images_path, f"{name}.png"))
        self.frame = Frame(root,borderwidth=0)
        self.button = Button(self.frame, image=self.photo, borderwidth=10, state="disabled" if floor > 1 else "normal", padx=0, pady=0, command=stay_clicked(self, all_buttons))
        self.button.grid(column=0, row=0, columnspan=2, rowspan=2)
        self.left = Button(self.frame, text="<", padx=0, pady=0, command=move_button(self.col, buttons_list, True))
        self.right = Button(self.frame, text=">", padx=0, pady=0, command=move_button(self.col, buttons_list, False))
        """self.three = Button(self.frame, text="3", padx=0, pady=0)
        self.three.grid(column=2, row=0, sticky="ns")
        self.two = Button(self.frame, text="2", padx=0, pady=0)
        self.two.grid(column=2, row=1, sticky="ns")
        self.one = Button(self.frame, text="1", padx=0, pady=0)
        self.one.grid(column=2, row=2, sticky="ns")"""
        self.grid(self.col, buttons_list)

    def grid(self, new_col, buttons_list):
        self.col = new_col
        self.frame.grid(column=self.col, row=self.row)
        self.left.configure(command=move_button(self.col, buttons_list, True))
        self.right.configure(command=move_button(self.col, buttons_list, False))

    def enable_disable_arrows(self, max_col):
        self.left.configure(state="disabled" if self.col == 0 else "normal")
        self.right.configure(state="disabled" if self.col == max_col else "normal")

    def show_arrows(self):
        self.left.grid(column=0, row=2, sticky="we")
        self.right.grid(column=1, row=2, sticky="we")

    def hide_arrows(self):
        self.left.grid_forget()
        self.right.grid_forget()

    def hide_or_show_floor_buttons(self, nb_buttons_clicked):
        if (nb_buttons_clicked+3)//2 >= self.floor:
            self.button.configure(state="normal")
        else:
            if self.button["relief"] != "sunken":
                self.button.configure(state="disabled")

    def generate_mutation_data(self):
        return {"name":self.name, "Brawl Floor":self.floor}

    def raise_button(self):
        self.button.configure(relief="raised", bg="white")

    def sunken_button(self):
        self.button.configure(relief="sunken",bg="black")

    def is_sunken(self):
        return self.button["relief"] == "sunken"

    def click(self):
        if self.is_sunken():
            self.raise_button()
        else:
            self.sunken_button()

class ClassButtonsFrame():

    def __init__(self, frame, unique=[], rare=[], common=[]):
        self.unique = []
        self.rare = []
        self.common = []
        self.frame = frame

    def add_mutation(self, mutation, all_buttons):
        if len(mutation["classes"]) == 10:
            self.add_common(mutation, all_buttons)
        elif len(mutation["classes"]) <= 1:
            self.add_unique(mutation, all_buttons)
        else:
            self.add_rare(mutation, all_buttons)

    def add_list(self, mutation, all_buttons, added_list, row):
        added_list.append(MutationButton(len(added_list), row, mutation["name"], mutation["Brawl Floor"], self.frame, all_buttons, added_list))
    def add_unique(self, mutation, all_buttons):
        self.add_list(mutation, all_buttons, self.unique, 0)
    def add_rare(self, mutation, all_buttons):
        self.add_list(mutation, all_buttons, self.rare, 1)
    def add_common(self, mutation, all_buttons):
        self.add_list(mutation, all_buttons, self.common, 2)

    def get_all_buttons(self):
        return self.unique+self.rare+self.common
        
    def show_arrows(self):
        for button_list in [self.unique, self.rare, self.common]:
            for button in button_list:
                button.show_arrows()
                button.enable_disable_arrows(len(button_list)-1)

    def hide_arrows(self):
        for button in self.get_all_buttons():
            button.hide_arrows()

    def generate_save_data(self):
        return {"unique":[m.generate_mutation_data() for m in self.unique],
                "rare":[m.generate_mutation_data() for m in self.rare],
                "common":[m.generate_mutation_data() for m in self.common]}

    def raise_buttons(self):
        for button in self.get_all_buttons():
            button.raise_button()

    def nb_buttons_clicked(self):
        return sum(b.is_sunken() for b in self.get_all_buttons())

    def hide_or_show_floor_buttons(self, nb_buttons_clicked):
        for b in self.get_all_buttons():
            b.hide_or_show_floor_buttons(nb_buttons_clicked)

class AllClassesMutations():

    def __init__(self, root, row_offset, classes_run):
        self.root = root
        self.row_offset = row_offset
        self.classes_run = classes_run
        if os.path.exists(full_layout_path(classes_run, True)):
            with open(full_layout_path(classes_run, True), "r") as f:
                layout = json.loads(f.read())
            self.load_layout(layout)
        else:
            print("does_not_exist")
            self.base_layout()

    def load_layout(self, layout):
        self.classes_logos = []
        self.buttons_frames = {}
        for class_id in range(len(layout)):
            class_name = layout[class_id][0]
            class_layout = layout[class_id][1]
            self.classes_logos.append(PhotoImage(file=os.path.join(classes_images_path, f"{class_name}.png")).zoom(2,2))
            class_logo = Label(self.root, image=self.classes_logos[-1])
            class_logo.grid(column=0,row=class_id+1+self.row_offset)
            class_frame = Frame(self.root,relief="ridge", borderwidth=5)
            class_frame.grid(column=1, row=class_id+1+self.row_offset, sticky="w")
            self.buttons_frames[class_name] = ClassButtonsFrame(class_frame)
            for mut in class_layout["unique"]:
                self.buttons_frames[class_name].add_unique(mut, self)
            for mut in class_layout["rare"]:
                self.buttons_frames[class_name].add_rare(mut, self)
            for mut in class_layout["common"]:
                self.buttons_frames[class_name].add_common(mut, self)

    def base_layout(self):
        self.buttons_frames = {}
        self.classes_logos = []
        self.classes_logos.append(PhotoImage(file=os.path.join(classes_images_path, f"Newbies.png")).zoom(2,2))
        text = Label(self.root, image=self.classes_logos[0])
        text.grid(column=0,row=self.row_offset)
        neutral_frame = Frame(self.root, relief="ridge", borderwidth=5)
        neutral_frame.grid(column=1, row=self.row_offset, sticky="w")
        self.buttons_frames["Neutral"] = ClassButtonsFrame(neutral_frame)
        for mut in ALL_MUTATIONS:
            if mut["is_neutral"]:
                self.buttons_frames["Neutral"].add_mutation(mut, self)
    
        for class_id in range(len(self.classes_run)):
            self.classes_logos.append(PhotoImage(file=os.path.join(classes_images_path, f"{self.classes_run[class_id]}.png")).zoom(2,2))
            class_logo = Label(self.root, image=self.classes_logos[-1])
            class_logo.grid(column=0,row=class_id+1+self.row_offset)
            class_frame = Frame(self.root,relief="ridge", borderwidth=5)
            class_frame.grid(column=1, row=class_id+1+self.row_offset, sticky="w")
            self.buttons_frames[self.classes_run[class_id]] = ClassButtonsFrame(class_frame)
            for mut in ALL_MUTATIONS:
                if self.classes_run[class_id] in mut["classes"]:
                    self.buttons_frames[self.classes_run[class_id]].add_mutation(mut, self)

    def raise_all_buttons(self):
        for k, cbf in self.buttons_frames.items():
            cbf.raise_buttons()
        self.hide_or_show_floor_buttons()

            
    def hide_or_show_floor_buttons(self):
        nb_buttons_clicked = sum(cbf.nb_buttons_clicked() for k,cbf in self.buttons_frames.items())
        for _,cbf in self.buttons_frames.items():
            cbf.hide_or_show_floor_buttons(nb_buttons_clicked)

    def save_layout(self):
        res = []
        for class_run in ["Neutral"]+self.classes_run:
            res.append((class_run, self.buttons_frames[class_run].generate_save_data()))
        with open(full_layout_path(self.classes_run, True), "w") as f:
            f.write(json.dumps(res))
    
            
def generate_buttons(classes_run, root):

    acm = AllClassesMutations(root, 1, classes_run)
    
    settings_frame = Frame(root,relief="ridge", borderwidth=5)
    settings_frame.grid(column=0, columnspan=2, row=0, sticky="we")
    show_arrows_button = Button(settings_frame, text="Move Mutations")
    show_arrows_button.configure(command=show_hide_arrows(show_arrows_button, acm.buttons_frames))
    show_arrows_button.grid(column=0, row=0)
    save_layout_button = Button(settings_frame, text="Save Layout", command=acm.save_layout)
    save_layout_button.grid(column=1, row=0)
    reset_run_button = Button(settings_frame, text="Reset Run", command=acm.raise_all_buttons)
    reset_run_button.grid(column=2, row=0)
    return acm
    
    
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
        btn.configure(command=stay_clicked_simple(btn))
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
