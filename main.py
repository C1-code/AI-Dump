import os
import sys
import shutil
from pathlib import Path

class AIDump:
    """
    A class to find specific files in a directory structure, copy them to a new
    flattened directory with handling for duplicate names, and generate an
    indented tree map that reflects the final copied file structure.
    """
    def __init__(self, root_folder):
        """
        Initializes the AIDump object.

        Args:
            root_folder (str): The path to the source folder to be processed.
        
        Raises:
            FileNotFoundError: If the specified root_folder does not exist.
        """
        if not os.path.isdir(root_folder):
            raise FileNotFoundError(f"The specified root folder does not exist: {root_folder}")
        
        self.folder_path = os.path.abspath(root_folder)
        self.dest_path = os.path.join(os.getcwd(), os.path.basename(root_folder))
        os.makedirs(self.dest_path, exist_ok=True)
        self.extensions = ['.py', '.html', '.css', '.js']

    def dump(self):
        """
        Walks the directory once to copy files, determines their final (potentially
        renamed) names, and then generates a filtered tree reflecting those final names.
        """
        path_to_final_name_map = {}
        files_copied_counts = {}

        for root, dirs, files in os.walk(self.folder_path):
            dirs.sort()
            files.sort()
            
            for file_name in files:
                if any(file_name.endswith(ext) for ext in self.extensions):
                    base_name, extension = os.path.splitext(file_name)
                    count = files_copied_counts.get(file_name, 0) + 1
                    files_copied_counts[file_name] = count
                    dest_filename = f"{base_name}_{count}{extension}" if count > 1 else file_name

                    full_src_path = os.path.join(root, file_name)
                    path_to_final_name_map[full_src_path] = dest_filename
                    
                    full_dest_path = os.path.join(self.dest_path, dest_filename)
                    shutil.copy(full_src_path, full_dest_path)
        
        folder_map_string = self._generate_filtered_tree_string(path_to_final_name_map)

        with open(os.path.join(self.dest_path, "tree.txt"), "w") as f:
            f.write(folder_map_string)

    def _generate_filtered_tree_string(self, path_to_final_name_map):
        """Builds the tree string from a map of original paths to final names."""
        if not path_to_final_name_map:
            return "(No files with specified extensions found)"

        paths_to_include = set()
        for original_path in path_to_final_name_map.keys():
            path_obj = Path(original_path)
            paths_to_include.add(str(path_obj))
            parent = path_obj.parent
            while parent and str(parent) != str(Path(self.folder_path).parent):
                paths_to_include.add(str(parent))
                if str(parent) == self.folder_path:
                    break
                parent = parent.parent
        
        tree_list = []
        root_name = os.path.basename(self.folder_path)
        tree_list.append(f"{root_name}/")
        
        self._build_tree_recursively(self.folder_path, 0, tree_list, paths_to_include, path_to_final_name_map)
        
        return "\n".join(tree_list)

    def _build_tree_recursively(self, current_path, level, tree_list, paths_to_include, path_to_final_name_map):
        """Recursively builds the indented tree, using final names for files."""
        try:
            all_items = sorted(os.listdir(current_path))
        except OSError:
            return

        filtered_items = [item for item in all_items if os.path.join(current_path, item) in paths_to_include]
        
        indent = ' ' * 4 * (level + 1)
        
        for item_name in filtered_items:
            item_path = os.path.join(current_path, item_name)

            if os.path.isdir(item_path):
                tree_list.append(f"{indent}{item_name}/")
                self._build_tree_recursively(item_path, level + 1, tree_list, paths_to_include, path_to_final_name_map)
            else:
                display_name = path_to_final_name_map.get(item_path, item_name)
                tree_list.append(f"{indent}{display_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("[FOLDER NEEDED] Provide a folder as a command line argument.\nUsage: python your_script_name.py /path/to/your/project")
    
    folder_to_process = sys.argv[1]
    ai_dump = AIDump(folder_to_process)
    ai_dump.dump()