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


if __name__ == '__main__':
    files = FileUtils.get_all_file_by_path(".", ext="*.py*", recursive=True)
    print(files)
