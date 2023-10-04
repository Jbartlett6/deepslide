import shutil
import pandas as pd
import os
import glob

def construct_class_dict(csv_path, mode, include_M_3 = True):
    
    data = pd.read_csv(csv_path)
    class_dict = {}
    
    if mode == 'all':
        vals = [1,2,3,5,6]
        classes = data['Mandard'].unique()[vals]
        print(classes)
        
        for class_name in classes:
            class_dict[class_name] = list(data.query(f"Mandard=='{class_name}'")['record_id'])

    elif mode == 'bin':

        true_query = "Mandard=='I - No residual cancer' | Mandard=='II - rare residual cancer cells'"
        
        if include_M_3 == True:
            false_query = "Mandard=='III - Fibrosis outgrowing residual cancer' | Mandard=='IV - Residual cancer outgrowing fibrosis' | Mandard=='V - Absence of regressive changes'"
        else:
            false_query = "Mandard=='IV - Residual cancer outgrowing fibrosis' | Mandard=='V - Absence of regressive changes'"
        
        class_dict['True'] = list(data.query(true_query)['record_id'])
        class_dict['False'] = list(data.query(false_query)['record_id'])

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

if __name__ == '__main__':
    deepslide_dir = '/data/gpfs/projects/punim2070/code/deepslide/deepslide'
    csv_path = os.path.join(deepslide_dir, 'OES_tools', 'Slide Scanning Log.xlsx - Labelling.csv')
    target_dir = os.path.join(deepslide_dir, 'all_wsi_including_3')

    assert os.path.exists(target_dir) == False, 'Target directory already exists, either delete current directory or change target directory'
    
    os.mkdir(target_dir)

    origin_dir = '/data/gpfs/projects/punim2070/data_jpg/OAC Slides JPEG Export_downsampled10'
    mode = 'bin'

    class_dict = construct_class_dict(csv_path, mode)
    make_directories(class_dict, target_dir)
    sort_subjects(class_dict, origin_dir, target_dir)
    