import datetime
import uuid
import os

def get_uuid():
    """
    return uuid string
    """
    return str(uuid.uuid4())


def get_date():
    """
    return date string
    """
    return str(datetime.datetime.utcnow(
    ).strftime("%Y-%m-%d"))


def get_time():
    """
    return time string
    """
    return str(datetime.datetime.utcnow().strftime("%H:%M:%S"))


def get_home_dir():
    """
    return home dir
    """
    return os.path.expanduser("~")


def get_fatoora_base_url(current_env):
    """
    get current base url
    """
    if current_env == "sandbox":
        return 'https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/'
    elif current_env == "simulation":
        return "https://gw-fatoora.zatca.gov.sa/e-invoicing/simulation/"

    return "https://gw-fatoora.zatca.gov.sa/e-invoicing/core/"

