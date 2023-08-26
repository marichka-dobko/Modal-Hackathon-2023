import glob
import shutil

files_iter = glob.glob('/Users/mariadobko/Modal-Hackathon-2023/plans_txt/**')
for f in files_iter:
    dst = '/Users/mariadobko/Modal-Hackathon-2023/plans_txt_resaved/'
    f_name = f.split('/')[-1]
    f_name = f_name.replace(' ', '_')
    print(f, dst+f_name)
    shutil.copyfile(f, dst+f_name)
