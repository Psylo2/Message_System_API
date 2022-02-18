from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity


class MessageSend(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        self._parser = RequestParser()

        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        """Send Message:     [*] Validate inputs
                             [*] find user receive message by idx
                             [*] Send MSG"""
        self._parser.add_argument('send_to',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('title',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")
        self._parser.add_argument('body',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank.")

        data = self._parser.parse_args()
        try:
            response, status_code = self._handler.send_message(user_id=get_jwt_identity(),
                                                               message_data=data)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageRead(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self, msg_id: int):
        """Read Message:     [*] check MSG, Sender, Receiver exists.
                             [*] Verify MSG belongs to Reader identity
                             [*] only receiver set mark as read
                             [*] Display MSG"""
        try:
            response, status_code = self._handler.read_message(user_id=get_jwt_identity(),
                                                               message_id=msg_id)
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageAllUnread(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Unread Message:
                                  [*] Display all Unread MSGs of User by identity"""
        try:
            response, status_code = self._handler.get_all_unread_messages(user_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageAllRead(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Read Message:
                                  [*] Display all Read MSGs of User by identity"""
        try:
            response, status_code = self._handler.get_all_read_messages(user_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageAllReceived(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Received Message:
                                  [*] Display all Received MSGs of User by identity"""
        try:
            response, status_code = self._handler.get_all_received_messages(user_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageAllSent(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Sent Message:
                                  [*] Display all Sent MSGs of User by identity"""
        try:
            response, status_code = self._handler.get_all_sent_messages(user_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400


class MessageReadByRec(Resource):
    def __init__(self, *args, handler, **kwargs):
        self._handler = handler
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        """All Been Read Message:
                                  [*] Display all MSG's Been Read of User by identity by other others."""
        try:
            response, status_code = self._handler.get_all_read_by_receiver_messages(user_id=get_jwt_identity())
            return response, status_code
        except Exception as err:
            return {"message": "Error occurred",
                    "details": err}, 400
