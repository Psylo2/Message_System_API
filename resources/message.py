from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from libs.strings import gettext
from libs.inputs_validation import valid_username, valid_msg_inputs

from models.message import MessageModel
from models.user import UserModel
from models.log import LogModel

"""Messages:     [*] send msg
                 [*] read msg
                 [*] display all unread Msg Titles
                 [*] display all read Msg Titles
                 [*] display all received msg Titles
                 [*] display all sent msg Titles"""


class MessageSend(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('send_to',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))
    parser.add_argument('body',
                        type=str,
                        required=True,
                        help=gettext("field_not_blank"))

    @classmethod
    @jwt_required
    def post(cls):
        """Send Message:     [*] Validate inputs
                             [*] find user receive message by idx
                             [*] Send MSG"""
        data = MessageSend.parser.parse_args()
        if not valid_username(data['send_to']):
            return {'message': gettext("username_error")}, 400
        if not valid_msg_inputs(data['title']) or not valid_msg_inputs(data['body']):
            return {'message': gettext("input_error")}, 400

        user = UserModel.find_by_username(data['send_to'])
        if user is None:
            return {'message': gettext("user_not_found")}, 401

        msg = MessageModel(get_jwt_identity(), user.idx,
                           data['title'], data['body'])
        msg.save_to_db()

        LogModel(get_jwt_identity(),
                 f"Msg Sent to User: [{user.idx}]",
                 'L').save_to_db()
        return {'message': gettext("msg_sent")}, 200


class MessageRead(Resource):
    @classmethod
    @jwt_required
    def get(cls, msg_id: int):
        """Read Message:     [*] check MSG, Sender, Receiver exists.
                             [*] Verify MSG belongs to Reader identity
                             [*] only receiver set mark as read
                             [*] Display MSG"""
        msg = MessageModel.find_msg_by_id(msg_id)
        try:
            sender = UserModel.find_by_id(msg.from_user)
            receiver = UserModel.find_by_id(msg.to_user)
        except Exception:
            return {"message": gettext("invalid_credentials")}, 401
        if get_jwt_identity() == sender.idx:
            LogModel(get_jwt_identity(),
                     f"Read Msg to User: [{receiver.idx}]",
                     'L').save_to_db()
            return msg.json_read_msg(sender.name, receiver.name, False), 200
        if get_jwt_identity() == receiver.idx:
            LogModel(get_jwt_identity(),
                     f"Read Msg from User: [{sender.idx}], Mark as READ",
                     'L').save_to_db()
            return msg.json_read_msg(sender.name, receiver.name, True), 200
        return {"message": gettext("invalid_credentials")}, 401


class MessageAllUnread(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Unread Message:
                                  [*] Display all Unread MSGs of User by identity"""
        LogModel(get_jwt_identity(),
                 f"Display all Unread MSG titles",
                 'L').save_to_db()
        return [msg.json_only_titles(msg.from_user, msg.to_user) for msg in
                MessageModel.find_all_unread(get_jwt_identity())]


class MessageAllRead(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Read Message:
                                  [*] Display all Read MSGs of User by identity"""
        LogModel(get_jwt_identity(),
                 f"Display all Read MSG titles",
                 'L').save_to_db()
        return [msg.json_only_titles(msg.from_user, msg.to_user) for msg in
                MessageModel.find_all_read(get_jwt_identity())]


class MessageAllReceived(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Received Message:
                                  [*] Display all Received MSGs of User by identity"""
        LogModel(get_jwt_identity(),
                 f"Display all Received MSG titles",
                 'L').save_to_db()
        return [msg.json_only_titles(msg.from_user, msg.to_user) for msg in
                MessageModel.find_all_received(get_jwt_identity())]


class MessageAllSent(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Sent Message:
                                  [*] Display all Sent MSGs of User by identity"""
        LogModel(get_jwt_identity(),
                 f"Display all Sent MSG titles",
                 'L').save_to_db()
        return [msg.json_only_titles(msg.from_user, msg.to_user) for msg in
                MessageModel.find_all_sent(get_jwt_identity())]


class MessageReadByRec(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """All Been Read Message:
                                  [*] Display all Been Read MSGs of User by identity by other others."""
        LogModel(get_jwt_identity(),
                 f"Display all confirmed Read MSG titles",
                 'L').save_to_db()
        return [msg.json_only_titles(msg.from_user, msg.to_user) for msg in
                MessageModel.find_sent_n_read()]
