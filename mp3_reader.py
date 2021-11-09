import sys
import os
import json
import time
from pygame import mixer

class mp3_reader:
    """
    Imagine you have a folder with audio files and you want to label them as noisy / clean.
    You need to write a script that will play the mp3 file one by one, after playing each file
    wait for user input - ‘n’ (for noisy) or ‘c’ (for clean). Once the appropriate key is pressed
    proceed to the next file.
    Once all the files are processed export a json file where you have the file names and
    corresponding labels.
    """
    # The function, which works when playing music, allows the user to select music noisy or clear
    def ask_user(self):
        check = str(input("Please select: 'n' (for noisy) or 'c' (for clean): ")).lower().strip()
        try:
            # return 'n' (for noisy)
            if check == 'n':
                return user_select
            # return 'c' (for clean)
            elif check == 'c':
                return user_select
            else:
                print("Invalid Input, please try again: 'n'  or 'c'")
                return self.ask_user()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user()

    # Function which return user provided directory where the json file should be exported or default/current dir.
    def valid_json_dir(self):
        check = input("Do you want to export in default path ? y/n: ").strip()
        try:
            # Return default directory, provided by user
            if check == 'y':
                return check
            # User provide dir for export
            elif check == 'n':
                export_path = input("Please specify the directory where the json file should be exported: ").strip()
                # Check if provided path is exist
                if not os.path.exists(export_path):
                    print("Provided path: {} doesn't exist, please provide correct path.".format(export_path))
                    return self.valid_json_dir()
                # Check if provided path is directory
                elif not os.path.isdir(export_path):
                    print("Provided path: {} isn't directory, please provide directory.".format(export_path))
                    return self.valid_json_dir()
                return export_path
            else:
                print("Invalid Input, please try again: 'y'  or 'n'")
                return self.valid_json_dir()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.valid_json_dir()

    # Function which return user provided json name or default one
    def valid_json_name(self):
        check = input("Do you want to save JSON file with default name mp3.json ? y/n: ").strip()
        try:
            # Return json name as a default one
            if check == 'y':
                return str("mp3.json")
            # Return user specifed json file name
            elif check == 'n':
                return str(input("Please specify the name of json file: ")).strip()
            else:
                print("Invalid Input, please try again: 'y'  or 'n'")
                return self.valid_json_name()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.valid_json_name()

    # Function whcih return valid provided by user directory
    def get_valid_directory(self):
        current_dir = input("Enter the Directory of your mp3 files: ").strip()
        try:
            # Check if provided path is exist
            if not os.path.exists(current_dir):
                print("Provided path: {} doesn't exist, please provide correct path.".format(current_dir))
                return self.get_valid_directory()
            # Check if provided path is directory
            elif not os.path.isdir(current_dir):
                print("Provided path: {} isn't directory, please provide directory.".format(current_dir))
                return self.get_valid_directory()
            # Check if provided directory is empty
            elif not os.listdir(current_dir):
                print("Provided directory: {} is empty.".format(current_dir))
                return self.get_valid_directory()
            print("Provided directory is correct: {}".format(current_dir))
            return current_dir
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.get_valid_directory()

    # Get list of mp3 files from provided directory
    def collect_files(self, current_dir):
        # Collect content of provided directory and set in list
        content_dir = os.listdir(current_dir)
        # Define the new list for mp3 format
        list_mp3 = []
        # Using loop sorting mp3 format
        for i in content_dir:
            # Choosing only files which ends with .mp3
            if str(i).endswith('.mp3'):
                # Defined full path of mp3 files
                full_path = os.path.join(current_dir, i)
                # Checking size of files
                check_file = os.path.getsize(full_path)
                # Check if path is file
                if not os.path.isfile(full_path):
                    print("The {} isn't file.".format(full_path))
                    break
                # Check if file is empty
                elif check_file == 0:
                    print("The {} is empty.".format(full_path))
                    break
                # If validation of file passed append in the list 
                list_mp3.append(full_path)
        return list_mp3

    # Waiting command of user, start playing music or exit from program
    def check_to_start_play(self):
        check = input("Do you want to start playback ? y/n: ").strip()
        try:
            if check == 'y':
                print("Starting playback music.")
                return
            elif check == 'n':
                sys.exit("Exit From Program!")
            else:
                print("Invalid Input, please try again: 'y'  or 'n'")
                return self.check_to_start_play()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.check_to_start_play()

    # Play list of mp3 files and return dictionary
    def playback_music(self, list_mp3):
        # Creating dictionary to define, key: mp3 file name and value: user choice
        my_dict = {}
        # Defined a total mp3 files in provided directory
        count = len(list_mp3)
        for i in list_mp3:
            # Counting the number of queued mp3 files found in the specified directory
            count -= 1
            # Using pygame(mixer) library playing mp3 files
            mixer.init()
            mixer.music.load(i)
            mixer.music.play()
            # Using a Loop to Control of Music Playback, a few choice is given to the user
            while True:
                print("Press 'p' to pause, 'r' to resume:")
                print("Press 'v' to restart music:")
                print("Press 'e' to exit the program:")
                print("Please select: 'n' (for noisy) or 'c' (for clean): ")
                query = input("  ").strip()
                if query == 'p':
                    # Pausing the music
                    mixer.music.pause()     
                elif query == 'r':
                    # Resuming the music
                    mixer.music.unpause()
                elif query == 'v':
                    # Restart the music
                    mixer.music.rewind()
                elif query == 'n' or query == 'c':
                    # Stop the mixer
                    mixer.music.stop()
                    break
                elif query == 'e':
                    # Stop and Exist from program
                    mixer.music.stop()
                    sys.exit("Exit From Program!")
                else:
                    print("Invalid Input, please try again:")
            # Set key & value in dictionary, key: file_name & value: user_input
            my_dict[os.path.basename(i)] = query
            # Gives the user information how many more files are in the queue
            if count != 0:
                print("{} files left to check.".format(count))
        return my_dict

    # The main procedure which call rest proc
    def main_proc(self):
        # Creating loop, until user provided valid directory which contain mp3 files
        while True:
            # Return valid provided by user directory
            current_dir = self.get_valid_directory()
            # Return list which contain mp3 format file/s from provided directory
            list_mp3 = self.collect_files(current_dir)
            if len(list_mp3) != 0:
                break
            else:
                print("There was no mp3 format in the specified directory, please provide the directory which contain mp3 format:")

        print("A total of {} files are ready to be scanned.".format(len(list_mp3)))
        # Check if user want to play music
        self.check_to_start_play()

        # Play mp3 files and return dict
        my_dict = self.playback_music(list_mp3)

        print("The default path of exporting JSON file is current directory: {}".format(current_dir))
        # Get valid json directory
        export_path = self.valid_json_dir()

        # Define current dir as a json export directory
        if export_path == 'y':
            export_path = current_dir

        print("The default name of JSON file is: mp3.json")
        # Return Json name
        json_name = self.valid_json_name()
        if not str(json_name).endswith('.json'):
            json_name = "".join(json_name + '.json')

        # Creating full path of json file
        json_path = os.path.join(export_path, json_name)

        # Creating json file and dump dictionnary into it
        with open(json_path, "w") as f:
            json.dump(my_dict, f)
        print("The Json file successfully saved under: {}".format(json_path))
        print("The Program Successfully Finished.")

if __name__ == "__main__":
    print ("Welcome to the MP3 reader!")
    class_reader = mp3_reader()
    class_reader.main_proc()

