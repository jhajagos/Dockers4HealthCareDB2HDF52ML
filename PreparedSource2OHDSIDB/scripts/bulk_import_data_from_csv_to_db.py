"""
    Imports a CSV file into SQL database that is supported by SqlAlchemy.

    The purpose of this script is to make importing CSV files easy into a database
    to do quick things that can be done quickly using a relational database, like filtering and
    SQL inner joins.

    Adapted from original import_tab_delimited_to_sql.py

    Based on the engine it creates SQL for a bulk import of the data

"""

import re
import csv
import pprint
from optparse import OptionParser
import os
import json

from sqlalchemy import Table, Column, Integer, Text, Float, String, DateTime, MetaData, create_engine, text


def clean_header(raw_header):
    header = []
    special_characters_map = {"#": "_POUND", "%": "_PERCENT", " ": "_", '"': "",
                              "&": "AND", "/": "_", "-": "_", ".": "_PERIOD",
                              "?": "_QUESTION", "+": "_PLUS", "(": "_", ")": "_", "$": "_DOLLAR", ",": "_",
                              '\n': "_"}

    for original_label in raw_header:  # Rewrite column names in a more SQL friendly way
        label = original_label
        for split_char in special_characters_map.keys():
            split_label = label.split(split_char)

            if len(split_label) > 1:
                label = special_characters_map[split_char].join(split_label) #split_label.join(special_characters_map[split_char])

        label = "_".join([x for x in label.split("_") if len(x) > 0])

        if label[-1] == "_":
            label = label[:-1]

        header.append(label)

    return header


def generate_schema_from_csv_file(file_name, connection_url, table_name="temp_table", delimiter=",", no_header=False,
                                  override_header=None, schema_only=None, schema=None, drop_table_first=False,
                                  no_primary_key=False, timestamp=True):
    """Takes a csv file and creates a table schema for it"""

    with open(file_name, newline="", mode="r") as f:

        try:
            engine = create_engine(connection_url)

        except(IOError):
            print("Database could not be connected to")
            raise

        if override_header:
            header = override_header
            csv_reader = csv.reader(f, delimiter=delimiter)
        else:
            if no_header:
                with open(file_name, newline="", mode="r") as ft:
                    csv_reader = csv.reader(ft, delimiter=delimiter)
                    row = csv_reader.__next__()

                    header = []
                    for i in range(len(row)):
                        header += ["V" + str(i)]

                csv_reader = csv.reader(f, delimiter=delimiter)

            else:
                csv_reader = csv.reader(f, delimiter=delimiter)
                raw_header = csv_reader.__next__()
                header = clean_header(raw_header)

        positions = {}
        data_types = {}
        field_sizes = {}

        for i in range(len(header)):
            positions[i] = header[i]
            data_types[header[i]] = {}
            field_sizes[header[i]] = 0

        # This part here will empirically determine data types from the entire file
        for row in csv_reader:
            for j in range(len(header)):
                    try:
                        data_type = get_data_type(row[j])
                        field_sizes[positions[j]] = max(field_sizes[positions[j]],len(row[j]))
                    except IndexError:
                        data_type = get_data_type("")

                    if data_type in data_types[positions[j]]:
                        data_types[positions[j]][data_type] += 1
                    else:
                        data_types[positions[j]][data_type] = 1
        f.close()

        data_type = {}
        for column_name in header:
            data_type[column_name] = find_data_type_by_precedence(data_types[column_name])

        if "ID" not in [column_name.upper() for column_name in header]:
            if not no_primary_key:
                columns_to_create = [Column('id', Integer, primary_key=True, autoincrement=True)]
            else:
                columns_to_create = []
        else:
            columns_to_create = []

        for j in range(len(header)):
            column_name = header[j]

            if data_type[column_name] is None:
                data_type[column_name] = String(1)

            if data_type[column_name] == String:
                allowed_field_sizes = [1, 4, 16, 256, 512, 1024]
                field_size = field_sizes[column_name]
                new_field_size = None
                if field_size < allowed_field_sizes[-1]:
                    for i in range(len(allowed_field_sizes)):
                        if allowed_field_sizes[i] == field_size:
                            new_field_size = allowed_field_sizes[i]
                        elif i > 0 and field_size < allowed_field_sizes[i] and field_size > allowed_field_sizes[i-1]:
                            new_field_size = allowed_field_sizes[i]

                    if new_field_size:
                        field_size = new_field_size
                if field_size == 0:
                    field_size = 1

                field_sizes[column_name] = field_size
                data_type[column_name] = String(field_sizes[column_name])

            if data_type[column_name] == Integer: # If the integer is too large store as string using 2**32 has 10 digits as cut off
                if field_sizes[column_name] > 9:
                    data_type[column_name] = String(field_sizes[column_name])

            columns_to_create.append(Column(column_name, data_type[column_name]))

        metadata = MetaData(schema=schema)
        if not drop_table_first:
            pass
        else:

            table_name_with_schema = table_name
            if schema is not None:
                table_name_with_schema = schema + "." + table_name_with_schema

            #TODO: This uses PostGreSQL if exists syntax
            # if table_name_with_schema in metadata.tables:
            #     table_object = metadata.tables[table_name_with_schema]
            #     table_object.drop()
            engine.execute("drop table if exists %s" % table_name_with_schema)

        if timestamp:
            columns_to_create += [Column("created_on", DateTime, server_default=text('NOW()'))]

        import_table = Table(table_name, metadata, *columns_to_create)

        pprint.pprint(columns_to_create)
        metadata.create_all(engine)

        metadata.create_all(engine)
        if schema_only:
           pass
        else:
            import_csv_file_using_inserts(file_name, connection_url, table_name, header, data_type, positions, delimiter, schema=schema)


