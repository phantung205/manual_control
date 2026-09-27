from configs import config_hands
import os
import shutil

def split_class(class_name):
    # lấy ra thư mục class
    class_dir = os.path.join(config.dir_raw_data,class_name)

    # lấy tất cả các file trong thư mục class đó
    files = [file_name for file_name in os.listdir(class_dir) if file_name.endswith(".npy")]


    # sắp xếp file
    files.sort()

    # tạo hai thư mục train và val
    train_dir = os.path.join(config_hands.dir_processed_data,"train",class_name)
    val_dir = os.path.join(config_hands.dir_processed_data,"val",class_name)

    os.makedirs(train_dir,exist_ok=True)
    os.makedirs(val_dir,exist_ok=True)

    # chia dữ liệu
    train_files = []
    val_files = []
    for index, file_name in enumerate(files):
        # Cứ 5 file lấy 1 file làm validation
        if (index + 1) % 5 == 0:
            val_files.append(file_name)
        else:
            train_files.append(file_name)

    # 5. Copy train
    for file_name in train_files:
        source = os.path.join(class_dir,file_name)
        destination = os.path.join(train_dir,file_name)
        shutil.copy2(source,destination)

    # 6. Copy validation
    for file_name in val_files:
        source = os.path.join(class_dir,file_name)
        destination = os.path.join(val_dir,file_name)
        shutil.copy2(source,destination)

    # 7. In kết quả
    print(
        f"{class_name}: "
        f"total={len(files)}, "
        f"train={len(train_files)}, "
        f"val={len(val_files)}"
    )

def main():
    for class_name in config_hands.categories:
        split_class(class_name)

if __name__ == "__main__":
    main()

