import os
import tarfile

# Создание директорий и файлов
os.makedirs('test_fs/folder', exist_ok=True)

with open('test_fs/file.txt', 'w') as f:
    f.write('Это тестовый файл.\n')

with open('test_fs/folder/nested_file.txt', 'w') as f:
    f.write('Это вложенный тестовый файл.\n')

# Создание tar-архива
with tarfile.open('test_fs.tar', 'w') as tar:
    tar.add('test_fs', arcname=os.path.basename('test_fs'))

