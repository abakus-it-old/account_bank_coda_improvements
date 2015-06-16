from openerp import models, fields, api

class account_next_sequence(models.Model):
    _inherit = ['account.bank.statement']
    bank_account_balance = fields.Float(compute='_compute_bank_account_balance', string="Bank account balance", store=False)
    
    @api.depends('journal_id')
    def _compute_bank_account_balance(self):
        cr = self.env.cr
        uid = self.env.user.id
        obj = self.pool.get('account.journal')
        journal_obj = obj.search(cr, uid, [('id', '=', self.journal_id.id)])
        if journal_obj:
            self.bank_account_balance = (obj.browse(cr, uid, journal_obj[0])).default_debit_account_id.balance
        else:
            self.bank_account_balance = -42