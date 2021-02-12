import logging
from quickchart import QuickChart

qc = QuickChart()
qc.width = 500
qc.height = 300
qc.device_pixel_ratio = 2.0
config = {
      "type": "bar",
      "data": {
        "labels": [],
        "datasets": [
          {
            "label": "Fail",
            "backgroundColor": "rgba(255, 99, 132, 0.5)",
            "borderColor": "rgb(255, 99, 132)",
            "borderWidth": 1,
            "data": []
          },
          {
            "label": "Pass",
            "backgroundColor": "rgba(54, 162, 235, 0.5)",
            "borderColor": "rgb(54, 162, 235)",
            "borderWidth": 1,
            "data": []
          }
        ]
      },
      "options": {
        "responsive": True,
        "legend": {
          "position": "top"
        },
        "title": {
          "display": True,
          "text": "Automatizace aplikace RWA pomoci robot framework, python a selenium"
        }
      }
    }


def report_results(cfg):
    """ Zjednoduseny priklad volani reportingoveho nastroje v cloudu. Metoda vygeneruje URL a QR kod reportu s vysledky
        posledniho behu vsech testu v testovaci sade. Reportovaci nastroj zobrazi vzdy jen posledni beh, neda se nad
        tim stavet zadna analytika, k tomu slouzi jine nastroje. Priklad vyuziva Python knihovnu pro generovani
        statickych reportu -> https://quickchart.io/
    """
    qc.config = cfg
    chart_url = qc.get_url()    # odesle pozadavek na https://quickchart.io/ a vygeneruje staticky report
    chart_qr_code = f'https://quickchart.io/qr?text={chart_url}&size=250'
    # URL reportu
    logging.warning(f'URL reportu: {chart_url}')
    # QR kod reportu
    logging.warning(f'QR kod reportu: {chart_qr_code}')
