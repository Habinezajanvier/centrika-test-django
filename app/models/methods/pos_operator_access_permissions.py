from app.models.pos_operator_access_permissions import Pos_Operator_Access_Permissions


class Methods_Pos_Operator_Access_Permissions:
    @classmethod
    def get_pos_access_permissions(cls, id):
        pos_access_permissions = Pos_Operator_Access_Permissions.objects.filter(
            pos_operator_access_permission_operator_id=id)
        auth_permissions = {}
        counter = 0
        for pos_access_permission in pos_access_permissions:
            auth_permissions[
                counter] = pos_access_permission.pos_operator_access_permission_name
            counter = counter + 1
        return auth_permissions