def import_csv_file_using_inserts(file_name, connection_url, table_name, header, data_type, positions, delimiter, schema=None):

    engine = create_engine(connection_url)
    connection = engine.connect()
    transaction = connection.begin()

    i = 0
    table_name_to_insert = engine.dialect.identifier_preparer.quote_identifier(table_name)
    if schema is not None:
        table_name_to_insert = engine.dialect.identifier_preparer.quote_identifier(schema) + "." + table_name_to_insert

    with open(file_name, newline="", mode="r") as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        csv_reader.__next__()
        for split_line in csv_reader:

            # Handle type conversion
            data_converted = []
            columns_to_include = []
            j = 0
            for value in split_line:
                cleaned_value = clean_string(value)
                converted_string = convert_string(cleaned_value, data_type[positions[j]])
                if converted_string is not None:
                    columns_to_include.append(header[j])
                    data_converted.append(converted_string)
                j += 1

            # Build insert sql string
            header_string = "("
            for label in columns_to_include:
                header_string = header_string + engine.dialect.identifier_preparer.quote_identifier(label) + ","
            header_string = header_string[:-1] + ")"

            insert_template = "insert into %s  %s values (%s)" % (table_name_to_insert, header_string,
                                                                  ("%s," * len(columns_to_include))[:-1])

            if len(data_converted) > 0:
                try:
                    connection.execute(insert_template % tuple(data_converted))
                except:
                    transaction.commit()
                    raise

            if i % 10000 == 0 and i > 0:
                print("Importing %s records" % i)
                transaction.commit()
                transaction = connection.begin() # Begin a new transaction
            i += 1

        transaction.commit()
        print("Imported %s rows into '%s'" % (i, table_name))
    connection.close()


def find_data_type_by_precedence(data_type_hash):
    data_types = data_type_hash.keys()
    inferred_data_type = None

    if DateTime in data_types and (Integer in data_types or Float in data_types):
        return String

    for data_type in data_types:
        if data_type is not None:
            if inferred_data_type is None and data_type is not None: #initially we assume that the data type is not None
                inferred_data_type = data_type
            else:
                if inferred_data_type == Integer and data_type == Float:
                    inferred_data_type = Float
                if inferred_data_type == DateTime and data_type == Integer:
                    inferred_data_type = String
                elif data_type == String:
                    inferred_data_type = String
                    
    if inferred_data_type is None:
        return Integer
    else:
        return inferred_data_type


