from app.models.operator_access_permissions import Operator_Access_Permissions


class Methods_Operator_Access_Permissions:
    @classmethod
    def get_access_permissions(cls, id):
        access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=id)
        auth_permissions = {}
        counter = 0
        for access_permission in access_permissions:
            auth_permissions[
                counter] = access_permission.operator_access_permission_name
            counter = counter + 1
        return auth_permissions
