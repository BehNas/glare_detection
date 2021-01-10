class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def validate_request(input_data):
    metadata = ['lat', 'lon', 'epoch', 'orientation']
    for data in metadata:
        if data not in input_data:
            raise InvalidUsage('Error: Missing input %s' % data, status_code=422)

        if data == 'lat' and (input_data[data] > 90 or input_data[data] < 0):
            raise InvalidUsage('Error: Latitude out of range', status_code=416)

        if data == 'lon' and (input_data[data] < -180 or input_data[data] > 180):
            raise InvalidUsage('Error: Longitude out of range', status_code=416)

        if data == 'orientation' and (input_data[data] < -180 or input_data[data] > 180):
            raise InvalidUsage('Error: orientation out of range', status_code=416)
