from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

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
            self.bank_account_balance = (obj.browse(cr, uid, journal_obj[0])).default_debit_account_id.compute_account_balance()
        else:
            self.bank_account_balance = -42

class account_with_balance(models.Model):
    _inherit = ['account.account']

    @api.multi
    def compute_account_balance(self):
        cr = self.env.cr
        uid = self.env.user.id
        obj = self.pool.get('account.move.line')
        moves = obj.search(cr, uid, [('account_id', '=', self.id)])
        debit = 0
        credit = 0
        if len(moves) > 0:
            for move in obj.browse(cr, uid, moves):
                debit += move.debit
                credit += move.credit
        balance = debit - credit
        return balance