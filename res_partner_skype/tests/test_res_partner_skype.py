import odoo.tests
from odoo.api import Environment


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_res_partner_skype(self):
        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        cr = self.registry.cursor()
        env = Environment(cr, self.uid, {})
        env['ir.module.module'].search([('name', '=', 'res_partner_skype')], limit=1).state = 'installed'
        cr.release()
        env['res.partner'].search(([('id', '=', 9)]), limit=1).write({
            'skype': 'skype_test',
        })

        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        self.phantom_js("/web",
                        "odoo.__DEBUG__.services['web_tour.tour'].run('tour_res_partner_skype', 1000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.tour_res_partner_skype.ready",
                        login="admin", timeout=300)
