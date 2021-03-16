import moment from "moment";

export const formatMoney = (amount) => {
  // Formatting amount to US currency format: $123,456.78
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  })
  return formatter.format(amount)
}

export const formatDate = (date) => {
  return moment(date).format("MMM Do, YYYY")
}

export const formatRate = (value) => {
  return "$" + value + '/hr'
}

