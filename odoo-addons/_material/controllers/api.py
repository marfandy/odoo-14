import json

from odoo import http
from odoo.http import Response, request


class MaterialController(http.Controller):
    @http.route("/materials", auth="public", methods=["GET"], csrf=False)
    def list_materials(self, **params):
        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))

        offset = (page - 1) * limit

        query_filter = []

        if params.get("type"):
            query_filter.append(("type", "=", params.get("type")))

        materials = (
            request.env["master.material"]
            .sudo()
            .search(query_filter, offset=offset, limit=limit)
        )

        response_data = []
        for data in materials:
            response_data.append(
                {
                    "id": data.id,
                    "code": data.code,
                    "name": data.name,
                    "type": data.type,
                    "buy_price": data.buy_price,
                    "supplier": {
                        "id": data.supplier_id.id,
                        "name": data.supplier_id.name,
                    },
                }
            )

        total_data = request.env["master.material"].sudo().search_count([])

        response = {
            "message": "success",
            "data": response_data,
            "page": page,
            "limit": limit,
            "total": total_data,
        }
        return Response(
            json.dumps(response), status=200, content_type="application/json"
        )

    @http.route("/materials/<int:id>", auth="public", methods=["GET"], csrf=False)
    def get_material(self, id, **params):
        try:
            data = request.env["master.material"].sudo().browse(id)
            response = {
                "message": "success",
                "data": {
                    "id": data.id,
                    "code": data.code,
                    "name": data.name,
                    "type": data.type,
                    "buy_price": data.buy_price,
                    "supplier": {
                        "id": data.supplier_id.id,
                        "name": data.supplier_id.name,
                    },
                },
            }
            return Response(
                json.dumps(response), status=200, content_type="application/json"
            )
        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route("/materials/<int:id>", auth="public", methods=["PUT"], csrf=False)
    def update_material(self, id, **params):
        try:
            data = request.env["master.material"].browse(id)
            data_update = {}
            if params.get("code"):
                data_update["code"] = params.get("code")

            if params.get("name"):
                data_update["name"] = params.get("name")

            if params.get("type"):
                data_update["type"] = params.get("type")

            if params.get("buy_price"):
                data_update["buy_price"] = params.get("buy_price")

            if params.get("supplier_id"):
                supplier = request.env["master.supplier"].browse(
                    params.get("supplier_id")
                )
                data_update["supplier_id"] = supplier.id

            data.write(params)
            return http.Response(
                json.dumps({"message": "data updated successfully"}),
                status=200,
                content_type="application/json",
            )
        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route("/materials/<int:id>", auth="public", methods=["DELETE"], csrf=False)
    def delete_material(self, id):
        try:
            data = request.env["master.material"].browse(id)
            data.unlink()
            return http.Response(
                json.dumps({"message": "data deleted successfully"}),
                content_type="application/json",
            )
        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )
