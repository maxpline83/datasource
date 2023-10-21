from flask import Flask, request, render_template, jsonify
import requests
import logging
from pytrends.request import TrendReq

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home_page():
    google_tag = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MJH545RKJV"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-MJH545RKJV');
    </script>
    """
    return google_tag + "Welcome to My Website"

@app.route('/app-dashboard', methods=['GET'])
def app_dashboard():
    return """
    <form method="GET" action="/show-analytics-dashboard">
        <input type="submit" value="Display App's Analytics Dashboard">
    </form>
    <form method="GET" action="/check-analytics-request-cookies">
        <input type="submit" value="Check Analytics Request Cookies">
    </form>
    """

@app.route('/show-analytics-dashboard', methods=['GET'])
def show_analytics_dashboard():
    analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    try:
        response = requests.get(analytics_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error accessing the Analytics Dashboard: {str(e)}"

@app.route('/check-analytics-request-cookies', methods=['GET'])
def check_analytics_request_cookies():
    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status()
        cookies = response.cookies
        cookies_html = "<h2>Google Analytics Request Cookies:</h2><ul>"
        for cookie in cookies:
            cookies_html += f"<li><strong>{cookie.name}:</strong> {cookie.value}</li>"
        cookies_html += "</ul>"
        return cookies_html
    except requests.exceptions.RequestException as e:
        return f"Error checking Google Analytics Request Cookies: {str(e)}"

@app.route("/logger", methods=['GET', 'POST'])
def log_page():
    log_msg = "You are connected to the log page"
    app.logger.info(log_msg)

    if request.method == 'POST':
        text_from_textbox = request.form['textbox']
        browser_log = f"""
        <script>
            console.log('Web browser console: You are connected to the log page');
            console.log('Text from the text box: {text_from_textbox}');
        </script>
        """
    else:
        browser_log = """
        <script>
            console.log('Web browser console: You are connected to the log page');
        </script>
        """

    form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Submit">
        <button type="button" onclick="makeGoogleRequest()">Make a Google Request</button>
    </form>
    """
    return log_msg + browser_log + form

@app.route('/perform-google-request-cookies', methods=['GET'])
def perform_google_request_cookies():
    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status()
        cookies = response.cookies
        return render_template('cookies.html', cookies=cookies)
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics Cookies request: {str(e)}"

@app.route('/chart_data')
def chart_data():
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ["Fortnite", "League of Legends"]
    pytrends.build_payload(keywords, timeframe='today 12-m', geo='US')
    interest_over_time_df = pytrends.interest_over_time()

    data = {
        'dates': interest_over_time_df.index.strftime('%Y-%m-%d').tolist(),
        'Fortnite': interest_over_time_df['Fortnite'].tolist(),
        'LeagueOfLegends': interest_over_time_df['League of Legends'].tolist()
    }

    return jsonify(data)

@app.route('/chart_data_render')
def index():
    return render_template('chart_trend_data.html')

if __name__ == "__main__":
    app.run(debug=True)
