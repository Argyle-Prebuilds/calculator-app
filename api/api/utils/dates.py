import dateutil.parser


def get_date_from_str(datetime: str):
    return dateutil.parser.isoparse(datetime).date()
