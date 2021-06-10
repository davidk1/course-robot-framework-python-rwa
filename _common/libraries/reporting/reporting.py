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


def report_results(test_names, test_statuses):
    """ Zjednoduseny priklad volani reportingoveho nastroje v cloudu. Metoda vygeneruje URL a QR kod reportu s vysledky
        posledniho behu vsech testu v testovaci sade. Reportovaci nastroj zobrazi vzdy jen posledni beh, neda se nad
        tim stavet zadna analytika, k tomu slouzi jine nastroje. Priklad vyuziva Python knihovnu pro generovani
        statickych reportu -> https://quickchart.io/
    """
    qc.config = _prepare_cfg_for_reporting_tool(test_names, test_statuses)
    chart_url = qc.get_url()    # vygeneruje url statickeho reportu
    chart_qr_code = f'https://quickchart.io/qr?text={chart_url}&size=250'
    # URL reportu
    logging.warning(f'reporting-url: {chart_url}')
    # QR kod reportu
    logging.warning(f'reporting-qr-kod: {chart_qr_code}')


def _prepare_cfg_for_reporting_tool(test_names, test_statuses):
    """Metoda vraci upravenou vychozi konfiguraci reportingoveho nastroje doplnenou o nazvy a stavy vsech
    spustenych testu.
    """
    cfg = config    # nacte vychozi(default) konfiguraci reportovaciho nastroje
    # ve vychozi(default) konfiguraci upravi jmena testu a jejich stavy (PASS / FAIL)
    for i in range(len(test_names)):
        cfg['data']['labels'].append(test_names[i])
        if test_statuses[i] == 'FAIL':
            cfg['data']['datasets'][0]['data'].append(1)
            cfg['data']['datasets'][1]['data'].append(0)
        else:
            cfg['data']['datasets'][1]['data'].append(1)
            cfg['data']['datasets'][0]['data'].append(0)
    return cfg
