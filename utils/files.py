import datetime
import os
from pathlib import Path


class FileUtils:
    @staticmethod
    def get_all_file_by_path(*paths, ext="*.*", recursive=False):
        result = []
        for path in paths:
            p = Path(path)
            if p.is_dir():
                files = p.rglob(ext) if recursive else p.glob(ext)
                for file in files:
                    result.append(str(file.absolute()))
            elif p.is_file():
                result.append(str(file.absolute()))
        return result

    @staticmethod
    def list_compressed_file(source_file: str):
        result = []
        if source_file.endswith(".tar.gz"):
            des_dir = source_file[:source_file.rfind(".tar.gz")] + "/"
            os.makedirs(des_dir)
            cmd = "tar -zxvf {} -C {}".format(source_file, des_dir)
            rs = os.system(cmd)
            if not rs == 0:
                return result
            for root, dirs, files in os.walk(des_dir):
                for file_name in files:
                    result.extend(FileUtils.list_compressed_file(os.path.join(root, file_name)))
        elif source_file.endswith(".tar"):
            des_dir = source_file[:source_file.rfind(".tar")] + "/"
            os.makedirs(des_dir)
            cmd = "tar -xvf {} -C {}".format(source_file, des_dir)
            rs = os.system(cmd)
            if not rs == 0:
                return result
            for root, dirs, files in os.walk(des_dir):
                for file_name in files:
                    result.extend(FileUtils.list_compressed_file(os.path.join(root, file_name)))
        elif source_file.endswith(".tar.bz2"):
            des_dir = source_file[:source_file.rfind(".tar.bz2")] + "/"
            os.makedirs(des_dir)
            cmd = "tar -xjvf {} -C {}".format(source_file, des_dir)
            rs = os.system(cmd)
            if not rs == 0:
                return result
            for root, dirs, files in os.walk(des_dir):
                for file_name in files:
                    result.extend(FileUtils.list_compressed_file(os.path.join(root, file_name)))
        elif source_file.endswith(".tar.Z"):
            des_dir = source_file[:source_file.rfind(".tar.Z")] + "/"
            os.makedirs(des_dir)
            cmd = "tar -xZvf {} -C {}".format(source_file, des_dir)
            rs = os.system(cmd)
            if not rs == 0:
                return result
            for root, dirs, files in os.walk(des_dir):
                for file_name in files:
                    result.extend(FileUtils.list_compressed_file(os.path.join(root, file_name)))
        elif source_file.endswith(".zip"):
            des_dir = source_file[:source_file.rfind(".zip")] + "/"
            cmd = "unzip -o {} -d {}".format(source_file, des_dir)
            rs = os.system(cmd)
            if not rs == 0:
                return result
            for root, dirs, files in os.walk(des_dir):
                for file_name in files:
                    result.extend(FileUtils.list_compressed_file(os.path.join(root, file_name)))
        else:
            result.append(source_file)
        return result

    @staticmethod
    async def delete_gq_24h_file(file_path):
        recent_time = (datetime.datetime.now() - datetime.timedelta(hours=24)).timestamp()
        for root, dirs, files in os.walk(file_path):
            for file_name in files:
                fp = os.path.join(root, file_name)
                visit_time = os.path.getatime(fp)
                if recent_time > visit_time:
                    os.remove(fp)


if __name__ == '__main__':
    files = FileUtils.get_all_file_by_path(".", ext="*.py*", recursive=True)
    print(files)
