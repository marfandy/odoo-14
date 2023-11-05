from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestMaterialApp(TransactionCase):
    def setUp(self):
        super(TestMaterialApp, self).setUp()
        self.supplier1 = self.env["master.supplier"].create(
            {
                "name": "Supplier Test 1",
            }
        )

        self.supplier2 = self.env["master.supplier"].create(
            {
                "name": "Supplier Test 2",
            }
        )

        self.material = self.env["master.material"].create(
            {
                "code": "M001",
                "name": "Material 1",
                "type": "fabric",
                "buy_price": 150.0,
                "supplier_id": self.supplier1.id,
            }
        )

    def test_create_material(self):
        material = self.material

        self.assertEqual(material.code, "M001")
        self.assertEqual(material.name, "Material 1")
        self.assertEqual(material.type, "fabric")
        self.assertEqual(material.buy_price, 150.0)
        self.assertEqual(material.supplier_id, self.supplier1)

    def test_update_material(self):
        self.material.write(
            {
                "code": "M002",
                "name": "Updated Material",
                "buy_price": 200.0,
            }
        )

        updated_material = self.env["master.material"].search(
            [("id", "=", self.material.id)]
        )

        self.assertEqual(updated_material.code, "M002")
        self.assertEqual(updated_material.name, "Updated Material")
        self.assertEqual(updated_material.buy_price, 200.0)

    def test_delete_material(self):
        self.material.unlink()
        deleted_material = self.env["master.material"].search(
            [("id", "=", self.material.id)]
        )
        self.assertFalse(deleted_material)

    def test_filter_material_by_type(self):
        self.env["master.material"].create(
            {
                "code": "M002",
                "name": "Material 2",
                "type": "jeans",
                "buy_price": 200.0,
                "supplier_id": self.supplier1.id,
            }
        )

        self.env["master.material"].create(
            {
                "code": "M003",
                "name": "Material 3",
                "type": "cotton",
                "buy_price": 175.0,
                "supplier_id": self.supplier1.id,
            }
        )
        filtered_materials1 = self.env["master.material"].search(
            [("type", "=", "jeans")]
        )

        self.assertEqual(len(filtered_materials1), 1)
        self.assertEqual(filtered_materials1[0].name, "Material 2")

        filtered_materials2 = self.env["master.material"].search(
            [("type", "=", "cotton")]
        )

        self.assertEqual(len(filtered_materials2), 1)
        self.assertEqual(filtered_materials2[0].name, "Material 3")

        filtered_materials3 = self.env["master.material"].search(
            [("type", "=", "fabric")]
        )

        self.assertEqual(len(filtered_materials3), 1)
        self.assertEqual(filtered_materials3[0].name, "Material 1")

    def test_filter_material_by_invalid_type(self):
        filtered_materials = self.env["master.material"].search(
            [("type", "=", "nonexistent_type")]
        )

        self.assertEqual(len(filtered_materials), 0)

    def test_negative_buy_price(self):
        with self.assertRaises(ValidationError) as context:
            self.env["master.material"].create(
                {
                    "code": "M001",
                    "name": "Material 1",
                    "type": "fabric",
                    "buy_price": 50,
                    "supplier_id": self.supplier2.id,
                }
            )

        self.assertTrue(
            "Buy Price should be greater than or equal to 100."
            in str(context.exception)
        )
