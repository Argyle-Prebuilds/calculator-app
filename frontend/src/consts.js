export const LOGIN_INITIAL_STATE = {
  email: '',
  password: '',
}

export const PASSWORD_RESET_INITIAL_STATE = {
  email: '',
}

export const PASSWORD_INITIAL_STATE = {
  password: '',
  password_confirmed: '',
}

export const PAGINATION_INITIAL_STATE = {
  count: 0,
  next: '',
  previous: ''
}

export const PAGE_LIMIT = 3

export const API_KEYS_INITIAL_STATE = {
  client_id: '',
  client_secret: '',
  plugin_key: '',
  is_sandbox_mode: false
}

export const FORMAT_MONEY_FIELDS = [
  'base_pay',
  'overtime',
  'commission',
  'bonuses',
  'gross_pay',
  'taxes',
  'deductions',
  'net_pay',
  'gross_monthly',
  'gross_monthly_with_last_year'
]

export const RATE_FIELDS = [
  'base_pay',
  'rate_of_pay',
]

export const CALCULATION_TOOLTIPS = {
  "total_days": {
    "last_year_total": "the maximum value of employers",
    "ytd_total": "the maximum value of employers",
    "projected_total": "the maximum value of employers",
    "companies": {
      "last_year_total": "termination date (or 31 December last year) - hire date (or 1 January last year)",
      "ytd_total": "today - hire date (or 1 January current year)",
      "projected_total": "termination date (or 31 December current year) - hire date (or 1 January current year)",
    }
  },
  "pay_frequency": {
    "last_year_total": "difference between payments",
    "ytd_total": "difference between payments",
    "projected_total": "YTD value",
    "companies": {
      "last_year_total": "difference between payments",
      "ytd_total": "difference between payments",
      "projected_total": "YTD value",
    }
  },
  "rate_of_pay": {
    "last_year_total": "average of company pay rates",
    "ytd_total": "average of company pay rates",
    "projected_total": "YTD value",
    "companies": {
      "last_year_total": "gross pay / hours",
      "ytd_total": "gross pay / hours",
      "projected_total": "YTD value",
    }
  },
  "base_pay": {
    "last_year_total": "gross pay - bonuses - reimbursements - overtime",
    "ytd_total": "gross pay - bonuses - reimbursements - overtime",
    "projected_total": "YTD value * 12 / current month",
    "companies": {
      "last_year_total": "gross pay - bonuses - reimbursements - overtime",
      "ytd_total": "gross pay - bonuses - reimbursements - overtime",
      "projected_total": "YTD value * 12 / current month",
    }
  },
  "overtime": {
    "last_year_total": "overtime",
    "ytd_total": "overtime",
    "projected_total": "YTD overtime * 12 / current month",
    "companies": {
      "last_year_total": "overtime",
      "ytd_total": "overtime",
      "projected_total": "YTD overtime * 12 / current month",
    }
  },
  "commission": {
    "last_year_total": "commission",
    "ytd_total": "commission",
    "projected_total": "YTD commission * 12 / current month",
    "companies": {
      "last_year_total": "commission",
      "ytd_total": "commission",
      "projected_total": "YTD commission * 12 / current month",
    }
  },
  "bonuses": {
    "last_year_total": "bonuses",
    "ytd_total": "bonuses",
    "projected_total": "YTD bonuses * 12 / current month",
    "companies": {
      "last_year_total": "bonuses",
      "ytd_total": "bonuses",
      "projected_total": "YTD bonuses * 12 / current month",
    }
  },
  "reimbursements": {
    "last_year_total": "reimbursements",
    "ytd_total": "reimbursements",
    "projected_total": "YTD reimbursements * 12 / current month",
    "companies": {
      "last_year_total": "reimbursements",
      "ytd_total": "reimbursements",
      "projected_total": "YTD reimbursements * 12 / current month",
    }
  },
  "gross_pay": {
    "last_year_total": "gross pay",
    "ytd_total": "gross pay",
    "projected_total": "YTD gross pay * 12 / current month",
    "companies": {
      "last_year_total": "gross pay",
      "ytd_total": "gross pay",
      "projected_total": "YTD gross pay * 12 / current month",
    }
  },
  "net_pay": {
    "last_year_total": "net pay",
    "ytd_total": "net pay",
    "projected_total": "YTD net pay * 12 / current month",
    "companies": {
      "last_year_total": "net pay",
      "ytd_total": "net pay",
      "projected_total": "YTD net pay * 12 / current month",
    }
  },
  "taxes": {
    "last_year_total": "taxes",
    "ytd_total": "taxes",
    "projected_total": "YTD taxes * 12 / current month",
    "companies": {
      "last_year_total": "taxes",
      "ytd_total": "taxes",
      "projected_total": "YTD taxes * 12 / current month",
    }
  },
  "gross_monthly_with_last_year": {
    "last_year_total": "gross pay / 12",
    "ytd_total": "(last year gross pay + gross pay) / (12 + current month)",
    "projected_total": "YTD value",
    "companies": {
      "last_year_total": "gross pay / 12",
      "ytd_total": "(last year gross pay + gross pay) / (12 + current month)",
      "projected_total": "YTD value",
    }
  },
  "hours_per_week": {
    "last_year_total": "hours / total weeks",
    "ytd_total": "hours / total weeks",
    "projected_total": "YTD value",
    "companies": {
      "last_year_total": "hours / total weeks",
      "ytd_total": "hours / total weeks",
      "projected_total": "YTD value",
    }
  },
  "gross_monthly": {
    "last_year_total": "gross pay / 12",
    "ytd_total": "gross pay / current month",
    "projected_total": "YTD total",
    "companies": {
      "last_year_total": "gross pay / 12",
      "ytd_total": "gross pay / current month",
      "projected_total": "YTD total",
    }
  },
  "deductions": {
    "last_year_total": "deductions",
    "ytd_total": "deductions",
    "projected_total": "YTD deductions * 12 / current month",
    "companies": {
      "last_year_total": "deductions",
      "ytd_total": "deductions",
      "projected_total": "YTD deductions * 12 / current month",
    }
  },
}

