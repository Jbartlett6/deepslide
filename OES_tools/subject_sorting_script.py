import shutil
import pandas as pd
import os
import glob

def construct_class_dict(csv_path, mode):
    
    data = pd.read_csv(csv_path)
    class_dict = {}
    if mode == 'all':
        vals = [1,2,3,5,6]
        classes = data['Mandard'].unique()[vals]

        
        for class_name in classes:
            class_dict[class_name] = list(data.query(f"Mandard=='{class_name}'")['record_id'])

    elif mode == 'bin':
        classes = ['True', 'False']
        pos_vals = [3,5]
        neg_vals = [1,6]

        pos_classes = data['Mandard'].unique()[pos_vals]
        neg_classes = data['Mandard'].unique()[neg_vals]

        pos_classes_list = list(data.query(f"Mandard=='{pos_classes[0]}'")['record_id']) + list(data.query(f"Mandard=='{pos_classes[1]}'")['record_id'])
        neg_classes_list = list(data.query(f"Mandard=='{neg_classes[0]}'")['record_id']) + list(data.query(f"Mandard=='{neg_classes[1]}'")['record_id'])

        class_dict = {'True': pos_classes_list, 'False': neg_classes_list}

    return class_dict

def make_directories(class_dict, target_directory):
    for class_name in class_dict.keys():
        class_dir = os.path.join(target_directory, class_name)
        if os.path.isdir(class_dir) == False:
            os.mkdir(class_dir)
        
def sort_subjects(class_dict, origin_dir, target_dir):
    for class_name, class_list in class_dict.items():
        for subject in class_list:

            subject_path = os.path.join(origin_dir, subject)
            file_list = glob.glob(f'{subject_path}_*')
            
            for file in file_list:
                shutil.copyfile(file, os.path.join(target_dir, class_name, file.split('/')[-1]))
                # print(file.split('/')[-1])
                # print(os.path.join(target_dir, class_name, file.split('/')[-1]))


if __name__ == '__main__':
    deepslide_dir = '/data/gpfs/projects/punim2070/code/deepslide/deepslide'
    csv_path = os.path.join(deepslide_dir, 'OES_tools', 'Slide Scanning Log.xlsx - Labelling.csv')
    target_dir = os.path.join(deepslide_dir, 'all_wsi')
    
    origin_dir = '/data/gpfs/projects/punim2070/data_jpg/OAC Slides JPEG Export_downsampled10'
    mode = 'bin'
    print('hello')
    print(os.path.exists(target_dir), '\n', os.path.exists(csv_path), '\n', os.path.exists(origin_dir), '\n')

    class_dict = construct_class_dict(csv_path, mode)
    make_directories(class_dict, target_dir)
    sort_subjects(class_dict, origin_dir, target_dir)
    