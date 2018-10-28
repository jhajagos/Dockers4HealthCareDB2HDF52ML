import sqlalchemy as sa
import json


def main(connection_string, schemas):

    engine = sa.create_engine(connection_string)

    with engine.connect() as connection:
        for schema in schemas:
            connection.execute("create schema if not exists %s" % schema)


if __name__ == "__main__":

    with open("../config/ps_2_cdm_config.json") as f:
        config = json.load(f)

    main(config["connection_uri"], ["ohdsi_cdm", "prepared_source"])