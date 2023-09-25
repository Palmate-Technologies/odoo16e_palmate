from odoo import models, fields


class ModuleDetails(models.Model):
    _name = "module.available"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True)
    purpose = fields.Char(string="Purpose")
    category_id = fields.Many2one("module.available.category", string="Category")
    developed_by = fields.Char(string="Developed By")
    version_ids = fields.Many2many("module.available.version", string="Version")
    repo_link = fields.Text(string="Repository")
    description = fields.Text(string="Description")


class Category(models.Model):
    _name = "module.available.category"

    name = fields.Char(string="Name")


class Version(models.Model):
    _name = "module.available.version"

    name = fields.Char(string="Name")