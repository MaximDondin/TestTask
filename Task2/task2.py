import os
import shutil
import json
from datetime import datetime
import subprocess


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def clone_repository(repo_url):
    log(f"Клонирование репозитория: {repo_url}")
    repo_name = os.path.basename(repo_url).replace('.git', '')
    clone_dir = os.path.abspath(repo_name)
    if not os.path.exists(repo_name):
        try:
            subprocess.run(['git', 'clone', repo_url], check=True,)
            log("Репозиторий успешно клонирован")
            return clone_dir
        except subprocess.CalledProcessError as error:
            log(f"Ошибка при клонировании: {error}")
            return None
    else:
        log("Репозиторий уже существует. Пропуск клонирования.")
        return clone_dir


def clean_root_directory(root_dir, keep_dir):
    log(f"Очистка корневой директории, сохранение только: {keep_dir}")
    base_dir = keep_dir.split(os.path.sep)[0]
    for item in os.listdir(root_dir):
        if item == '.git':
            continue

        item_path = os.path.join(root_dir, item)
        if item != base_dir:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                log(f"Удалена директория: {item}")
            else:
                os.remove(item_path)
                log(f"Удален файл: {item}")


def create_version_file(source_dir, version):
    log("Создание version.json")

    files = []
    for filename in os.listdir(source_dir):
        if filename.endswith(('.py', '.js', '.sh')):
            files.append(filename)

    version_info = {
        "name": "hello world",
        "version": version,
        "files": sorted(files)
    }

    version_path = os.path.join(source_dir, 'version.json')
    with open(version_path, 'w') as file:
        json.dump(version_info, file, indent=4)

    log(f"Создан файл: {version_path}")
    log(f"Содержимое version.json:\n{json.dumps(version_info, indent=4)}")


def create_archive(source_path, output_dir):
    log("Создание архива")

    dir_name = os.path.basename(source_path)
    date_str = datetime.now().strftime("%d%m%y")
    archive_name = f"{dir_name}{date_str}.zip"
    archive_path = os.path.join(output_dir, archive_name)

    parent_dir = os.path.dirname(source_path)
    base_dir = os.path.basename(source_path)

    shutil.make_archive(
        base_name=os.path.join(output_dir, dir_name + date_str),
        format='zip',
        root_dir=parent_dir,
        base_dir=base_dir
    )

    log(f"Создан архив: {archive_path}")
    return archive_path


def build_package(repo_url, src_path, version):
    start_time = datetime.now()
    log("Начало процесса сборки")

    clone_dir = clone_repository(repo_url)
    if not clone_dir:
        return

    clean_root_directory(clone_dir, src_path)

    source_dir = os.path.join(clone_dir, src_path)
    if not os.path.exists(source_dir):
        log(f"Директория с исходным кодом не найдена: {source_dir}")
        return

    create_version_file(source_dir, version)

    archive_path = create_archive(source_dir, os.getcwd())

    log(f"Сборка завершена. Общее время: {datetime.now() - start_time}")
    return archive_path


if __name__ == "__main__":
    build_package('https://github.com/paulbouwer/hello-kubernetes', 'src/app', '25.3000')