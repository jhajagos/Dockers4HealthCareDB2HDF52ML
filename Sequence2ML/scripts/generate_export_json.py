import json
import os


def main():

    with open("../config/config_export.json") as f:
        config_dict = json.load(f)

    table_names =  ["map2_condition_occurrence", "map2_drug_exposure", "map2_measurement_numeric",
                   "map2_measurement_categorical", "map2_death_visit_occurrence",
                   "map2_observation_numeric", "map2_observation_categorical", "map2_person_visit_occurrence",
                   "map2_procedure_occurrence", "map2_visit_occurrence", "map2_condition_occurrence_hierarchy",
                   "map2_atc3_drug_exposure", "map2_atc4_drug_exposure", "map2_visit_detail", "map2_atc5_flattened_drug_exposure"
                   ]

    export_table_template_dict = {
         "file_name": None,
         "connection_uri": None,
         "table_name": None,
         "schema": None,
    }

    export_table_list = []

    for table_name in table_names:

        export_table_dict = export_table_template_dict.copy()

        export_table_dict["file_name"] = os.path.join(config_dict["export_directory"], table_name + ".csv")
        export_table_dict["connection_uri"] = config_dict["connection_uri"]
        export_table_dict["table_name"] = config_dict["schema"] + "." + table_name
        export_table_dict["schema"] = config_dict["schema"]
        export_table_dict["order_by"] = ["visit_occurrence_id"]

        if "restrictions" in config_dict:
            export_table_dict["restrictions"] = config_dict["restrictions"]

        export_table_list += [export_table_dict]

    with open("../config/export_tables.json", "w") as fw:
        json.dump(export_table_list, fw, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    main()
