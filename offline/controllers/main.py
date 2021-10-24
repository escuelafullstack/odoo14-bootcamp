import json

from odoo import http, fields
from odoo.http import request


class OfflineController(http.Controller):
    @http.route(['/offline'], type='http', auth='user', website=True)
    def home(self, *args, **kwargs):

        return request.render('offline.home')

    @http.route(['/getPartners'], type='http', auth='user', website=True)
    def getPartners(self, *args, **kwargs):
        domain = []
        partner_objs = request.env['res.partner'].search(domain)
        data = []
        for partner in partner_objs:
            data.append({
                'id': partner.id,
                'name': partner.name,
                'create_date': fields.Datetime.to_string(partner.create_date),
                'write_date': fields.Datetime.to_string(partner.write_date),
            })
        return json.dumps(data)
