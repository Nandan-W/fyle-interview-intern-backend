from flask import Response, jsonify, make_response

class APIResponse(Response):
    @classmethod
    def respond(cls, data=None, error=None, message=None, status_code=200):
        response_data = {}
        if data is not None:
            response_data['data'] = data
        if error is not None:
            response_data['error'] = error
        if message is not None:
            response_data['message'] = message
        
        return make_response(jsonify(response_data), status_code)
