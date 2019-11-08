# -*- coding:utf-8 -*-

from flask import request

from api.lib.decorator import args_required
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resource import ResourceGroupCRUD
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class ResourceView(APIView):
    url_prefix = ("/resources", "/resources/<int:resource_id>")

    @args_required('app_id')
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')

        numfound, res = ResourceCRUD.search(q, app_id, page, page_size)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            resources=[i.to_dict() for i in res])

    @args_required('name')
    @args_required('type_id')
    @args_required('app_id')
    def post(self):
        name = request.values.get('name')
        type_id = request.values.get('type_id')
        app_id = request.values.get('app_id')

        resource = ResourceCRUD.add(name, type_id, app_id)

        return self.jsonify(resource.to_dict())

    @args_required('name')
    def put(self, resource_id):
        name = request.values.get('name')

        resource = ResourceCRUD.update(resource_id, name)

        return self.jsonify(resource.to_dict())

    def delete(self, resource_id):
        ResourceCRUD.delete(resource_id)

        return self.jsonify(resource_id=resource_id)


class ResourceGroupView(APIView):
    url_prefix = ("/resource_groups", "/resource_groups/<int:group_id>")

    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')

        numfound, res = ResourceGroupCRUD.search(q, app_id, page, page_size)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            groups=[i.to_dict() for i in res])

    @args_required('name')
    @args_required('type_id')
    @args_required('app_id')
    def post(self):
        name = request.values.get('name')
        type_id = request.values.get('type_id')
        app_id = request.values.get('app_id')

        group = ResourceGroupCRUD.add(name, type_id, app_id)

        return self.jsonify(group.to_dict())

    @args_required('items')
    def put(self, group_id):
        items = handle_arg_list(request.values.get("items"))

        ResourceGroupCRUD.update(group_id, items)

        items = ResourceGroupCRUD.get_items(group_id)

        return self.jsonify(items)

    def delete(self, group_id):
        ResourceGroupCRUD.delete(group_id)

        return self.jsonify(group_id=group_id)


class ResourceGroupItemsView(APIView):
    url_prefix = "/resource_groups/<int:group_id>/items"

    def get(self, group_id):
        items = ResourceGroupCRUD.get_items(group_id)

        return self.jsonify(items)
