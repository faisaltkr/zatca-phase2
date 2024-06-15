import tempfile


def get_config(config_dict):
    """
    create temporary config file from json and return the temporary
    file path
    """
    config_content = ""
    for section, values in config_dict.items():
        if section == "oid_section":
            config_content += f"oid_section = {values}\n\n"
        else:
            config_content += f"[ {section} ]\n"
            for key, value in values.items():
                config_content += f"{key} = {value}\n"
            config_content += "\n"

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.cnf') as temp_config:
        temp_config_path = temp_config.name
        temp_config.write(config_content)

    
    return temp_config_path
