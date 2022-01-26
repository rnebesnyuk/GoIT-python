from pathlib import Path
import os
import re
import shutil
import sys

PIC_EXT = ['.jpeg', '.png', '.jpg', '.svg', '.gif', '.bmp']
VID_EXT = ['.avi', '.mp4', '.mov', '.mkv']
DOC_EXT = ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.xls', '.pptx', '.ppt']
AUD_EXT = ['.mp3', '.ogg', '.wav', '.amr']
ARCH_EXT = ['.zip', '.gz', '.tar']
FILE_CATEGORIES = {
    'images':[], 
    'video': [],
    'documents': [],
    'audio': [], 
    'archives': []
    }
KNOWN_EXT = set()
UNKNOWN_EXT = set()

def get_cmd_input():
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        print("Please enter 1 argument with a valid Directory path")
    else:
        return sys.argv[1]

def create_folder(p):
    for category in FILE_CATEGORIES:
        folder = p/category
        if not folder.exists():
            os.mkdir(folder)

def folder_check(p):
    for item in p.iterdir():
        if item.is_dir():
            if item.name !='images'and item.name !='video'and item.name !='documents'and item.name !='audio'and item.name !='archives':
                new_folder_name = normalize(item.name)
                updated_folder_path = Path(f'{item.parent}/{new_folder_name}')
                os.rename(item, updated_folder_path)
                folder_check(updated_folder_path)
        elif item.is_file():
            sorter_of_files(item)

def sorter_of_files(p): 
    ext = p.suffix
    name = p.stem
    normalized_name = normalize(name)
    updated_path = p.rename(Path(p.parent, normalized_name + ext))
    if ext.casefold() in PIC_EXT:
        FILE_CATEGORIES['images'].append(normalized_name + ext)
        KNOWN_EXT.add(ext)
        shutil.move(f'{p.parent}/{normalized_name}{ext}', f'{SORTING_FOLDER}/images/{normalized_name}{ext}')
    elif ext.casefold() in VID_EXT:
        FILE_CATEGORIES['video'].append(normalized_name + ext)
        KNOWN_EXT.add(ext)
        shutil.move(f'{p.parent}/{normalized_name}{ext}', f'{SORTING_FOLDER}/video/{normalized_name}{ext}')
    elif ext.casefold() in DOC_EXT:
        FILE_CATEGORIES['documents'].append(normalized_name + ext)
        KNOWN_EXT.add(ext)
        shutil.move(f'{p.parent}/{normalized_name}{ext}', f'{SORTING_FOLDER}/documents/{normalized_name}{ext}')
    elif ext.casefold() in AUD_EXT:
        FILE_CATEGORIES['audio'].append(normalized_name + ext)
        KNOWN_EXT.add(ext)
        shutil.move(f'{p.parent}/{normalized_name}{ext}', f'{SORTING_FOLDER}/audio/{normalized_name}{ext}')
    elif ext.casefold() in ARCH_EXT:
        FILE_CATEGORIES['archives'].append(normalized_name + ext)
        KNOWN_EXT.add(ext)
        if not os.path.exists(f'{SORTING_FOLDER}/archives/{normalized_name}'):
            os.mkdir(f'{SORTING_FOLDER}/archives/{normalized_name}')
        shutil.unpack_archive(updated_path, f'{SORTING_FOLDER}/archives/{normalized_name}')
        os.remove(updated_path)
    else:
        UNKNOWN_EXT.add(ext)


def normalize(name):
    table_symbols = ("абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ", 
                        (*(u"abvhgde"), "ye", "zh", *(u"zyi"), "yi", *(u"yklmnoprstuf"), "kh", "ts", 
                        "ch", "sh", "shch", "yu", "ya", "y", "ye", *(u"ABVHGDE"), "YE", "ZH", *(u"ZYI"), "YI", 
                        *(u"YKLMNOPRSTUF"), "KH", "TS", "CH", "SH", "SHCH", "YU", "YA", "Y", "YE", *(u"_" * 4))
                    )
    map_cyr_to_lat = {ord(a): b for a, b in zip(*table_symbols)}
    return re.sub(r"[\W]", "_", name.translate(map_cyr_to_lat))

def remove_empty_folders(p):
    for item in p.iterdir():
        if item.is_dir():
            if len(os.listdir(item)) == 0 and item.name !='images'and item.name !='video'and item.name !='documents'and item.name !='audio'and item.name !='archives':
                recheck_folder = (item.parent).parent
                shutil.rmtree(item)
                remove_empty_folders(recheck_folder)
            else:
                remove_empty_folders(item)           

if __name__ == "__main__":
    p = Path(get_cmd_input())
    SORTING_FOLDER = p
    if p.is_dir():
        print(f"Sorting started in {p.name} folder")
        create_folder(p)
        folder_check(p)
        remove_empty_folders(p)
        print(f'Sorting completed')
        print(f'{FILE_CATEGORIES},\nKnown extensions: {KNOWN_EXT}, Unknown extensions: {UNKNOWN_EXT}')
    else:
        print("Path entered refers to not valid Directory or File, please provide a correct Directory path")