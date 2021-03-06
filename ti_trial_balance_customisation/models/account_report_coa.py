# -*-coding: utf-8 -*-

import logging
from odoo import models, api, _

_logger = logging.getLogger(__name__)


class ChartOfAccountReport(models.AbstractModel):
    _inherit = "account.coa.report"

    @api.model
    def _get_columns(self, options):
        """
        Override the method to pass only single column "Balance" instead of Debit/Credit
        """

        header1 = [
            {'name': '', 'style': 'width:40%'},
            {'name': _('Initial Balance'), 'class': 'number', 'colspan': 1},
        ] + [
            {'name': period['string'], 'class': 'number', 'colspan': 1}
            for period in reversed(options['comparison'].get('periods', []))
        ] + [
            {'name': options['date']['string'], 'class': 'number', 'colspan': 1},
            {'name': _('Total'), 'class': 'number', 'colspan': 1},
        ]
        header2 = [
            {'name': '', 'style': 'width:40%'},
            {'name': _("Balance"), 'class': 'number o_account_coa_column_contrast'}
        ]
        if options.get('comparison') and options['comparison'].get('periods'):
            header2 += [
            {'name': _("Balance"), 'class': 'number o_account_coa_column_contrast'}
            ] * len(options['comparison']['periods'])
        header2 += [
            {'name': _("Balance"), 'class': 'number o_account_coa_column_contrast'},
            {'name': _("Balance"), 'class': 'number o_account_coa_column_contrast'}
        ]
        return [header1, header2]

    @api.model
    def _get_lines(self, options, line_id=None):
        """
        Override the default method such that we pass single balance value in trial report instead of Debit/Credit
        """

        # Create new options with 'unfold_all' to compute the initial balances.
        # Then, the '_do_query' will compute all sums/unaffected earnings/initial balances for all comparisons.
        new_options = options.copy()
        new_options['unfold_all'] = True
        options_list = self._get_options_periods_list(new_options)
        accounts_results, taxes_results = self.env['account.general.ledger']._do_query(options_list, fetch_lines=False)

        lines = []
        totals = [0.0] * (1 * (len(options_list) + 2))

        # Add lines, one per account.account record.
        for account, periods_results in accounts_results:
            sums = []
            account_balance = 0.0
            for i, period_values in enumerate(reversed(periods_results)):
                account_sum = period_values.get('sum', {})
                account_un_earn = period_values.get('unaffected_earnings', {})
                account_init_bal = period_values.get('initial_balance', {})

                if i == 0:
                    # Append the initial balances.
                    initial_balance = account_init_bal.get('balance', 0.0) + account_un_earn.get('balance', 0.0)
                    sums += [
                        initial_balance or 0.0  # initial balance comes as a single value from the last year and it's sinle value displayed based on the 
                    ]
                    account_balance += initial_balance

                # Append the debit/credit columns.
                debit = account_sum.get('debit', 0.0) - account_init_bal.get('debit', 0.0)
                credit = account_sum.get('credit', 0.0) - account_init_bal.get('credit', 0.0)
                account_balance += debit - credit
                
                # Adding the Balance in the sums list
                sums.append(debit - credit)

            # Append the totals.
            sums += [
                account_balance or 0.0
            ]

            # account.account report line.
            columns = []
            for i, value in enumerate(sums):
                # Update totals.
                totals[i] += value

                # Create columns.
                columns.append({'name': self.format_value(value, blank_if_zero=True), 'class': 'number', 'no_format_name': value})

            name = account.name_get()[0][1]

            lines.append({
                'id': account.id,
                'name': name,
                'title_hover': name,
                'columns': columns,
                'unfoldable': False,
                'caret_options': 'account.account',
                'class': 'o_account_searchable_line o_account_coa_column_contrast',
            })

        # Total report line.
        lines.append({
             'id': 'grouped_accounts_total',
             'name': _('Total'),
             'class': 'total o_account_coa_column_contrast',
             'columns': [{'name': self.format_value(round(total, 3)), 'class': 'number'} for total in totals],
             'level': 1,
        })

        return lines