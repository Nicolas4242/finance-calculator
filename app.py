from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def loan():
    return render_template('loan.html', request_form={}, loan_result=None, monlthly_loan_result=None)
# def investment():
#     return render_template('investment.html', request_form={}, interest_result=None)
# def retirement_savings():
#     return render_template('retirement_savings.html', request_form={}, monthly_saving_needed=None,
#         total_savings_estimate=None, future_result=None)
# def networth():
#     return render_template('networth.html', request_form={}, networth_result=None)

@app.route('/calculator', methods=['GET','POST'])
def calculator():
    interest_result = None
    yearly_values = []
    request_form = {}
    year_labels = []
    if request.method == 'POST':
        amount = float(request.form['amount'])
        rate = float(request.form['rate'])
        years = int(request.form['years'])
        monthly_invest = float(request.form['monthly_investment'])
        year_labels = list(range(1, years + 1))

        request_form = {
            "amount": amount,
            "rate": rate,
            "years": years,
            "monthly_investment": monthly_invest
        }

        r = rate / 100
        n = 12
        P = amount
        PMT = monthly_invest

        for year in range(1, years + 1):
            compound = P * (1 + r / n) ** (n * year)
            contribution = PMT * (((1 + r / n) ** (n * year) - 1) / (r / n))
            total = compound + contribution
            yearly_values.append(round(total, 2))

        interest_result = yearly_values[-1]

    return render_template(
        'investment.html',
        interest_result=interest_result,
        request_form=request_form,
        yearly_values=yearly_values,
        year_labels=year_labels
    )

@app.route('/loan', methods=['GET','POST'])
def loan_calculator():
    loan_result = None
    monthly_pay = None
    request_form = {}
    if request.method == 'POST':
        amount = float(request.form['loan_amount'])
        rate = float(request.form['interest_rate'])/(12*100)
        rate_real = float(request.form['interest_rate'])
        month = float(request.form['years_loan'])* 12
        years = float(request.form['years_loan'])
        request_form = {"loan_amount": amount, "interest_rate": rate_real, "years_loan": years}
        monthly_pay = amount * rate / (1 - (1 + rate) ** -month)
        loan_result = round(monthly_pay * month, 2)
        monthly_pay = round(monthly_pay, 2)
 
    # Calcul du coût total des intérêts
    
    return render_template('loan.html', loan_result=loan_result, monthly_loan_result = monthly_pay, active ='loan', request_form=request_form)

@app.route('/retirement_savings', methods=['GET', 'POST'])
def retirement_savings():
    monthly_saving_needed = None
    total_savings_estimate = None
    future_result = None  # For template
    request_form = {}

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'retirement_payment':
            # Monthly savings calculator
            try:
                goal_amount = float(request.form.get('amount', 0) or 0)
                current_savings = float(request.form.get('current', 0) or 0)
                annual_rate = float(request.form.get('rate', 0) or 0)
                years = float(request.form.get('years', 0) or 0)
            except ValueError:
                return render_template('retirement_savings.html',
                                       monthly_saving_needed=None,
                                       total_savings_estimate=None,
                                       request_form=request.form,
                                       active='retirement',
                                       error="Please enter valid numeric values.")

            monthly_rate = annual_rate / 100 / 12
            months = years * 12

            request_form = {
                "amount": goal_amount,
                "current": current_savings,
                "rate": annual_rate,
                "years": years,
            }

            if monthly_rate != 0 and months > 0:
                fv_current = current_savings * (1 + monthly_rate) ** months
                monthly_saving_needed = round(
                    (goal_amount - fv_current) * monthly_rate / ((1 + monthly_rate) ** months - 1),
                    2
                )
            else:
                monthly_saving_needed = round((goal_amount - current_savings) / months if months > 0 else 0, 2)

        elif form_type == 'retirement_growth':
            # Total savings growth calculator
            try:
                monthly_payment = float(request.form.get('monthly', 0) or 0)
                current_savings = float(request.form.get('current_growth', 0) or 0)
                annual_rate = float(request.form.get('rate_growth', 0) or 0)
                years = float(request.form.get('years_growth', 0) or 0)
            except ValueError:
                return render_template('retirement_savings.html',
                                       monthly_saving_needed=None,
                                       total_savings_estimate=None,
                                       request_form=request.form,
                                       active='retirement',
                                       error="Please enter valid numeric values.")

            monthly_rate = annual_rate / 100 / 12
            months = years * 12

            request_form = {
                "monthly": monthly_payment,
                "current_growth": current_savings,
                "rate_growth": annual_rate,
                "years_growth": years,
            }

            if monthly_rate != 0 and months > 0:
                future_result = round(
                    current_savings * (1 + monthly_rate) ** months +
                    monthly_payment * ((1 + monthly_rate) ** months - 1) / monthly_rate,
                    2
                )
            else:
                future_result = round(current_savings + monthly_payment * months, 2)

    return render_template('retirement_savings.html',
                           monthly_saving_needed=monthly_saving_needed,
                           future_result=future_result,
                           request_form=request_form,
                           active='retirement')
@app.route('/networth', methods=['GET','POST'])
def networth():
    networth_result = None
    request_form = {}
    if request.method == 'POST':
        real_estate = float(request.form['real_estate'])
        business = float(request.form['Business'])
        bank = float(request.form['Bank'])
        stocks = float(request.form['Stock'])
        Crypto = float(request.form['Crypto'])
        cash = float(request.form['Cash'])
        Debt = float(request.form['Debt'])
        credit = float(request.form['Credit'])
        networth_result = round(real_estate + business + bank + stocks + Crypto + cash - Debt - credit, 2)
        request_form = {
            "real_estate": real_estate,
            "Business": business,
            "Bank": bank,
            "Stock": stocks,
            "Crypto": Crypto,
            "Cash": cash,
            "Debt": Debt,
            "Credit": credit
        }
    return render_template('networth.html', networth_result=networth_result, request_form=request_form, active='networth')

from flask import Response
from datetime import date

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = [
        "https://finance-calculator-645x.onrender.com/",
        "https://finance-calculator-645x.onrender.com/calculator",
        "https://finance-calculator-645x.onrender.com/loan",
        "https://finance-calculator-645x.onrender.com/retirement_savings",
        "https://finance-calculator-645x.onrender.com/networth"
    ]
    today = date.today().isoformat()

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f"  <url>\n"
        xml += f"    <loc>{page}</loc>\n"
        xml += f"    <lastmod>{today}</lastmod>\n"
        xml += f"    <changefreq>monthly</changefreq>\n"
        xml += f"    <priority>0.8</priority>\n"
        xml += f"  </url>\n"
    xml += "</urlset>"

    return Response(xml, mimetype='text/xml')

@app.route('/robots.txt')
def robots_txt():
    content = "User-agent: *\nAllow: /\nSitemap: https://finance-calculator-645x.onrender.com/sitemap.xml\n"
    return Response(content, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=False)