def clean_csv_file_for_import(csv_file_name, delimiter=",", header = True):
    """Cleans a CSV file and returns a cleaned version"""

    abs_csv_file_for_import = os.path.abspath(csv_file_name)
    base_path, pure_csv_file_name = os.path.split(abs_csv_file_for_import)

    pure_csv_base_name,extension = os.path.splitext(pure_csv_file_name)

    cleaned_csv_file_name = pure_csv_base_name + "_cleaned.csv"

    abs_cleaned_csv_file_name = os.path.join(base_path, cleaned_csv_file_name)
    # print(abs_cleaned_csv_file_name)

    with open(abs_csv_file_for_import, newline="", mode="r") as f:
        with open(abs_cleaned_csv_file_name, newline="w") as fw:

            csv_reader = csv.reader(f, delimiter=delimiter)
            csv_writer = csv.writer(fw)

            i = 0

            if header:
                header = csv_reader.__next__()
                header_cleaned = clean_header(header)
                csv_writer.writerow(header_cleaned)

            for row in csv_reader:
                cleaned_row = [clean_string(item) for item in row]
                csv_writer.writerow(cleaned_row)

                i += 1
    return abs_cleaned_csv_file_name


re_money = re.compile(r"\$[0-9,.]+")
re_float = re.compile(r"-?([0-9+]*\.?|[eE]?|[0-9]?)+$")
re_quotes = re.compile(r'^".*"$')
re_us_date_format = re.compile(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}$")


def clean_string(string_to_clean):
    """Cleans a string for importing into a sql database"""
    # Right now we only pre-process money string

    string_to_clean = string_to_clean.rstrip()
   
    if re_quotes.match(string_to_clean):
        string_to_clean = string_to_clean[1:-1]

    if len(string_to_clean) <= 16: # Long strings ignore
        if re_money.match(string_to_clean):
            string_to_clean = "".join(string_to_clean.split(","))[1:]
            if "." not in string_to_clean:  # if there is no decimal add one so it is imported as a float
                string_to_clean = string_to_clean + ".00"

    if len(string_to_clean) <= 16: # Long strings ignore
        if re_float.match(string_to_clean):
            string_to_clean = "".join(string_to_clean.split(","))

    if re_us_date_format.match(string_to_clean):
        date_split = string_to_clean.split("/")
        
        month = int(date_split[0])
        day = int(date_split[1])
        year_string = date_split[2]
        
        year = int(year_string)
        
        if len(year_string) == 1:
            year_string = "0" + year_string
        
        date_string = ""
        if len(year_string) < 4:
            if year < 100:
                if year > 50:
                    year_string = "19%s" % year_string
                else:
                    year_string = "20%s" % year_string
        else:
            year_string = "%s" % year
        
        date_string = "%s-%s-%s" % (year_string, month, day)
        string_to_clean = date_string    
        
    return string_to_clean


def convert_string(string_to_convert, data_type):
    if "'" in string_to_convert:
        string_to_convert = "''".join(string_to_convert.split("'"))
    
    if "%" in string_to_convert:
        string_to_convert = "%%".join(string_to_convert.split("%"))
        
    if string_to_convert == "":
        return "NULL"
    elif data_type == Float:
        if "." == string_to_convert:
            string_to_convert = "0"
        return float(string_to_convert)
    elif data_type == Integer:
        return int(string_to_convert)
    else:
        return "'%s'" % string_to_convert

re_integer = re.compile(r"^([1-9][0-9]*$|0$)")
re_float_complex = re.compile(r"([0-9]*\.[0-9]+[eE](\+|\-)?[0-9]+|[[1-9][0-9]*[eE](\+|\-)?[0-9]+|[0-9]*\.[0-9]*|\.[0-9]+[eE](\+|\-)?[0-9]+|\.[0-9]+|[1-9][0-9]*)$")
re_odbc_date = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$")
re_odbc_date_time_1 = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}$")
re_odbc_date_time_2 = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")
re_odbc_date_time_3 = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]+$")
re_odbc_date_time_4 = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[-+][0-9]{2}:[0-9]{2}")
re_date = re.compile(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}")


def get_data_type(string_to_evaluate):
    """Take a string and returns a SQLAlchemy data type class"""

    if string_to_evaluate == "":
        return None
    elif re_odbc_date.match(string_to_evaluate):
        return DateTime
    elif re_date.match(string_to_evaluate):
        return DateTime
    elif re_odbc_date_time_1.match(string_to_evaluate):
        return DateTime
    elif re_odbc_date_time_2.match(string_to_evaluate):
        return DateTime
    elif re_odbc_date_time_3.match(string_to_evaluate):
        return DateTime
    elif re_odbc_date_time_4.match(string_to_evaluate):
        return DateTime
    elif re_integer.match(string_to_evaluate):
        return Integer
    elif re_float_complex.match(string_to_evaluate):
        return Float

    else:
        return String


