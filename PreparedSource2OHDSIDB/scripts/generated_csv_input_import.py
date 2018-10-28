
import glob
import os
import json


def main(input_directory, template_name, script_directory, path_to_python="python"):

    generated_templates = generate_json_import_template(input_directory + "*.csv",
                                           template_name)

    generated_scripts = []
    for generated_template in generated_templates:

        _, file_name = os.path.split(generated_template)
        script_name = os.path.join(script_directory + file_name + ".sh")

        generated_scripts += [script_name]

        with open(script_name, "w") as fw:

            fw.write("#!/bin/bash")
            fw.write("\n")
            fw.write(path_to_python + " " + os.path.abspath("../bulk_import_data_from_csv_to_db.py") + " -j " +
                     generated_template)

        import_all_script = os.path.join(script_directory, "import_all.sh")

        with open(import_all_script, "w") as fw:

            fw.write("#!/bin/bash")
            fw.write("\n")

            for script in generated_scripts:
                fw.write("bash " + script + "\n")


def generate_json_import_template(file_name_pattern, template_json_file):

    files_to_import = glob.glob(file_name_pattern)
    generated_templates = []

    csv_files_to_import = []
    for file_name in files_to_import:
        full_file_name = os.path.abspath(file_name)

        directory, file_name = os.path.split(full_file_name)
        base_file_name, extension = os.path.splitext(file_name)

        extension = extension.lower()
        if extension in (".csv", ".txt"):
            csv_files_to_import += [(file_name, base_file_name, directory)]

    for csv_file_to_import in csv_files_to_import:
        with open(template_json_file, "r") as f:
            template_obj = json.load(f)

            file_name, base_file_name, directory = csv_file_to_import
            template_obj["file_name"] = os.path.join(directory, file_name)
            template_obj["table_name"] = base_file_name

            template_file_name = os.path.join(directory, file_name) + ".json"
            with open(template_file_name, "w") as fw:
                json.dump(template_obj, fw, indent=4, separators=(',', ': '))

            generated_templates += [template_file_name]

    return generated_templates



if __name__ == "__main__":

    main("Y:\\healthfacts\\20180919\\input\\", "../config/prepared_source_template.json", "./input/")


    #main("/root/ohdsi/input/", "../config/prepared_source_template.json", "/root/ohdsi/scripts/import/")