import firewall.config
from firewall.client import FirewallClient
from flask import Flask, render_template, url_for


app = Flask(__name__)
app.debug = True

#####################
# fw_offline helpers
#
def get_fw_zone_settings(zone):
    if fw_offline:
        fw_zone = fw.config.get_zone(zone)
        fw_settings = FirewallClientZoneSettings(
            list(fw.config.get_zone_config(fw_zone))
        )
    else:
        fw_zone = fw.config().getZoneByName(zone)
        fw_settings = fw_zone.getSettings()
 
    return (fw_zone, fw_settings)

def update_fw_settings(fw_zone, fw_settings):
    if fw_offline:
        fw.config.set_zone_config(fw_zone, fw_settings.settings)
    else:
        fw_zone.update(fw_settings)

####################
# source handling
#
def get_source(zone, source):
    fw_zone, fw_settings = get_fw_zone_settings(zone)
    if source in fw_settings.getSources():
       return True
    else:
        return False
        
def add_source(zone, source):
    fw_zone, fw_settings = get_fw_zone_settings(zone)
    fw_settings.addSource(source)
    update_fw_settings(fw_zone, fw_settings)

def remove_source(zone, source):
    fw_zone, fw_settings = get_fw_zone_settings(zone)
    fw_settings.removeSource(source)
    update_fw_settings(fw_zone, fw_settings)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/addsource")
def fetch_data():
    add_source('publicweb','192.168.100.24')

if __name__ == '__main__':
    
    ## Handle running (online) daemon vs non-running (offline) daemon
    global fw
    global fw_offline
    global Rich_Rule
    global FirewallClientZoneSettings
    fw_offline = False
 
    try:
        fw = FirewallClient()
    except AttributeError:
        ## Firewalld is not currently running, permanent-only operations
        print("Firewalld is not currently running")
    
    app.run(host='0.0.0.0')