def ensure_options_dict_missing_fields(options_dict):

    option_names = ["file_name", "connection_string", "table_name", "delimiter", "no_headers", "header", "out_file_name",
                    "schema_only_file_name", "cleaned_csv_file_name", "db_schema", "drop_table_first", "no_primary_key"]

    for option_name in option_names:
        if option_name not in options_dict:
            options_dict[option_name] = None
    return options_dict


def set_options(options):
    options_dict = {}
    options_dict["file_name"] = options.file_name
    options_dict["connection_string"] = options.connection_string
    options_dict["table_name"] = options.table_name
    options_dict["delimiter"] = options.delimiter
    options_dict["no_headers"] = options.no_headers
    if options.header.__class__ == "".__class__:
        options_dict["header"] = options.header.split()
    else:
        options_dict["header"] = options.header

    options_dict["out_file_name"] = options.out_file_name
    options_dict["schema_only_file_name"] = options.schema_only_file_name
    options_dict["cleaned_csv_file_name"] = options.cleaned_csv_file_name
    options_dict["db_schema"] = options.db_schema
    options_dict["drop_table_first"] = options.drop_table_first
    options_dict["no_primary_key"] = options.no_primary_key

    return options_dict


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file_name",
                      help="CSV file to import")

    parser.add_option("-d", "--delimiter", dest="delimiter",
                      help="default delimiter is ','", default=",")

    parser.add_option("-c", "--connection",
                      help="SQLAlchemy Connection String", default="sqlite:///import.db3", dest="connection_string")

    parser.add_option("-t", "--tablename",
                      help="SQLALchemy connection string", default="csv_import_table", dest="table_name")

    parser.add_option("-n", "--noheader",
                      help="Whether there is a header present or not", default=False, dest="no_headers")

    parser.add_option("-x", "--header",
                      help="Specify the header as a space separated list, .e.d, first_name last_name dob",
                      default=None, dest="header")

    parser.add_option("-o", "--outfilename",
                      help="Rather then execute we will write the file as an SQL statement", default=None,
                      dest="out_file_name"
                      )

    parser.add_option("-y", "--schemaonly",
                      help="Generate the schema with flag 1", default=None, dest="schema_only_file_name"
                      )

    parser.add_option("-l", "--cleanedcsvfilename",
                      help="Output a cleaned version of the file", default=None, dest="cleaned_csv_file_name",
                      )

    parser.add_option("-b", "--bulk_load_file_name",
                      help="Bulk load a file using database bulk load functionality. The file has to be accessible on the server."
                      )

    parser.add_option("-s", "--schema",
                      help="Import data set into a specified database schema", default=None, dest="db_schema"
                      )

    parser.add_option("-p", "--droptablefirst",
                      help="Drop the existing table first", default=False, dest="drop_table_first", action="store_true"
                      )

    parser.add_option("-j", "--jsonfile", default=False, dest="json_file_name")

    parser.add_option("-i", "--noid", default=False, dest="no_primary_key", action="store_true")

    (options, args) = parser.parse_args()

    if options.json_file_name:
        absolute_json_file_name = os.path.abspath(options.json_file_name)
        if os.path.exists(absolute_json_file_name):
            print("Loading options from '%s'" % absolute_json_file_name)

            with open(options.json_file_name, "r") as f:
                options_dict = json.load(f)
            pprint.pprint(options_dict)

        else:
            options_dict = set_options(options)

            with open(absolute_json_file_name, "w") as fw:
                json.dump(options_dict, fw, indent=4, separators=(',', ': '))
    else:
        options_dict = set_options(options)

    options_dict = ensure_options_dict_missing_fields(options_dict)
    generate_schema_from_csv_file(options_dict["file_name"], options_dict["connection_string"],
                                  options_dict["table_name"], str(options_dict["delimiter"]),
                                  drop_table_first=options_dict["drop_table_first"],schema=options_dict["db_schema"],
                                  no_header=options_dict["no_headers"], override_header=options_dict["header"],
                                  no_primary_key=options_dict["no_primary_key"])
