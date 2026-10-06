import os


"""common"""
# root project
root_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# directory data
dir_raw_data = os.path.join(root_project,"data","raw")
dir_processed_data = os.path.join(root_project,"data","processed")